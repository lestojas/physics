/*
 * main.js — Application bootstrap and orchestration (VCS.main).
 *
 * Holds the authoritative MotionState, performs the asset self-check, wires the
 * Control_Panel to the physics model and renderer, and keeps the Readout_Panel
 * in sync. Runs after physics.js, render.js and ui.js have loaded.
 *
 * Flow on any input change:
 *   input -> classifyInput -> (accepted|clamped) recompute + update readouts +
 *   push state to renderer ; (rejected|ignored) keep last valid state + message.
 *
 * Loaded as a classic <script> (no ES module) and attaches to global VCS.
 */
(function (global) {
  "use strict";

  var VCS = global.VCS = global.VCS || {};
  var doc = global.document;

  // Default initial inputs (Design: Default Initial Inputs).
  var DEFAULTS = { r: 2, m: 1, driver: "T", driverValue: 4 };

  // Authoritative application state (last valid inputs + cached quantities).
  var state = {
    r: DEFAULTS.r,
    m: DEFAULTS.m,
    driver: DEFAULTS.driver,
    driverValue: DEFAULTS.driverValue,
    T: 0, v: 0, omega: 0, a_c: 0, F_net: 0
  };

  // View options owned here and read by the renderer via getViewOptions.
  var viewOptions = { showForce: true };

  var controller = null; // render controller

  /** Recompute all coupled/derived quantities into `state`. */
  function recompute() {
    var motion = VCS.physics.computeMotion(state);
    state.T = motion.T;
    state.v = motion.v;
    state.omega = motion.omega;
    state.a_c = motion.a_c;
    state.F_net = motion.F_net;
  }

  /** Push the current readouts to the UI. */
  function refreshReadouts() {
    VCS.ui.updateReadouts({
      r: state.r,
      m: state.m,
      T: state.T,
      v: state.v,
      omega: state.omega,
      a_c: state.a_c,
      F_net: state.F_net
    });
  }

  /**
   * Handle a change to the radius or mass input.
   * @param {string} field "r" or "m"
   * @param {string} raw
   */
  function onInput(field, raw) {
    var result = VCS.physics.classifyInput(field, raw);
    if (result.status === "accepted" || result.status === "clamped") {
      state[field] = result.value;
      VCS.ui.echoInput(field, result.value); // reflect clamped/normalized value
      VCS.ui.clearMessage(field);            // Req 11.7
      recompute();
      refreshReadouts();
    } else {
      // rejected or ignored: keep last valid, re-display it, show message
      VCS.ui.echoInput(field, state[field]);
      VCS.ui.showMessage(field, result.message);
      // Readouts intentionally left unchanged (Req 6.7).
    }
  }

  /**
   * Handle a change to the active driver value input.
   * @param {string} raw
   */
  function onDriverValue(raw) {
    var field = state.driver; // "T" | "v" | "omega"
    var result = VCS.physics.classifyInput(field, raw);
    if (result.status === "accepted" || result.status === "clamped") {
      state.driverValue = result.value;
      VCS.ui.echoInput("driver", result.value);
      VCS.ui.clearMessage("driver");
      recompute();
      refreshReadouts();
    } else {
      VCS.ui.echoInput("driver", state.driverValue);
      VCS.ui.showMessage("driver", result.message);
    }
  }

  /**
   * Handle a driver selector change: preserve the {T, v, ω} triple and echo the
   * preserved value into the driver input. (Req 4.6, 4.7)
   * @param {string} newDriver
   */
  function onDriverChange(newDriver) {
    var newState = VCS.physics.switchDriver(state, newDriver);
    state.driver = newState.driver;
    state.driverValue = newState.driverValue;
    VCS.ui.clearMessage("driver");
    recompute();
    VCS.ui.echoDriverInput(state.driver, state.driverValue);
    refreshReadouts();
  }

  function onForceToggle(checked) {
    viewOptions.showForce = !!checked;
    if (controller) controller.draw();
  }

  function onPlay() {
    if (controller) {
      controller.play();
      VCS.ui.setPlaying(true);
    }
  }

  function onPause() {
    if (controller) {
      controller.pause();
      VCS.ui.setPlaying(false);
    }
  }

  function onReset() {
    if (controller) {
      controller.reset();
      VCS.ui.setPlaying(false);
    }
  }

  /**
   * Verify required modules and the canvas 2D context are present. Returns true
   * when the app can run; otherwise shows the error banner and returns false.
   * (Requirements 2.7)
   */
  function assetSelfCheck(canvas) {
    var missing = [];
    if (!VCS.physics) missing.push("physics");
    if (!VCS.render) missing.push("render");
    if (!VCS.ui) missing.push("ui");

    if (missing.length > 0) {
      showBannerFallback("A required asset could not be loaded (" +
        missing.join(", ") + "). Please ensure all files are present.");
      return false;
    }
    if (!canvas || typeof canvas.getContext !== "function" || !canvas.getContext("2d")) {
      VCS.ui.showAssetError("The animation canvas is unavailable in this browser.");
      return false;
    }
    return true;
  }

  // Fallback banner in case VCS.ui itself failed to load.
  function showBannerFallback(text) {
    if (VCS.ui && VCS.ui.showAssetError) {
      VCS.ui.showAssetError(text);
      return;
    }
    var banner = doc.getElementById("error-banner");
    if (banner) {
      banner.textContent = text;
      banner.hidden = false;
      banner.className = (banner.className + " visible").trim();
    }
  }

  /** Bootstrap the whole simulator once the DOM is ready. */
  function boot() {
    var canvas = doc.getElementById("sim-canvas");

    if (!assetSelfCheck(canvas)) {
      return; // banner already shown
    }

    // Build UI.
    var controlRoot = doc.getElementById("control-panel");
    var readoutRoot = doc.getElementById("readout-panel");

    VCS.ui.buildReadouts(readoutRoot);
    VCS.ui.buildControls(controlRoot, {
      onInput: onInput,
      onDriverValue: onDriverValue,
      onDriverChange: onDriverChange,
      onForceToggle: onForceToggle,
      onPlay: onPlay,
      onPause: onPause,
      onReset: onReset
    }, {
      r: state.r,
      m: state.m,
      driver: state.driver,
      driverValue: state.driverValue,
      showForce: viewOptions.showForce
    });

    // Compute defaults and populate readouts before any interaction (Req 6.5).
    recompute();
    refreshReadouts();

    // Initialize the renderer with accessors into our state.
    controller = VCS.render.init(
      canvas,
      function () { return state; },
      function () { return viewOptions; }
    );
    VCS.ui.setPlaying(false);

    // Expose for tests / debugging.
    VCS.main = {
      getState: function () { return state; },
      getViewOptions: function () { return viewOptions; },
      getController: function () { return controller; },
      onInput: onInput,
      onDriverValue: onDriverValue,
      onDriverChange: onDriverChange,
      onForceToggle: onForceToggle
    };
  }

  // Provide VCS.main early (methods filled in on boot) so tests can detect it.
  VCS.main = VCS.main || {};

  if (doc) {
    if (doc.readyState === "loading") {
      doc.addEventListener("DOMContentLoaded", boot);
    } else {
      boot();
    }
  }
})(typeof window !== "undefined" ? window : this);
