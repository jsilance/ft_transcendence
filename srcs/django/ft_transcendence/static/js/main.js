// Toggle navbar dropdown menu  
let dropdown_menu = document.getElementById("dropdown_menu")

function toggleMenu() {
    dropdown_menu.classList.toggle("open_menu");
}

function blockUnblock(id, action) {
    var url = "/accounts/blocking?user_id=738784&action=892893".replace(738784, id).replace(892893, action)
    $.ajax({
        type: "GET",
        dataType: "json",
        url: url,
        timaout: 5000,
        success: function(data) {
            console.log(data['response'], 'Success');
        },
        error: function(data) {
            // alert(data['response'], 'Error');
        },
        complete: function(data) {
            console.log(data['response'], 'Complete')
            location.reload()
        },
    })
}

document.body.addEventListener('htmx:configRequest', (event) => {
    // Add the CSRF token to htmx requests
    var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    event.detail.headers['X-CSRFToken'] = csrfToken;
});