// Opcional: define una versión para futuras actualizaciones, incluso si no estás cacheando.
const CACHE_NAME = 'App-Chips-v1-no-cache';

self.addEventListener('install', event => {
  console.log('Service Worker instalado. No se están cacheando archivos.');
  // No hay un evento `waitUntil` para cachear activos.
});

self.addEventListener('fetch', event => {
  // En este caso, simplemente devolvemos la respuesta de la red.
  // No hay lógica de caché.
  event.respondWith(fetch(event.request));
});

// Opcional: Puedes agregar una lógica para limpiar cachés antiguos en la activación.
self.addEventListener('activate', event => {
  console.log('Service Worker activado.');
  // Lógica para limpiar cachés antiguos, si decides implementarlo en el futuro.
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.filter(cacheName => cacheName !== CACHE_NAME)
          .map(cacheName => caches.delete(cacheName))
      );
    })
  );
});