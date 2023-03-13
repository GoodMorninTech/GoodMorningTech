const email = document.getElementById('email');

email.addEventListener("input", function(event) {
    if (email.validity.typeMismatch) {
        email.style.borderColor = "#F43434";
    } else if (email.validity.valueMissing) {
        email.style.borderColor = "#ffb300";
    } else {
        email.style.borderColor = "#15803d";
    }
});

document.addEventListener("DOMContentLoaded", () => {
    document.getElementById(Intl.DateTimeFormat().resolvedOptions().timeZone)
        .setAttribute("selected", "selected");
})