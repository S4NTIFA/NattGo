document.addEventListener("DOMContentLoaded", function () {
    const email = document.getElementById("email")
    const form = document.getElementById("form")
    const parrafo = document.getElementById("warnings")

    form.addEventListener("submit", e => {
        e.preventDefault()
        let warnings = ""
        let entrar = false
        let regexEmail = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/
        parrafo.innerHTML = ""

        email.classList.remove("error-input");

        if (!regexEmail.test(email.value)) {
            warnings += "El email no es válido <br>";
            email.classList.add("error-input");
            entrar = true;
        }
        if (entrar) {
            parrafo.innerHTML = warnings;
        } else {
            alert("Se ha registrado correctamente");
            form.reset();
        }
    });
});