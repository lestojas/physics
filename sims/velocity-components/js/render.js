/*
 * render.js — Canvas drawing and animation loop for the simulator.
 *
 * Responsibilities (VCS.render):
 *   - map physical radius (meters) to a pixel radius that always fits the canvas,
 *   - place the object on the circular path for a given angle,
 *   - compute the velocity (tangent) and force (radial-to-center) vectors,
 *   - draw the path, object, and both vectors with arrowheads, distinct colors,
 *     and text labels,
 *   - run a requestAnimationFrame loop timed to real wall-clock so one full
 *     revolution takes the current period T,
 *   - implement the play / pause / reset state machine.
 *
 * Loaded as a classic <script> (no ES module) and attaches to the global VCS
 * namespace. Pure geometry helpers are exposed for testing.
 */
(function (global) {
  "use strict";

  var VCS = global.VCS = global.VCS || {};
  var TAU = 2 * Math.PI;

  // ---- Rendering constants -------------------------------------------------
  // Pixel radius bounds for the circular path. R_MAX_PX plus MARGIN_PX must
  // leave room inside the canvas for the object, vectors, and labels.
  var R_MIN_PX = 30;
  var R_MAX_PX = 150;
  var MARGIN_PX = 70;      // reserved space outside the path for vectors/labels

  var K_V = 1.5;           // velocity vector: pixels per (m/s)
  var K_F = 0.5;           // force vector: pixels per newton (pre-clamp)
  var FORCE_MIN_FRAC = 0.05; // force length min as fraction of R_px
  var FORCE_MAX_FRAC = 1.00; // force length max as fraction of R_px

  var COLOR_PATH = "#4a5568";
  var COLOR_OBJECT = "#1a202c";
  var COLOR_VELOCITY = "#1e88e5"; // blue
  var COLOR_FORCE = "#e53935";    // red
  var COLOR_CENTER = "#a0aec0";

  var R_RANGE = { min: 0.1, max: 10 }; // must match physics RANGES.r

  // ---- Pure geometry helpers (exposed for tests) ---------------------------

  /**
   * Monotonic linear map from physical radius (meters) to a pixel radius.
   * Larger r yields a strictly larger pixel radius; the full path plus margin
   * always fits within the canvas. (Requirement 7.1)
   *
   * @param {number} r radius in meters
   * @returns {number} pixel radius
   */
  function mapRadius(r) {
    var t = (r - R_RANGE.min) / (R_RANGE.max - R_RANGE.min);
    if (t < 0) t = 0;
    if (t > 1) t = 1;
    return R_MIN_PX + (R_MAX_PX - R_MIN_PX) * t;
  }

  /**
   * Velocity vector length in pixels — strictly increasing in speed. (Req 8.6)
   * @param {number} v tangential speed (m/s)
   * @returns {number}
   */
  function velocityLength(v) {
    return K_V * v;
  }

  /**
   * Unclamped force vector length (pre-clamp), linear in F_net with a single
   * constant scale factor. (Requirement 9.5)
   * @param {number} fNet net centripetal force (N)
   * @returns {number}
   */
  function forceLengthRaw(fNet) {
    return K_F * fNet;
  }

  /**
   * Clamp a force vector length to [5%, 100%] of the pixel radius. Clamping is
   * idempotent. (Requirement 9.6)
   * @param {number} rawLength unclamped length in pixels
   * @param {number} rPx pixel radius of the path
   * @returns {number}
   */
  function clampForceLength(rawLength, rPx) {
    var lo = FORCE_MIN_FRAC * rPx;
    var hi = FORCE_MAX_FRAC * rPx;
    if (rawLength < lo) return lo;
    if (rawLength > hi) return hi;
    return rawLength;
  }

  /**
   * Object position on the path for a given center, pixel radius, and angle.
   * Canvas y grows downward. (Requirement 7.2)
   * @returns {{x:number, y:number}}
   */
  function objectPosition(center, rPx, theta) {
    return {
      x: center.x + rPx * Math.cos(theta),
      y: center.y + rPx * Math.sin(theta)
    };
  }

  /**
   * Unit vectors at a given angle:
   *   tangent (direction of motion) = direction * (-sinθ, cosθ)  [⊥ to radius]
   *   radial-to-center              = -(cosθ, sinθ)              [obj -> center]
   * @returns {{tangent:{x,y}, toCenter:{x,y}}}
   */
  function unitVectors(theta, direction) {
    var d = direction >= 0 ? 1 : -1;
    return {
      tangent: { x: d * -Math.sin(theta), y: d * Math.cos(theta) },
      toCenter: { x: -Math.cos(theta), y: -Math.sin(theta) }
    };
  }

  // ---- Canvas drawing primitives -------------------------------------------

  function drawArrow(ctx, from, dir, length, color, label) {
    if (length <= 0) return;
    var tipX = from.x + dir.x * length;
    var tipY = from.y + dir.y * length;

    ctx.save();
    ctx.strokeStyle = color;
    ctx.fillStyle = color;
    ctx.lineWidth = 3;

    // shaft
    ctx.beginPath();
    ctx.moveTo(from.x, from.y);
    ctx.lineTo(tipX, tipY);
    ctx.stroke();

    // arrowhead
    var ang = Math.atan2(dir.y, dir.x);
    var head = 10;
    ctx.beginPath();
    ctx.moveTo(tipX, tipY);
    ctx.lineTo(
      tipX - head * Math.cos(ang - Math.PI / 6),
      tipY - head * Math.sin(ang - Math.PI / 6)
    );
    ctx.lineTo(
      tipX - head * Math.cos(ang + Math.PI / 6),
      tipY - head * Math.sin(ang + Math.PI / 6)
    );
    ctx.closePath();
    ctx.fill();

    // label near the tip
    if (label) {
      ctx.font = "13px sans-serif";
      ctx.fillText(label, tipX + 6, tipY - 6);
    }
    ctx.restore();
  }

  // ---- init() : builds the controller + rAF loop ---------------------------

  /**
   * Initialize the renderer on a canvas.
   *
   * @param {HTMLCanvasElement} canvas
   * @param {function():object} getState returns the current MotionState
   *        ({r, m, T, v, omega, a_c, F_net}).
   * @param {function():object} getViewOptions returns { showForce:boolean }.
   * @returns {{play:Function, pause:Function, reset:Function,
   *            isPlaying:Function, currentAngle:Function, draw:Function}}
   */
  function init(canvas, getState, getViewOptions) {
    var ctx = canvas.getContext("2d");
    if (!ctx) {
      throw new Error("render.init: 2D canvas context unavailable");
    }

    var view = {
      theta: 0,          // current angular position (radians)
      initialTheta: 0,   // fixed reference start for reset (Req 7.7)
      direction: 1,      // constant sense of travel
      playing: false,    // state-machine flag
      lastTs: null       // last rAF timestamp for dt integration
    };

    function center() {
      return { x: canvas.width / 2, y: canvas.height / 2 };
    }

    function draw() {
      var state = getState();
      var opts = getViewOptions ? getViewOptions() : { showForce: true };
      var c = center();
      var rPx = mapRadius(state.r);

      ctx.clearRect(0, 0, canvas.width, canvas.height);

      // circular path
      ctx.save();
      ctx.strokeStyle = COLOR_PATH;
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.arc(c.x, c.y, rPx, 0, TAU);
      ctx.stroke();
      ctx.restore();

      // center marker
      ctx.save();
      ctx.fillStyle = COLOR_CENTER;
      ctx.beginPath();
      ctx.arc(c.x, c.y, 3, 0, TAU);
      ctx.fill();
      ctx.restore();

      var obj = objectPosition(c, rPx, view.theta);
      var units = unitVectors(view.theta, view.direction);

      // force vector (drawn first so velocity sits on top) — Req 9.7 toggle
      if (opts.showForce) {
        var lf = clampForceLength(forceLengthRaw(state.F_net), rPx);
        drawArrow(ctx, obj, units.toCenter, lf, COLOR_FORCE, "F_net (centripetal)");
      }

      // velocity vector (tangent, direction of motion) — Req 8
      var lv = velocityLength(state.v);
      drawArrow(ctx, obj, units.tangent, lv, COLOR_VELOCITY, "v (velocity)");

      // the object itself
      ctx.save();
      ctx.fillStyle = COLOR_OBJECT;
      ctx.beginPath();
      ctx.arc(obj.x, obj.y, 7, 0, TAU);
      ctx.fill();
      ctx.restore();
    }

    function step(now) {
      if (view.lastTs === null) view.lastTs = now;
      var dt = (now - view.lastTs) / 1000; // seconds
      view.lastTs = now;

      if (view.playing) {
        var state = getState();
        var T = state.T > 0 ? state.T : 1;
        // one revolution (2π) per real period T (Requirement 7.3)
        view.theta += view.direction * (TAU / T) * dt;
        // keep theta bounded for numeric stability
        view.theta = view.theta % TAU;
      }

      draw();
      global.requestAnimationFrame(step);
    }

    // Kick off the continuous render loop (draws even while paused so that
    // input changes are reflected immediately).
    if (typeof global.requestAnimationFrame === "function") {
      global.requestAnimationFrame(step);
    }

    return {
      play: function () {
        if (!view.playing) {
          view.playing = true;
          view.lastTs = null; // avoid a large dt jump after a pause
        }
      },
      pause: function () {
        view.playing = false;
      },
      reset: function () {
        view.theta = view.initialTheta;
        view.playing = false;
        view.lastTs = null;
        draw();
      },
      isPlaying: function () {
        return view.playing;
      },
      currentAngle: function () {
        return view.theta;
      },
      draw: draw
    };
  }

  VCS.render = {
    init: init,
    // Pure helpers exposed for tests and reuse:
    mapRadius: mapRadius,
    velocityLength: velocityLength,
    forceLengthRaw: forceLengthRaw,
    clampForceLength: clampForceLength,
    objectPosition: objectPosition,
    unitVectors: unitVectors,
    constants: {
      R_MIN_PX: R_MIN_PX,
      R_MAX_PX: R_MAX_PX,
      MARGIN_PX: MARGIN_PX,
      K_V: K_V,
      K_F: K_F,
      FORCE_MIN_FRAC: FORCE_MIN_FRAC,
      FORCE_MAX_FRAC: FORCE_MAX_FRAC,
      COLOR_VELOCITY: COLOR_VELOCITY,
      COLOR_FORCE: COLOR_FORCE
    }
  };
})(typeof window !== "undefined" ? window : this);
