////////////////////////////////////////////////////////////////////////////////
//                               HTMX                                         //
////////////////////////////////////////////////////////////////////////////////

// Add CSRF token to every HTMX requests
document.body.addEventListener('htmx:configRequest', (event) => {
    var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    event.detail.headers['X-CSRFToken'] = csrfToken;
});