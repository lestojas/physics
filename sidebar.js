/* =============================================================
   PHYlip Simulators — shared, auto-updating, collapsible sidebar
   -------------------------------------------------------------
   FOLDER LAYOUT
     index.html          <- home page (root)
     styles.css
     sidebar.js          <- this file
     sims/               <- put every simulator .html in here
       falling-target.html
       velocity-components.html
       _template.html     (files starting with "_" are ignored)

   HOW NEW SIMULATORS APPEAR
   - Run the folder through a local web server (see the guide):
     the sidebar AUTO-DISCOVERS every .html inside sims/.
     Just drop a new file into sims/, refresh — it's listed.
     No edits to any list required.
   - If you instead open a file by double-click (file://),
     browsers can't read a folder, so it uses the FALLBACK
     list below. Add new filenames there for offline use.

   OPTIONAL: nicer titles/subtitles in META (else auto-titled).
   ============================================================= */
(function () {
  "use strict";

  // Used only when opened via file:// (double-click).
  var FALLBACK = [
    "falling-target.html",
    "velocity-components.html"
  ];

  // Optional prettier labels. Unlisted files are auto-titled.
  var META = {
    "falling-target.html":      { title: "Falling Target" },
    "velocity-components.html": { title: "Velocity Components" }
  };

  // Are we currently on a page inside sims/ ?
  var inSims = /\/sims\/[^\/]*$/.test(location.pathname);
  var base = inSims ? "../" : "";        // prefix back to the root folder
  var simsDir = base + "sims/";

  function prettify(file) {
    if (META[file] && META[file].title) return META[file].title;
    return file.replace(/\.html$/i, "")
               .replace(/[-_]+/g, " ")
               .replace(/\b\w/g, function (c) { return c.toUpperCase(); });
  }

  function currentFile() {
    var f = location.pathname.split("/").pop();
    return f && f.length ? f : "index.html";
  }

  function keep(file) {
    // Skip helper/template files (leading underscore) and non-html.
    return /\.html$/i.test(file) && file.charAt(0) !== "_" && file.indexOf("/") === -1;
  }

  function discover() {
    // Read the sims/ directory listing (works when served by a web server).
    return fetch(simsDir, { cache: "no-store" })
      .then(function (res) {
        if (!res.ok) throw new Error("no listing");
        return res.text();
      })
      .then(function (text) {
        var doc = new DOMParser().parseFromString(text, "text/html");
        var links = Array.prototype.slice.call(doc.querySelectorAll("a[href]"));
        var files = links
          .map(function (a) { return a.getAttribute("href") || ""; })
          .map(function (h) { return h.replace(/^\.\//, ""); })
          .map(function (h) { try { return decodeURIComponent(h); } catch (e) { return h; } })
          .filter(keep);
        var seen = {}, unique = [];
        files.forEach(function (f) { if (!seen[f]) { seen[f] = true; unique.push(f); } });
        if (!unique.length) throw new Error("empty");
        unique.sort();
        return unique;
      })
      .catch(function () {
        return FALLBACK.filter(keep).sort();
      });
  }

  function render(sims) {
    var cur = currentFile();
    var atHome = !inSims && (cur === "index.html");

    var homeItem =
      '<li><a' + (atHome ? ' class="active"' : '') + ' href="' + base + 'index.html">' +
        '<span class="num">\u2630</span>' +
        '<span class="t"><b>Home</b></span>' +
      '</a></li>';

    var n = 0;
    var items = sims.map(function (f) {
      var meta = META[f] || {};
      var sub = meta.sub ? "<small>" + meta.sub + "</small>" : "";
      var active = (f === cur) ? ' class="active"' : '';
      return '<li><a' + active + ' href="' + simsDir + f + '">' +
               '<span class="num">' + (++n) + '</span>' +
               '<span class="t"><b>' + prettify(f) + '</b>' + sub + '</span>' +
             '</a></li>';
    }).join("");

    return '<div class="sidebar-head">' +
             '<p class="brand">PHYlip <span class="accent">Simulators</span></p>' +
             '<button class="nav-collapse" id="nav-collapse" title="Hide menu" aria-label="Hide menu">\u00ab</button>' +
           '</div>' +
           '<p class="brand-sub">Interactive physics simulators</p>' +
           '<p class="nav-label">Simulators</p>' +
           '<ul class="nav">' + homeItem + items + '</ul>';
  }

  function init() {
    var host = document.getElementById("app-sidebar");
    if (!host) return;
    host.className = "sidebar";
    var app = document.querySelector(".app") || document.body;

    // Floating "open" button, visible only when the sidebar is collapsed.
    var openBtn = document.createElement("button");
    openBtn.className = "nav-open";
    openBtn.id = "nav-open";
    openBtn.setAttribute("aria-label", "Show menu");
    openBtn.innerHTML = "\u2630";
    document.body.appendChild(openBtn);

    function setCollapsed(collapsed) {
      app.classList.toggle("nav-collapsed", collapsed);
      try { localStorage.setItem("phylipNav", collapsed ? "1" : "0"); } catch (e) {}
      // let the simulators refit their canvas to the new width (after transition)
      setTimeout(function () { window.dispatchEvent(new Event("resize")); }, 40);
      setTimeout(function () { window.dispatchEvent(new Event("resize")); }, 300);
    }
    openBtn.addEventListener("click", function () { setCollapsed(false); });

    // Restore saved state.
    var saved = "0";
    try { saved = localStorage.getItem("phylipNav") || "0"; } catch (e) {}
    if (saved === "1") app.classList.add("nav-collapsed");

    discover().then(function (sims) {
      host.innerHTML = render(sims);
      var cb = document.getElementById("nav-collapse");
      if (cb) cb.addEventListener("click", function () { setCollapsed(true); });
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
