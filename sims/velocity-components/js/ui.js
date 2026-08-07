/*
 * ui.js — Control_Panel, Readout_Panel wiring, validation messages, and the
 * asset-error banner (VCS.ui).
 *
 * This module builds the interactive widgets inside the (initially empty)
 * panel containers provided by index.html, echoes readouts/driver values, and
 * surfaces per-field validation messages. It holds no physics; it only calls
 * back into handlers supplied by main.js.
 *
 * Loaded as a classic <script> (no ES module) and attaches to global VCS.
 */
(function (global) {
  "use strict";

  var VCS = global.VCS = global.VCS || {};
  var doc = global.document;

  // Human-friendly metadata for the driver value input.
  var DRIVER_META = {
    T:     { label: "Period T", unit: "s" },
    v:     { label: "Tangential speed v", unit: "m/s" },
    omega: { label: "Angular speed \u03C9", unit: "rad/s" } // ω
  };

  // Readout rows: order + symbol + unit. (Requirements 6.1, 6.2)
  var READOUT_ROWS = [
    { key: "r",     symbol: "r",              unit: "m"      },
    { key: "m",     symbol: "m",              unit: "kg"     },
    { key: "T",     symbol: "T",              unit: "s"      },
    { key: "v",     symbol: "v",              unit: "m/s"    },
    { key: "omega", symbol: "\u03C9",         unit: "rad/s"  }, // ω
    { key: "a_c",   symbol: "a\u1D04",        unit: "m/s\u00B2" }, // a_c, m/s²
    { key: "F_net", symbol: "F\u2099\u2091\u209C", unit: "N" }   // F_net
  ];

  // Internal references to created DOM elements, populated by buildControls /
  // buildReadouts.
  var els = {
    inputs: {},     // field -> <input>
    messages: {},   // field -> <span> message element
    readouts: {},   // key -> <span> value element
    driverSelect: null,
    driverValueInput: null,
    driverValueLabel: null,
    driverValueUnit: null,
    forceToggle: null,
    playBtn: null,
    pauseBtn: null,
    resetBtn: null,
    banner: null
  };

  function el(tag, opts) {
    var node = doc.createElement(tag);
    opts = opts || {};
    if (opts.className) node.className = opts.className;
    if (opts.text != null) node.textContent = opts.text;
    if (opts.id) node.id = opts.id;
    if (opts.attrs) {
      Object.keys(opts.attrs).forEach(function (k) {
        node.setAttribute(k, opts.attrs[k]);
      });
    }
    return node;
  }

  /**
   * Build a labeled numeric input row with an inline message span.
   * @returns {HTMLElement} the row container
   */
  function buildNumericRow(field, labelText, value, handlers) {
    var range = VCS.physics.RANGES[field];
    var row = el("div", { className: "control-row" });

    var label = el("label", { className: "control-label", text: labelText });
    var input = el("input", {
      className: "control-input",
      attrs: {
        type: "number",
        step: "any",
        min: String(range.min),
        max: String(range.max),
        value: String(value)
      }
    });
    var msg = el("span", { className: "control-message", attrs: { role: "alert" } });

    input.addEventListener("change", function () {
      handlers.onInput(field, input.value);
    });

    row.appendChild(label);
    row.appendChild(input);
    row.appendChild(msg);

    els.inputs[field] = input;
    els.messages[field] = msg;
    return row;
  }

  /**
   * Build all Control_Panel widgets and the animation controls.
   * (Requirements 3.1, 3.2, 3.3, 3.4, 3.11, 7.4, 9.7)
   *
   * @param {HTMLElement} root container for the control panel
   * @param {object} handlers { onInput(field, raw), onDriverChange(driver),
   *                            onDriverValue(raw), onForceToggle(bool),
   *                            onPlay(), onPause(), onReset() }
   * @param {object} initial   { r, m, driver, driverValue, showForce }
   */
  function buildControls(root, handlers, initial) {
    root.innerHTML = "";

    // radius + mass
    root.appendChild(buildNumericRow("r", "Radius r (m)", initial.r, handlers));
    root.appendChild(buildNumericRow("m", "Mass m (kg)", initial.m, handlers));

    // driver selector
    var driverRow = el("div", { className: "control-row" });
    driverRow.appendChild(el("label", { className: "control-label", text: "Motion driver" }));
    var select = el("select", { className: "control-input" });
    [
      { v: "T", t: "Period (T)" },
      { v: "v", t: "Tangential speed (v)" },
      { v: "omega", t: "Angular speed (\u03C9)" }
    ].forEach(function (o) {
      var opt = el("option", { text: o.t });
      opt.value = o.v;
      if (o.v === initial.driver) opt.selected = true;
      select.appendChild(opt);
    });
    select.addEventListener("change", function () {
      handlers.onDriverChange(select.value);
    });
    driverRow.appendChild(select);
    root.appendChild(driverRow);
    els.driverSelect = select;

    // active driver value input
    var meta = DRIVER_META[initial.driver];
    var dRow = el("div", { className: "control-row" });
    var dLabel = el("label", {
      className: "control-label",
      text: meta.label + " (" + meta.unit + ")"
    });
    var dInput = el("input", {
      className: "control-input",
      attrs: {
        type: "number",
        step: "any",
        value: String(initial.driverValue)
      }
    });
    var dMsg = el("span", { className: "control-message", attrs: { role: "alert" } });
    dInput.addEventListener("change", function () {
      handlers.onDriverValue(dInput.value);
    });
    dRow.appendChild(dLabel);
    dRow.appendChild(dInput);
    dRow.appendChild(dMsg);
    root.appendChild(dRow);
    els.driverValueInput = dInput;
    els.driverValueLabel = dLabel;
    els.messages.driver = dMsg;

    // force-display toggle
    var fRow = el("div", { className: "control-row" });
    var fLabel = el("label", { className: "control-label", text: "Show force vector" });
    var fToggle = el("input", { attrs: { type: "checkbox" } });
    fToggle.checked = initial.showForce !== false;
    fToggle.addEventListener("change", function () {
      handlers.onForceToggle(fToggle.checked);
    });
    fLabel.insertBefore(fToggle, fLabel.firstChild);
    fRow.appendChild(fLabel);
    root.appendChild(fRow);
    els.forceToggle = fToggle;

    // play / pause / reset buttons
    var btnRow = el("div", { className: "control-row button-row" });
    var play = el("button", { className: "btn", text: "Play" });
    var pause = el("button", { className: "btn", text: "Pause" });
    var reset = el("button", { className: "btn", text: "Reset" });
    play.addEventListener("click", handlers.onPlay);
    pause.addEventListener("click", handlers.onPause);
    reset.addEventListener("click", handlers.onReset);
    btnRow.appendChild(play);
    btnRow.appendChild(pause);
    btnRow.appendChild(reset);
    root.appendChild(btnRow);
    els.playBtn = play;
    els.pauseBtn = pause;
    els.resetBtn = reset;
  }

  /**
   * Build the Readout_Panel rows (values filled later by updateReadouts).
   * (Requirements 6.1, 6.2)
   * @param {HTMLElement} root
   */
  function buildReadouts(root) {
    root.innerHTML = "";
    var list = el("dl", { className: "readout-list" });
    READOUT_ROWS.forEach(function (row) {
      var dt = el("dt", { className: "readout-term", text: row.symbol });
      var dd = el("dd", { className: "readout-def" });
      var val = el("span", { className: "readout-value", text: "-" });
      var unit = el("span", { className: "readout-unit", text: " " + row.unit });
      dd.appendChild(val);
      dd.appendChild(unit);
      list.appendChild(dt);
      list.appendChild(dd);
      els.readouts[row.key] = val;
    });
    root.appendChild(list);
  }

  /**
   * Write the seven readout values with formatting. (Requirements 6.1–6.4)
   * @param {object} values { r, m, T, v, omega, a_c, F_net }
   */
  function updateReadouts(values) {
    READOUT_ROWS.forEach(function (row) {
      var span = els.readouts[row.key];
      if (span && values[row.key] != null) {
        span.textContent = VCS.physics.formatValue(values[row.key]);
      }
    });
  }

  /**
   * After a driver switch, update the driver value input's label/unit and echo
   * the preserved value. (Requirement 4.7)
   * @param {string} driver
   * @param {number} value
   */
  function echoDriverInput(driver, value) {
    var meta = DRIVER_META[driver];
    if (els.driverValueLabel && meta) {
      els.driverValueLabel.textContent = meta.label + " (" + meta.unit + ")";
    }
    if (els.driverValueInput) {
      els.driverValueInput.value = VCS.physics.formatValue(value);
    }
  }

  /**
   * Re-display a field's value in its input (used after reject/ignore/clamp).
   * @param {string} field  "r", "m", or "driver"
   * @param {number} value
   */
  function echoInput(field, value) {
    var input = field === "driver" ? els.driverValueInput : els.inputs[field];
    if (input) {
      input.value = VCS.physics.formatValue(value);
    }
  }

  /** Show a per-field validation message. (Req 11.2–11.6) */
  function showMessage(field, text) {
    var msg = els.messages[field];
    if (msg) {
      msg.textContent = text;
      msg.classList.add("visible");
    }
  }

  /** Clear a per-field validation message. (Req 11.7) */
  function clearMessage(field) {
    var msg = els.messages[field];
    if (msg) {
      msg.textContent = "";
      msg.classList.remove("visible");
    }
  }

  /** Show the global asset-error banner. (Req 1.6, 2.7) */
  function showAssetError(text) {
    if (!els.banner) {
      els.banner = doc.getElementById("error-banner");
    }
    if (els.banner) {
      els.banner.textContent = text;
      els.banner.classList.add("visible");
      els.banner.hidden = false;
    }
  }

  /** Reflect play/pause state on the buttons (optional visual cue). */
  function setPlaying(isPlaying) {
    if (els.playBtn) els.playBtn.disabled = isPlaying;
    if (els.pauseBtn) els.pauseBtn.disabled = !isPlaying;
  }

  VCS.ui = {
    buildControls: buildControls,
    buildReadouts: buildReadouts,
    updateReadouts: updateReadouts,
    echoDriverInput: echoDriverInput,
    echoInput: echoInput,
    showMessage: showMessage,
    clearMessage: clearMessage,
    showAssetError: showAssetError,
    setPlaying: setPlaying
  };
})(typeof window !== "undefined" ? window : this);
