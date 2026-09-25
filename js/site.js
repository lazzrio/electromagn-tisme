/* Électromagnétisme — thème, menu, sommaires, chapitres validés, exercices faits, compte à rebours, hors ligne */
(function () {
  "use strict";
  var root = document.documentElement;

  function lire(cle, defaut) {
    try { var v = localStorage.getItem(cle); return v === null ? defaut : JSON.parse(v); } catch (e) { return defaut; }
  }
  function ecrire(cle, v) { try { localStorage.setItem(cle, JSON.stringify(v)); } catch (e) {} }

  /* ---------- thème ---------- */
  var thBtn = document.getElementById("themeBtn"), thIcon = document.getElementById("thIcon");
  var SUN = '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>';
  var MOON = '<path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/>';
  function theme() {
    if (root.getAttribute("data-theme")) return root.getAttribute("data-theme");
    return window.matchMedia && matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }
  function icone() { if (thIcon) thIcon.innerHTML = theme() === "dark" ? SUN : MOON; }
  var t0 = lire("em_theme", null);
  if (t0) root.setAttribute("data-theme", t0);
  icone();
  if (thBtn) thBtn.addEventListener("click", function () {
    var n = theme() === "dark" ? "light" : "dark";
    root.setAttribute("data-theme", n);
    ecrire("em_theme", n);
    icone();
  });

  /* ---------- menu téléphone ---------- */
  var burger = document.getElementById("burger"), nav = document.getElementById("nav");
  if (burger && nav) burger.addEventListener("click", function () {
    var o = nav.classList.toggle("open");
    burger.setAttribute("aria-expanded", o ? "true" : "false");
  });

  /* ---------- sommaires : surligner la section lue ---------- */
  function suivi(selLiens, classe, decalage) {
    var liens = Array.prototype.slice.call(document.querySelectorAll(selLiens));
    if (!liens.length) return;
    var cibles = liens.map(function (a) { return document.querySelector(a.getAttribute("href")); });
    function maj() {
      var y = window.scrollY + decalage, k = 0;
      cibles.forEach(function (c, i) { if (c && c.getBoundingClientRect().top + window.scrollY <= y) k = i; });
      liens.forEach(function (a, i) {
        var on = i === k;
        a.classList.toggle(classe, on);
        var p = a.parentNode;
        if (on && p.scrollWidth > p.clientWidth &&
            (a.offsetLeft < p.scrollLeft || a.offsetLeft + a.offsetWidth > p.scrollLeft + p.clientWidth)) {
          p.scrollLeft = a.offsetLeft - 16;
        }
      });
    }
    var t = null;
    window.addEventListener("scroll", function () { if (!t) t = setTimeout(function () { t = null; maj(); }, 120); }, { passive: true });
    maj();
  }
  suivi(".s4-toc a", "on", 150);
  suivi(".toc a[href^='#']", "active", 120);

  /* ---------- chapitres validés (page Cours) ---------- */
  var chap = lire("em_chapitres", {});
  document.querySelectorAll("[data-chk]").forEach(function (c) {
    var k = c.getAttribute("data-chk");
    c.checked = !!chap[k];
    c.addEventListener("change", function () { chap[k] = c.checked; ecrire("em_chapitres", chap); });
  });

  /* ---------- exercices faits (page Corrigés) ---------- */
  var faits = lire("em_faits", {});
  var arts = Array.prototype.slice.call(document.querySelectorAll("article.cx[id]"));
  function compte() {
    var p = document.getElementById("cxProgress");
    var n = arts.filter(function (a) { return faits[a.id]; }).length;
    if (p) p.textContent = n + " / " + arts.length + " faits";
    document.querySelectorAll(".cx-card[href^='#']").forEach(function (card) {
      var sec = document.querySelector(card.getAttribute("href"));
      if (!sec) return;
      var its = sec.querySelectorAll("article.cx[id]"), k = 0;
      its.forEach(function (i) { if (faits[i.id]) k++; });
      var cnt = card.querySelector(".cnt"), bar = card.querySelector(".bar i");
      if (cnt) cnt.textContent = k + " / " + its.length + " faits";
      if (bar) bar.style.width = (its.length ? 100 * k / its.length : 0) + "%";
    });
  }
  arts.forEach(function (a) {
    var hd = a.querySelector(".cx-hd");
    if (!hd) return;
    var b = document.createElement("button");
    b.type = "button";
    b.className = "cx-done";
    function peindre() {
      a.classList.toggle("done", !!faits[a.id]);
      b.textContent = faits[a.id] ? "✓ Fait" : "Marquer fait";
      b.setAttribute("aria-pressed", faits[a.id] ? "true" : "false");
    }
    b.addEventListener("click", function () { faits[a.id] = !faits[a.id]; ecrire("em_faits", faits); peindre(); compte(); });
    hd.appendChild(b);
    peindre();
  });
  compte();
  var tout = document.getElementById("cxExpand");
  if (tout) tout.addEventListener("click", function () {
    var ds = document.querySelectorAll("article.cx details");
    var ouvrir = Array.prototype.some.call(ds, function (d) { return !d.open; });
    ds.forEach(function (d) { d.open = ouvrir; });
    tout.textContent = ouvrir ? "Tout replier" : "Tout déplier";
    if (window.ajusterFormules) window.ajusterFormules(document);
  });
  function ouvrirAdresse() {
    var el = location.hash ? document.getElementById(location.hash.slice(1)) : null;
    if (el && el.matches("article.cx")) el.querySelectorAll("details").forEach(function (d) { d.open = true; });
    if (el && el.tagName === "DETAILS") el.open = true;
  }
  window.addEventListener("hashchange", ouvrirAdresse);
  ouvrirAdresse();

  /* ---------- compte à rebours (accueil) ---------- */
  var JALONS = [
    { d: new Date(2026, 8, 28, 8, 0, 0), t: "jours avant l'interro surprise de la semaine 40 (en TD)" },
    { d: new Date(2026, 9, 17, 11, 0, 0), t: "jours avant l'évaluation du samedi 17 octobre (11 h)" },
    { d: new Date(2026, 11, 14, 8, 0, 0), t: "jours avant la semaine des partiels (14 décembre)" }
  ];
  var cd = document.getElementById("countdown"), cdl = document.getElementById("countdownLbl");
  if (cd) {
    var now = new Date(), cible = null;
    for (var i = 0; i < JALONS.length; i++) { if (JALONS[i].d > now) { cible = JALONS[i]; break; } }
    if (cible) { cd.textContent = Math.max(0, Math.ceil((cible.d - now) / 864e5)); if (cdl) cdl.textContent = cible.t; }
    else { cd.textContent = "✓"; if (cdl) cdl.textContent = "évaluations du semestre terminées"; }
  }

  /* ---------- hors ligne ---------- */
  if ("serviceWorker" in navigator && location.protocol === "https:") {
    window.addEventListener("load", function () { navigator.serviceWorker.register("sw.js").catch(function () {}); });
  }
})();
