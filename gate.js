/* Verrou d'accès : demande un mot de passe avant d'afficher la page.
   Une fois saisi, il est mémorisé dans ce navigateur pour tous les sites lazzrio.github.io.
   Attention : protection côté navigateur seulement (dissuasive). Le contenu reste dans le dépôt GitHub. */
(function () {
  "use strict";
  var KEY = "gate_v1";
  var HASH = "26954047a47e4986aa521187833971b97989cd14607e1901d4f43b2dae69039f";
  var SALT = "lazzrio-gate:";

  function sha256(str) {
    var K = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5, 0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
      0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da, 0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
      0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85, 0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
      0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3, 0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2];
    var H = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19];
    var b = unescape(encodeURIComponent(str)), n = b.length, w = [], i, j;
    for (i = 0; i < n; i++) w[i >> 2] |= b.charCodeAt(i) << (24 - (i % 4) * 8);
    w[n >> 2] |= 0x80 << (24 - (n % 4) * 8);
    w[(((n + 8) >> 6) << 4) + 15] = n * 8;
    function rr(x, c) { return (x >>> c) | (x << (32 - c)); }
    for (i = 0; i < w.length; i += 16) {
      var a = H.slice(), t = new Array(64);
      for (j = 0; j < 64; j++) {
        if (j < 16) t[j] = w[i + j] | 0;
        else {
          var s0 = rr(t[j - 15], 7) ^ rr(t[j - 15], 18) ^ (t[j - 15] >>> 3);
          var s1 = rr(t[j - 2], 17) ^ rr(t[j - 2], 19) ^ (t[j - 2] >>> 10);
          t[j] = (t[j - 16] + s0 + t[j - 7] + s1) | 0;
        }
        var S1 = rr(a[4], 6) ^ rr(a[4], 11) ^ rr(a[4], 25);
        var ch = (a[4] & a[5]) ^ (~a[4] & a[6]);
        var t1 = (a[7] + S1 + ch + K[j] + t[j]) | 0;
        var S0 = rr(a[0], 2) ^ rr(a[0], 13) ^ rr(a[0], 22);
        var mj = (a[0] & a[1]) ^ (a[0] & a[2]) ^ (a[1] & a[2]);
        var t2 = (S0 + mj) | 0;
        a = [(t1 + t2) | 0, a[0], a[1], a[2], (a[3] + t1) | 0, a[4], a[5], a[6]];
      }
      for (j = 0; j < 8; j++) H[j] = (H[j] + a[j]) | 0;
    }
    return H.map(function (x) { return ("00000000" + (x >>> 0).toString(16)).slice(-8); }).join("");
  }

  function dejaOuvert() { try { return localStorage.getItem(KEY) === HASH; } catch (e) { return false; } }
  if (dejaOuvert()) return;

  var root = document.documentElement;
  var avant = { v: root.style.visibility, o: root.style.overflow };
  root.style.visibility = "hidden";
  root.style.overflow = "hidden";

  var ov = document.createElement("div");
  ov.setAttribute("role", "dialog");
  ov.setAttribute("aria-label", "Accès protégé");
  ov.style.cssText = "position:fixed;inset:0;z-index:2147483647;visibility:visible;display:grid;place-items:center;padding:24px;" +
    "background:#161211;color:#efe6d8;font-family:system-ui,-apple-system,Segoe UI,sans-serif";
  ov.innerHTML =
    '<form id="gate-f" style="width:min(360px,100%);text-align:center">' +
    '<div style="font-size:42px;line-height:1">🔒</div>' +
    '<h1 style="font-size:22px;margin:14px 0 6px">Accès protégé</h1>' +
    '<p style="margin:0 0 18px;color:#a1917d;font-size:14px">Saisis le mot de passe pour afficher ce site.</p>' +
    '<input id="gate-p" type="password" autocomplete="current-password" placeholder="Mot de passe" autofocus ' +
    'style="width:100%;box-sizing:border-box;padding:12px 14px;border-radius:10px;border:1px solid #4a3f36;background:#1e1815;color:#efe6d8;font-size:16px">' +
    '<button type="submit" style="margin-top:12px;width:100%;padding:12px;border:0;border-radius:10px;background:#e0864a;color:#1a1008;font-size:16px;font-weight:600;cursor:pointer">Entrer</button>' +
    '<p id="gate-e" role="alert" style="min-height:20px;margin:12px 0 0;color:#e77d70;font-size:14px"></p>' +
    "</form>";

  function monter() {
    (document.body || root).appendChild(ov);
    var f = ov.querySelector("#gate-f"), p = ov.querySelector("#gate-p"), e = ov.querySelector("#gate-e");
    f.addEventListener("submit", function (ev) {
      ev.preventDefault();
      if (sha256(SALT + p.value) === HASH) {
        try { localStorage.setItem(KEY, HASH); } catch (x) {}
        ov.remove();
        root.style.visibility = avant.v;
        root.style.overflow = avant.o;
      } else {
        e.textContent = "Mot de passe incorrect.";
        p.value = "";
        p.focus();
      }
    });
    p.focus();
  }
  if (document.body) monter(); else document.addEventListener("DOMContentLoaded", monter);
})();
