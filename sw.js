/* Hors ligne : le réseau d'abord (contenu toujours à jour), la copie locale si pas de connexion. */
const CACHE = "electromag-v3";
const CORE = ["./", "index.html", "interro-s40.html", "ds1.html", "cours.html", "formules.html", "corriges.html", "quiz.html",
  "css/style.css", "js/site.js", "js/maths.js", "js/quiz.js", "assets/favicon.svg", "assets/icon-192.png", "manifest.webmanifest"];

self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(CORE)).then(() => self.skipWaiting()));
});
self.addEventListener("activate", (e) => {
  e.waitUntil(caches.keys()
    .then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
    .then(() => self.clients.claim()));
});
self.addEventListener("fetch", (e) => {
  const req = e.request;
  const url = new URL(req.url);
  /* le site, plus KaTeX (formules) pour qu'il reste lisible hors ligne */
  if (req.method !== "GET" || (url.origin !== location.origin && url.host !== "cdn.jsdelivr.net")) return;
  e.respondWith(
    fetch(req)
      .then((res) => {
        if (res.ok) { const copie = res.clone(); caches.open(CACHE).then((c) => c.put(req, copie)); }
        return res;
      })
      .catch(() => caches.match(req, { ignoreSearch: true })
        .then((r) => r || (req.mode === "navigate" ? caches.match("index.html") : undefined)))
  );
});
