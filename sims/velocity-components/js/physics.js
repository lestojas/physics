/*
 * physics.js — Pure computation model for the Velocity Components Simulator.
 *
 * This module is DOM-free and side-effect-free (apart from attaching itself to
 * the single global `VCS` namespace). It owns:
 *   - the canonical quantity ranges (single source of truth for bounds),
 *   - the coupled temporal computation ({T, v, ω}),
 *   - the derived quantities (centripetal acceleration a_c and net force F_net),
 *   - input classification/validation,
 *   - driver switching (preserving the {T, v, ω} triple), and
 *   - numeric formatting for the readouts.
 *
 * Everything here is deliberately pure so it can be reasoned about and property
 * tested in isolation. It is loaded via a classic <script> tag (NOT an ES
 * module) so it works from file:// with no server or bundler.
 */
(function (global) {
  "use strict";

  // The global namespace shared by all simulator modules.
  var VCS = global.VCS = global.VCS || {};

  var TAU = 2 * Math.PI;

  /**
   * Inclusive validity ranges for every user-facing quantity. This is the
   * single source of truth consumed by both validation and the UI.
   * (Requirements 3.5, 3.6, 3.7, 3.9, 3.10)
   */
  var RANGES = {
    r:     { min: 0.1, max: 10,  unit: "m"     },
    m:     { min: 0.1, max: 100, unit: "kg"    },
    T:     { min: 0.5, max: 60,  unit: "s"     },
    v:     { min: 0.1, max: 100, unit: "m/s"   },
    omega: { min: 0.1, max: 12,  unit: "rad/s" }
  };

  /**
   * Compute the consistent temporal triple {T, v, omega} from a radius and a
   * single motion driver. The driver's own value is preserved exactly; the two
   * non-driver quantities are derived from the governing equations.
   *
   *   driver "T":     v = 2πr / T ;   ω = 2π / T
   *   driver "v":     T = 2πr / v ;   ω = v / r
   *   driver "omega": v = r·ω     ;   T = 2π / ω
   *
   * (Requirements 4.1, 4.2, 4.3, 4.4, 4.5)
   *
   * @param {number} r          radius in meters (> 0)
   * @param {string} driver     one of "T", "v", "omega"
   * @param {number} driverValue value of the selected driver (> 0)
   * @returns {{T:number, v:number, omega:number}}
   */
  function computeTriple(r, driver, driverValue) {
    var T, v, omega;
    switch (driver) {
      case "T":
        T = driverValue;
        v = (TAU * r) / T;
        omega = TAU / T;
        break;
      case "v":
        v = driverValue;
        T = (TAU * r) / v;
        omega = v / r;
        break;
      case "omega":
        omega = driverValue;
        v = r * omega;
        T = TAU / omega;
        break;
      default:
        throw new Error("computeTriple: unknown driver '" + driver + "'");
    }
    return { T: T, v: v, omega: omega };
  }

  /**
   * Compute the derived quantities from radius, mass and the temporal triple.
   * a_c is computed as v²/r; rω² is available as a cross-check and agrees with
   * v²/r whenever the triple is consistent. F_net = m·a_c. Both are returned as
   * non-negative magnitudes.
   *
   * (Requirements 5.1, 5.2, 5.3, 5.4, 5.5, 5.6)
   *
   * @param {number} r
   * @param {number} m
   * @param {{v:number, omega:number}} triple
   * @returns {{a_c:number, F_net:number}}
   */
  function computeDerived(r, m, triple) {
    var v = triple.v;
    var omega = triple.omega;
    var a_c = (v * v) / r;          // primary formula: a_c = v² / r
    var a_c_cross = r * omega * omega; // cross-check: a_c = rω²
    // Guard against any tiny negative from floating point; magnitudes only.
    a_c = Math.abs(a_c);
    var F_net = Math.abs(m * a_c);
    return { a_c: a_c, F_net: F_net, a_c_cross: Math.abs(a_c_cross) };
  }

  /**
   * Convenience: compute the full motion state (triple + derived) from a state
   * object containing {r, m, driver, driverValue}.
   *
   * (Requirements 4, 5)
   *
   * @param {{r:number, m:number, driver:string, driverValue:number}} state
   * @returns {{T:number, v:number, omega:number, a_c:number, F_net:number}}
   */
  function computeMotion(state) {
    var triple = computeTriple(state.r, state.driver, state.driverValue);
    var derived = computeDerived(state.r, state.m, triple);
    return {
      T: triple.T,
      v: triple.v,
      omega: triple.omega,
      a_c: derived.a_c,
      F_net: derived.F_net
    };
  }

  /**
   * Classify a raw input string for a given field. Centralizes all validation
   * so main.js can decide whether to recompute or retain the last valid state.
   *
   *   non-numeric / empty          -> "ignored"  (Req 11.6)
   *   numeric <= 0                 -> "rejected" (Req 11.1–11.4)
   *   numeric > 0 but out of range -> "clamped"  (value = nearest bound) (Req 11.5)
   *   numeric within range         -> "accepted"
   *
   * @param {string} field one of "r", "m", "T", "v", "omega"
   * @param {*} raw raw input value (string from a text/number input)
   * @returns {{status:string, value?:number, message?:string}}
   */
  function classifyInput(field, raw) {
    var range = RANGES[field];
    if (!range) {
      throw new Error("classifyInput: unknown field '" + field + "'");
    }

    // Treat empty / whitespace-only as ignored.
    if (raw === null || raw === undefined) {
      return { status: "ignored", message: "Input ignored; kept last valid value." };
    }
    var str = String(raw).trim();
    if (str === "") {
      return { status: "ignored", message: "Input ignored; kept last valid value." };
    }

    // Number(...) rejects things like "1.2.3" and "abc" (returns NaN) while
    // still accepting scientific notation and signed values.
    var num = Number(str);
    if (!isFinite(num)) {
      return { status: "ignored", message: "Input ignored; kept last valid value." };
    }

    // Non-positive values are rejected for all physical quantities.
    if (num <= 0) {
      return { status: "rejected", message: "Value must be greater than zero; rejected." };
    }

    // Strictly-positive but out-of-range values are clamped to the nearest bound.
    if (num < range.min) {
      return { status: "clamped", value: range.min };
    }
    if (num > range.max) {
      return { status: "clamped", value: range.max };
    }

    return { status: "accepted", value: num };
  }

  /**
   * Switch the active motion driver without changing the physical motion. The
   * current consistent triple {T, v, ω} is recomputed and preserved, and the
   * new driver's `driverValue` is set to the current value of that quantity so
   * that no quantity changes on switch.
   *
   * (Requirements 4.6, 4.7)
   *
   * @param {{r:number, m:number, driver:string, driverValue:number}} state
   * @param {string} newDriver one of "T", "v", "omega"
   * @returns {object} a new state object with driver switched and preserved triple
   */
  function switchDriver(state, newDriver) {
    if (newDriver !== "T" && newDriver !== "v" && newDriver !== "omega") {
      throw new Error("switchDriver: unknown driver '" + newDriver + "'");
    }
    // Recompute the current triple from the existing driver so we have all
    // three values, then read off the value for the new driver.
    var triple = computeTriple(state.r, state.driver, state.driverValue);
    var newValue = triple[newDriver];
    var newState = {
      r: state.r,
      m: state.m,
      driver: newDriver,
      driverValue: newValue
    };
    // Carry any extra fields (e.g. cached quantities) forward, then overwrite
    // with the freshly preserved values.
    return newState;
  }

  /**
   * Format a numeric value for display: at most 3 decimal places. For nonzero
   * magnitudes smaller than 0.001, fall back to a form that preserves at least
   * one significant figure instead of rendering "0.000".
   *
   * (Requirements 6.3, 6.4)
   *
   * @param {number} x
   * @returns {string}
   */
  function formatValue(x) {
    if (typeof x !== "number" || !isFinite(x)) {
      return String(x);
    }
    if (x === 0) {
      return "0";
    }

    var mag = Math.abs(x);
    // Tiny nonzero magnitude: preserve >=1 significant figure.
    if (mag < 0.001) {
      // toPrecision(1) keeps a single significant figure, e.g. 0.00004 -> "4e-5".
      var p = x.toPrecision(1);
      // Normalize numeric noise (e.g. "0.00004000000001") without losing the
      // significant figure.
      return String(Number(p));
    }

    // Round to at most 3 decimals; strip trailing zeros for readability.
    var rounded = Math.round(x * 1000) / 1000;
    return String(rounded);
  }

  VCS.physics = {
    TAU: TAU,
    RANGES: RANGES,
    computeTriple: computeTriple,
    computeDerived: computeDerived,
    computeMotion: computeMotion,
    classifyInput: classifyInput,
    switchDriver: switchDriver,
    formatValue: formatValue
  };
})(typeof window !== "undefined" ? window : this);
