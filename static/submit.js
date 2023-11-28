const menu1 = document.querySelector("#menu1") // No Condition
const menu2 = document.querySelector("#menu2") // Vegetarian
const menu3 = document.querySelector("#menu3") // Vegan
const menu4 = document.querySelector("#menu4") // Celiac

const successModal = new bootstrap.Modal(document.querySelector("#successModal"), {
    keyboard: false
})

const errorModal = new bootstrap.Modal(document.querySelector("#errorModal"), {
    keyboard: false
})

const successModalMessage = document.querySelector("#successModalMessage");
const errorModalMessage = document.querySelector("#errorModalMessage");

document.querySelector("#mainForm").addEventListener("submit", function(e){
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
    formData.append('last_name', last_name);
    formData.append('menu', menu);
    formData.append('csrfmiddlewaretoken', '{{ csrf_token }}');
    
    fetch("", {
        method: 'POST',
        body: formData
    })
    .then((response) => response.json())
    .then((data) => {
        if (data.username_error) {
            submitBtn.setAttribute("disabled", "");
            errorModalMessage.innerHTML = `<p class="modal-title">${data.username_error}</p><span aria-hidden="true">&#9940;</span>`
            errorModal.show()
            firstnameField.value = "";
            lastnameField.value = "";

            menu1.checked = false;
            menu2.checked = false;
            menu3.checked = false;
            menu4.checked = false;

            setTimeout(function(){
                errorModal.hide()
            }, 2000)
        } else {
            successModalMessage.innerHTML = `<p class="modal-title">${data.username_success}</p><span aria-hidden="true">&#9989;</span>`
            successModal.show()
            firstnameField.value = "";
            lastnameField.value = "";

            menu1.checked = false;
            menu2.checked = false;
            menu3.checked = false;
            menu4.checked = false;

            setTimeout(function(){
                successModal.hide()
            }, 2000)
        }

    })
    .catch(error => {
        console.error('Error:', error);
    })
});