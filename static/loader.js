// LOADER GLOBAL
// Variable para contar el número de peticiones activas
let activeRequests = 0;

// Referencia al elemento del modal de Bootstrap y su instancia
const loaderModalElement = document.getElementById('global-loader-modal');
// La API de Bootstrap para controlar el modal
const loaderModal = new bootstrap.Modal(loaderModalElement, {
  backdrop: 'static', // Evita que se cierre al hacer clic fuera
  keyboard: false     // Evita que se cierre con la tecla Escape
});

// Función para mostrar el loader
function showLoader() {
    activeRequests++;
    loaderModal.show();
}

// Función para ocultar el loader
function hideLoader() {
    activeRequests--;
    if (activeRequests <= 0) {
        activeRequests = 0; // Evitar que el contador sea negativo
        loaderModal.hide();
    }
}

// Interceptamos el método 'fetch' para agregar la lógica del loader
const originalFetch = window.fetch;

window.fetch = function(...args) {
    // 1. Mostrar el loader antes de la petición
    showLoader();

    // 2. Ejecutar la petición 'fetch' original
    return originalFetch.apply(this, args)
        .then(response => {
            // 3. Ocultar el loader cuando la petición finaliza (éxito)
            hideLoader();
            return response;
        })
        .catch(error => {
            // 4. Ocultar el loader también en caso de error
            hideLoader();
            console.error('Fetch error:', error);
            throw error; // Propagar el error
        });
};

