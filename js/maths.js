/* Formules des corrigés : rendu KaTeX, puis ajustement de la taille des formules centrées
   pour qu'elles tiennent dans la largeur de l'écran (téléphone). Au-delà de la réduction
   maximale, la formule défile horizontalement dans son cadre. */
(function () {
  "use strict";
  var BS = String.fromCharCode(92);
  if (window.renderMathInElement) {
    window.renderMathInElement(document.body, {
      delimiters: [
        { left: BS + "[", right: BS + "]", display: true },
        { left: BS + "(", right: BS + ")", display: false }
      ],
      throwOnError: false,
      strict: false
    });
  }

  var MIN = 0.66;
  function ajuster(racine) {
    var blocs = (racine || document).querySelectorAll(".katex-display");
    Array.prototype.forEach.call(blocs, function (d) {
      var k = d.querySelector(".katex");
      if (!k) return;
      k.style.fontSize = "";
      var dispo = d.clientWidth;
      if (!dispo) return;                    /* bloc replié : on ajustera à l'ouverture */
      var besoin = k.scrollWidth;
      if (besoin > dispo) {
        var r = Math.max(MIN, (dispo - 4) / besoin);
        k.style.fontSize = (r * 1.07).toFixed(3) + "em";
      }
    });
  }

  document.addEventListener("toggle", function (e) {
    if (e.target && e.target.open) ajuster(e.target);
  }, true);
  var t = null;
  window.addEventListener("resize", function () {
    clearTimeout(t);
    t = setTimeout(function () { ajuster(document); }, 150);
  });
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { ajuster(document); });
  window.addEventListener("beforeprint", function () { ajuster(document); });
  window.ajusterFormules = ajuster;
})();
