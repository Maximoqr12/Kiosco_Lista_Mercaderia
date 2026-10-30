
document.addEventListener("DOMContentLoaded", () => {
    const formularios = document.querySelectorAll("form[data-confirm]");

    formularios.forEach((formulario) => {
        formulario.addEventListener("submit", (evento) => {
            const mensaje =
                formulario.dataset.confirm ||
                "¿Confirmás esta acción?";

            if (!window.confirm(mensaje)) {
                evento.preventDefault();
            }
        });
    });
});
