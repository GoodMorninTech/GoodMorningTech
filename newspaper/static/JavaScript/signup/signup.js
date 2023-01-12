const email = document.getElementById('email');

email.addEventListener("input", function(event) {
    if (email.validity.typeMismatch) {
        email.style.borderColor = "#F43434";
    } else if (email.validity.valueMissing) {
        email.style.borderColor = "#ffb300";
    } else {
        email.style.borderColor = "#62A539";
    }
});

const everyday = document.getElementById('everyday');
const weekend = document.getElementById('weekend');
const weekday = document.getElementById('weekday');