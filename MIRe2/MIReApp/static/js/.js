/*
VIEW IN FULL SCREEN MODE
FULL SCREEN MODE: http://salehriaz.com/404Page/404.html

DRIBBBLE: https://dribbble.com/shots/4330167-404-Page-Lost-In-Space
*/
<script>
    document.addEventListener("DOMContentLoaded", function() {
        const eliminarButtons = document.querySelectorAll(".eliminar-btn");
        
        eliminarButtons.forEach(button => {
            button.addEventListener("click", function() {
                const historialId = this.getAttribute("data-id");
                
                if (confirm("¿Estás seguro de que deseas eliminar este registro?")) {
                    // Realizar la solicitud AJAX para eliminar el historial
                    fetch(`/eliminar_historial_metrica/${historialId}/`, {
                        method: "POST",
                        headers: {
                            "X-CSRFToken": "{{ csrf_token }}",
                            "Content-Type": "application/json"
                        }
                    })
                    .then(response => response.json())
                    .then(data => {
                        // Eliminar la fila de la tabla en la página
                        if (data.success) {
                            const fila = this.closest("tr");
                            fila.remove();
                        }
                    })
                    .catch(error => {
                        console.error("Error:", error);
                    });
                }
            });
        });
    });
</script>