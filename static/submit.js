// opciones de menu (botones radio)
const menu1 = document.querySelector("#menu1") // Sin Condicion
const menu2 = document.querySelector("#menu2") // Vegetariano
const menu3 = document.querySelector("#menu3") // Vegano
const menu4 = document.querySelector("#menu4") // Celiaco

// modal exito
const miModalSuccess = new bootstrap.Modal(document.querySelector("#modalExito"), {
    keyboard: false
})

// modal error
const miModalError = new bootstrap.Modal(document.querySelector("#modalError"), {
    keyboard: false
})

// mensaje de modal exito
const mensajeModalExito = document.querySelector("#modalSucc");

// mensaje de modal error
const mensajeModalError = document.querySelector("#modalErr");

document.querySelector("#inviform").addEventListener("submit", function(e){
    e.preventDefault();

    first_name = firstnameField.value;
    last_name = lastnameField.value;
    let menu;

    if (menu1.checked) {
        menu = menu1.value;
    } else if (menu2.checked) {
        menu = menu2.value;
    } else if (menu3.checked) {
        menu = menu3.value;
    } else if (menu4.checked) {
        menu = menu4.value;
    } else {
        menu = 'none'
    }

    const formData = new FormData();
    
    formData.append('first_name', first_name);
    formData.append('last_name', last_name)
    formData.append('menu', menu);
    formData.append('csrfmiddlewaretoken', '{{ csrf_token }}');
    /* console.log(formData); */

    
    fetch("", {
        method: 'POST',
        body: formData
    })
    .then((response) => response.json())
    .then((data) => {
        if (data.username_error) {
            submitBtn.setAttribute("disabled", "");
            mensajeModalError.innerHTML = `<p class="modal-title" style="font-weight: 500;">${data.username_error}</p> 
                                                            <span aria-hidden="true">&#9940;</span>`
            miModalError.show()
            firstnameField.value = "";
            lastnameField.value = "";

            menu1.checked = false;
            menu2.checked = false;
            menu3.checked = false;
            menu4.checked = false;

            setTimeout(function(){
                miModalError.hide()
            }, 2000)
        } else {
            mensajeModalExito.innerHTML = `<p class="modal-title" style="text-align: center; font-weight: 500;">${data.username_success} &#128515;</p>
                                                                <span aria-hidden="true">&#9989;</span>`
            miModalSuccess.show()
            firstnameField.value = "";
            lastnameField.value = "";

            menu1.checked = false;
            menu2.checked = false;
            menu3.checked = false;
            menu4.checked = false;

            setTimeout(function(){
                miModalSuccess.hide()
            }, 2000)
        }

    })
    .catch(error => {
        console.error('Error:', error);
    })
});