// nombre
const firstnameField = document.querySelector("#firstnameField");

// apellido
const lastnameField = document.querySelector("#lastnameField");

// boton de confirmacion
const submitBtn = document.querySelector("#submitButton");

firstnameField.addEventListener("keyup", (e) => {
    e.preventDefault();

    const firstnameVal = e.target.value;

    submitBtn.disabled = true;
    firstnameField.classList.remove("is-invalid");
    submitBtn.removeAttribute("disabled");
    if (firstnameVal.length > 0) {
        fetch("/validate-username", {
            body: JSON.stringify({ first_name: firstnameVal }),
            method: "POST",
        })
            .then((res) => res.json())
            .then((data) => {
                // console.log("data", data)
                if (data.username_error) {
                    firstnameField.classList.add("is-invalid");
                    submitBtn.disabled = true;
                }            
            });
    }
});

lastnameField.addEventListener("keyup", (e) => {
    e.preventDefault();

    const lastnameVal = e.target.value;

    lastnameField.classList.remove("is-invalid");
    submitBtn.removeAttribute("disabled");
    if (lastnameVal.length > 0) {
        fetch("/validate-lastname", {
            body: JSON.stringify({ last_name: lastnameVal }),
            method: "POST",
        })
            .then((res) => res.json())
            .then((data) => {
                // console.log("data", data)
                if (data.lastname_error) {
                    lastnameField.classList.add("is-invalid");
                    submitBtn.disabled = true;
                }
            });
    }
});

