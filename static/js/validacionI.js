document.addEventListener("DOMContentLoaded", function () {
    const email = document.getElementById("email");
    const pass = document.getElementById("password");
    const form = document.getElementById("form");
    const parrafo = document.getElementById("warnings");
  
    form.addEventListener("submit", function (e) {
      let warnings = "";
      let entrar = false;
      let regexEmail = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
      parrafo.innerHTML = "";
  
     
      email.classList.remove("error-input");
      pass.classList.remove("error-input");
  
      if (!regexEmail.test(email.value)) {
        warnings += "El email no es válido <br>";
        email.classList.add("error-input");
        entrar = true;
      }
  
      if (pass.value.length < 8) {
        warnings += "La contraseña no es válida <br>";
        pass.classList.add("error-input");
        entrar = true;
      }
  
      if (entrar) {
        e.preventDefault();
        parrafo.innerHTML = warnings;
      } else {
        parrafo.innerHTML = "Enviado";
      }
    });
  });
  