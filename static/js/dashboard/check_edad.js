    document.addEventListener('DOMContentLoaded', function() {
        const fechaNacimientoInput = document.getElementById('id_fecha_nacimiento');
        const botonProcesar = document.getElementById('check-edad');

        // Función para calcular la edad
        function calcularEdad(fechaNacimiento) {
            const hoy = new Date();
            const fechaNac = new Date(fechaNacimiento);
            let edad = hoy.getFullYear() - fechaNac.getFullYear();
            const mes = hoy.getMonth() - fechaNac.getMonth();

            // Ajustar si el cumpleaños de este año aún no ha pasado
            if (mes < 0 || (mes === 0 && hoy.getDate() < fechaNac.getDate())) {
                edad--;
            }
            return edad;
        }

        // Función para validar y habilitar/deshabilitar el botón
        function validarEdad() {
            const fechaNacimiento = fechaNacimientoInput.value;
            if (fechaNacimiento) {
                const edad = calcularEdad(fechaNacimiento);
                if (edad >= 18) {
                    botonProcesar.disabled = false;
                } else {
                    botonProcesar.disabled = true;
                }
            } else {
                // Si el campo de fecha está vacío, el botón debe estar deshabilitado
                botonProcesar.disabled = true;
            }
        }

        // Deshabilita el botón al cargar la página por primera vez
        botonProcesar.disabled = true;

        // Añade un "listener" al campo de fecha de nacimiento para detectar cambios
        fechaNacimientoInput.addEventListener('change', validarEdad);
    });
