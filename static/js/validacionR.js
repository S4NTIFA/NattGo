document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("form");
    const parrafo = document.getElementById("warnings");

    form.addEventListener("submit", function (e) {
        e.preventDefault();
        let warnings = "";
        let entrar = false;
        let regexEmail = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
        parrafo.innerHTML = "";

        const nombre = document.getElementById("nombre");
        const apellidos = document.getElementById("apellidos");
        const email = document.getElementById("correo");
        const telefono = document.getElementById("telefono");
        const fechaNacimiento = document.getElementById("fechanacimientousuario");
        const pass = document.getElementById("password");
        const confirmPass = document.getElementById("confirm-password");

        nombre.classList.remove("error-input");
        apellidos.classList.remove("error-input");
        email.classList.remove("error-input");
        telefono.classList.remove("error-input");
        fechaNacimiento.classList.remove("error-input");
        pass.classList.remove("error-input");
        confirmPass.classList.remove("error-input");

        if (nombre.value.length < 2) {
            warnings += "El nombre no es válido <br>";
            nombre.classList.add("error-input");
            entrar = true;
        }

        if (apellidos.value.length < 2) {
            warnings += "Los apellidos no son válidos <br>";
            apellidos.classList.add("error-input");
            entrar = true;
        }

        if (!regexEmail.test(email.value)) {
            warnings += "El email no es válido <br>";
            email.classList.add("error-input");
            entrar = true;
        }

        if (telefono.value.length < 6) {
            warnings += "El teléfono no es válido <br>";
            telefono.classList.add("error-input");
            entrar = true;
        }

        if (fechaNacimiento.value === "") {
            warnings += "La fecha de nacimiento es requerida <br>";
            fechaNacimiento.classList.add("error-input");
            entrar = true;
        }

        if (pass.value.length < 8) {
            warnings += "La contraseña no es válida <br>";
            pass.classList.add("error-input");
            entrar = true;
        }

        if (pass.value !== confirmPass.value) {
            warnings += "Las contraseñas no coinciden <br>";
            pass.classList.add("error-input");
            confirmPass.classList.add("error-input");
            entrar = true;
        }

        if (entrar) {
            parrafo.innerHTML = warnings;
        } else {
            form.submit();
        }
    });
});
