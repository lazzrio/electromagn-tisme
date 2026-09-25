/* Quiz : questions lues dans #qzData (formules déjà rendues par KaTeX), mélangées à chaque partie */
(function () {
  "use strict";
  var data = document.getElementById("qzData"), card = document.getElementById("qzCard"), bar = document.getElementById("qzBar");
  if (!data || !card) return;
  var banque = Array.prototype.map.call(data.children, function (li) {
    var rep = Array.prototype.map.call(li.querySelectorAll("ul > li"), function (x) { return x.innerHTML; });
    return { q: li.querySelector("p").innerHTML, rep: rep, c: parseInt(li.getAttribute("data-c"), 10), exp: li.getAttribute("data-exp") };
  });
  var nb = 10, liste = [], i = 0, score = 0, fautes = [];

  function melange(t) {
    t = t.slice();
    for (var k = t.length - 1; k > 0; k--) { var j = Math.floor(Math.random() * (k + 1)); var x = t[k]; t[k] = t[j]; t[j] = x; }
    return t;
  }
  function rendre(el) {
    if (window.renderMathInElement) {
      var BS = String.fromCharCode(92);
      window.renderMathInElement(el, { delimiters: [{ left: BS + "(", right: BS + ")", display: false }], throwOnError: false, strict: false });
    }
  }
  function partie(n) {
    nb = n;
    liste = melange(banque).slice(0, n).map(function (q) {
      var ordre = melange(q.rep.map(function (_, k) { return k; }));
      return { q: q.q, rep: ordre.map(function (k) { return q.rep[k]; }), c: ordre.indexOf(q.c), exp: q.exp };
    });
    i = 0; score = 0; fautes = [];
    question();
  }
  function question() {
    var q = liste[i];
    card.innerHTML = '<div class="qz-meta"><span>Question ' + (i + 1) + " / " + liste.length + "</span><span>Score : " + score + "</span></div>" +
      '<div class="qz-q">' + q.q + '</div><div class="qz-ans">' +
      q.rep.map(function (r, k) { return '<button type="button" data-k="' + k + '">' + r + "</button>"; }).join("") + "</div>";
    card.querySelectorAll(".qz-ans button").forEach(function (b) {
      b.addEventListener("click", function () { repondre(parseInt(b.getAttribute("data-k"), 10)); });
    });
  }
  function repondre(k) {
    var q = liste[i], bs = card.querySelectorAll(".qz-ans button");
    bs.forEach(function (b, j) { b.disabled = true; if (j === q.c) b.classList.add("ok"); else if (j === k) b.classList.add("ko"); });
    if (k === q.c) score++; else fautes.push(q);
    var exp = document.createElement("div");
    exp.className = "qz-exp";
    exp.innerHTML = (k === q.c ? "<b>Juste.</b> " : "<b>Faux.</b> ") + q.exp;
    rendre(exp);
    card.appendChild(exp);
    var nx = document.createElement("button");
    nx.type = "button";
    nx.className = "qz-next";
    nx.textContent = i + 1 < liste.length ? "Question suivante →" : "Voir le résultat";
    nx.addEventListener("click", function () { i++; if (i < liste.length) question(); else resultat(); });
    card.appendChild(nx);
    nx.focus();
  }
  function resultat() {
    var pct = Math.round(100 * score / liste.length);
    var msg = pct >= 80 ? "Très bien : tu es prêt." : pct >= 50 ? "Bonne base : relis les explications des erreurs." : "Reprends le cours et les TD corrigés, puis refais le quiz.";
    card.innerHTML = '<div class="qz-res"><div class="big">' + score + " / " + liste.length + "</div><p>" + msg + "</p></div>" +
      (fautes.length ? "<h3 style=\"font-size:17px;margin-top:14px\">À revoir</h3>" + fautes.map(function (q) { return '<div class="qz-exp"><b>' + q.q + "</b><br>" + q.exp + "</div>"; }).join("") : "");
    rendre(card);
    var nx = document.createElement("button");
    nx.type = "button";
    nx.className = "qz-next";
    nx.textContent = "Nouvelle partie";
    nx.addEventListener("click", function () { partie(nb); });
    card.appendChild(nx);
  }
  bar.querySelectorAll("button[data-n]").forEach(function (b) {
    b.addEventListener("click", function () {
      bar.querySelectorAll("button[data-n]").forEach(function (x) { x.classList.toggle("on", x === b); });
      partie(parseInt(b.getAttribute("data-n"), 10));
    });
  });
  document.getElementById("qzRestart").addEventListener("click", function () { partie(nb); });
  partie(nb);
})();
