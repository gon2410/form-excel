/* password */
const passwd = document.querySelector("#passwordField")
const excelSubmit = document.querySelector("#downloadButton")

window.addEventListener('load', () => {
    excelSubmit.disabled = true;
})

passwd.addEventListener("keyup", (e) => {
    const passwordVal = e.target.value;

    passwd.classList.remove("is-invalid");
    passwd.classList.remove("is-valid");
    
    excelSubmit.disabled = true;
    if (passwordVal.length > 0) {
        fetch("/validate-password", {
            body: JSON.stringify({ password: passwordVal }),
            method: "POST",
        })
            .then((res) => res.json())
            .then((data) => {
                if (data.password_error) {
                    passwd.classList.add("is-invalid");
                    excelSubmit.disabled = true;
                } else if (data.password_valid) {
                    passwd.classList.remove("is-invalid")
                    passwd.classList.add("is-valid")
                    excelSubmit.removeAttribute("disabled");
                    // passwd.value = "";
                }
            })
    }
});