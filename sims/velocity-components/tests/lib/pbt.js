/*
 * pbt.js — A tiny, zero-dependency property-based-testing helper.
 *
 * This file is a TEST-ONLY utility. It is intentionally NOT referenced by the
 * shipped simulator (`sims/velocity-components/index.html`), so the deliverable
 * remains self-contained and dependency-free (preserves Requirement 2.2).
 *
 * It provides:
 *   - a small deterministic PRNG (so failures are reproducible),
 *   - value generators (bounded floats, integers, driver picks, angles,
 *     invalid/edge input strings, small-magnitude reals, frame-delta schedules),
 *   - a `forAll(gen, predicate, {iterations})` runner (default >= 100 iterations),
 *   - basic shrinking toward simpler counterexamples.
 *
 * It works both in the browser (attaches to window.PBT) and under Node
 * (module.exports), so property tests can run in either environment.
 */
(function (global) {
  "use strict";

  // ---- Deterministic PRNG (mulberry32) -------------------------------------
  function makeRng(seed) {
    var a = seed >>> 0;
    return function () {
      a |= 0;
      a = (a + 0x6D2B79F5) | 0;
      var t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  // ---- Generator constructors ----------------------------------------------
  // A generator is: { sample(rng) -> value, shrink(value) -> [values] }.

  function float(min, max) {
    return {
      sample: function (rng) { return min + (max - min) * rng(); },
      shrink: function (v) {
        var mid = (min + max) / 2;
        var candidates = [min, mid, (v + min) / 2];
        return candidates.filter(function (c) { return c !== v && c >= min && c <= max; });
      }
    };
  }

  function integer(min, max) {
    return {
      sample: function (rng) { return Math.floor(min + (max - min + 1) * rng()); },
      shrink: function (v) {
        var out = [];
        if (v > min) out.push(min);
        if (v - 1 > min) out.push(v - 1);
        return out;
      }
    };
  }

  function pick(items) {
    return {
      sample: function (rng) { return items[Math.floor(rng() * items.length)]; },
      shrink: function (v) {
        var i = items.indexOf(v);
        return i > 0 ? [items[0]] : [];
      }
    };
  }

  function driver() { return pick(["T", "v", "omega"]); }

  function angle() { return float(0, 2 * Math.PI); }

  // Strings that should be treated as non-numeric / empty (ignored inputs).
  function invalidString() {
    return pick(["", "   ", "abc", "1.2.3", "NaN", "--5", "1e", "+", "one", "10x"]);
  }

  // Non-positive numeric values (rejected inputs).
  function nonPositive() {
    return {
      sample: function (rng) { return -(rng() * 100); },
      shrink: function () { return [0]; }
    };
  }

  // Small nonzero magnitudes (0 < |x| < 0.001) for formatting tests.
  function smallMagnitude() {
    return {
      sample: function (rng) {
        var sign = rng() < 0.5 ? -1 : 1;
        // range roughly [1e-9, 9e-4]
        var mag = Math.pow(10, -(3 + rng() * 6)) * (1 + rng() * 8);
        return sign * mag;
      },
      shrink: function () { return []; }
    };
  }

  // A schedule of positive frame deltas (seconds) that sum exactly to `total`.
  function frameDeltas(total, maxFrames) {
    maxFrames = maxFrames || 120;
    return {
      sample: function (rng) {
        var n = 1 + Math.floor(rng() * maxFrames);
        var raw = [];
        var sum = 0;
        for (var i = 0; i < n; i++) {
          var d = rng() + 1e-6;
          raw.push(d);
          sum += d;
        }
        // normalize so the deltas sum exactly to `total`
        return raw.map(function (d) { return (d / sum) * total; });
      },
      shrink: function () { return [[total]]; } // simplest: single frame
    };
  }

  function record(shape) {
    var keys = Object.keys(shape);
    return {
      sample: function (rng) {
        var obj = {};
        keys.forEach(function (k) { obj[k] = shape[k].sample(rng); });
        return obj;
      },
      shrink: function (v) {
        var out = [];
        keys.forEach(function (k) {
          var shrunk = shape[k].shrink(v[k]);
          shrunk.forEach(function (s) {
            var clone = {};
            keys.forEach(function (kk) { clone[kk] = v[kk]; });
            clone[k] = s;
            out.push(clone);
          });
        });
        return out;
      }
    };
  }

  // ---- The forAll runner ----------------------------------------------------

  /**
   * Run `predicate` against generated values. Throws on the first failing case
   * (after shrinking) with a descriptive message.
   *
   * @param {object} gen a generator ({sample, shrink})
   * @param {function(value):(boolean|void)} predicate returns false/throws on failure
   * @param {object} [opts] { iterations>=100, seed }
   * @returns {{ok:true, iterations:number}}
   */
  function forAll(gen, predicate, opts) {
    opts = opts || {};
    var iterations = Math.max(100, opts.iterations || 100);
    var seed = opts.seed != null ? opts.seed : (Date.now() >>> 0);
    var rng = makeRng(seed);

    function passes(value) {
      try {
        return predicate(value) !== false;
      } catch (e) {
        return false;
      }
    }

    for (var i = 0; i < iterations; i++) {
      var value = gen.sample(rng);
      if (!passes(value)) {
        var shrunk = shrink(gen, value, passes);
        throw new Error(
          "Property failed (seed=" + seed + ", iteration=" + i + "). " +
          "Counterexample: " + safeStringify(shrunk)
        );
      }
    }
    return { ok: true, iterations: iterations };
  }

  // Greedy shrinking: repeatedly replace the value with a smaller failing one.
  function shrink(gen, value, passes) {
    var current = value;
    var improved = true;
    var guard = 0;
    while (improved && guard < 1000) {
      improved = false;
      guard++;
      var candidates = gen.shrink ? gen.shrink(current) : [];
      for (var i = 0; i < candidates.length; i++) {
        if (!passes(candidates[i])) {
          current = candidates[i];
          improved = true;
          break;
        }
      }
    }
    return current;
  }

  function safeStringify(v) {
    try { return JSON.stringify(v); } catch (e) { return String(v); }
  }

  var PBT = {
    makeRng: makeRng,
    forAll: forAll,
    shrink: shrink,
    gen: {
      float: float,
      integer: integer,
      pick: pick,
      driver: driver,
      angle: angle,
      invalidString: invalidString,
      nonPositive: nonPositive,
      smallMagnitude: smallMagnitude,
      frameDeltas: frameDeltas,
      record: record
    }
  };

  if (typeof module !== "undefined" && module.exports) {
    module.exports = PBT;
  }
  global.PBT = PBT;
})(typeof window !== "undefined" ? window : (typeof globalThis !== "undefined" ? globalThis : this));
