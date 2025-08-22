    document.addEventListener('DOMContentLoaded', function() {
        const loteSelect = document.getElementById('id_lote');
        const simcardSelect = document.getElementById('id_simcard');
        var urlAjaxTemplate = ""
        // Generar la URL de Django directamente en el script
        const ajaxUrl = urlAjaxTemplate;
        loteSelect.addEventListener('change', function() {
            const loteId = this.value;
            
            simcardSelect.innerHTML = '<option value="">--- Seleccione una SIM Card ---</option>';
            simcardSelect.disabled = true;
            
            if (loteId) {
                const fetchUrl = `${ajaxUrl}?lote_id=${loteId}`;
                fetch(fetchUrl)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('La respuesta de la red no fue exitosa');
                    }
                    return response.json();
                    })
                    .then(data => {
                        data.simcards.forEach(simcard => {
                            const option = document.createElement('option');
                            option.value = `${simcard.id}`;
                            option.textContent = `${simcard.codigo} | ${simcard.estado}`;
                            simcardSelect.appendChild(option);
                        });
                        simcardSelect.disabled = false;
                    })
                    .catch(error => {
                        console.error('Error al cargar las SIM Cards:', error);
                        alert('No se pudieron cargar las SIM Cards. Intente de nuevo.');
                    });
            }
        });
    });
