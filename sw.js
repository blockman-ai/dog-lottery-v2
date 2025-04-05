self.addEventListener('install', event => {
  event.waitUntil(
    caches.open('dog-lottery-cache').then(cache => {
      return cache.addAll([
        './',
        './index.html',
        './lottery_status.json',
        './lottery_entries.json',
        './manifest.json',
        './sw.js'
      ]);
    })
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request).then(response => {
      return response || fetch(event.request);
    })
  );
});
