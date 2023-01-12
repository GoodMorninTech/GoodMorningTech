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

//Ensuring only one of the three is selected at any one time
everyday.addEventListener("click", function(event) {
    if (everyday.checked) {
        weekend.checked = false;
        weekday.checked = false;
    }
});

weekend.addEventListener("click", function(event) {
    if (weekday.checked) {
        weekday.checked = false;
        everyday.checked = false;
    }
});

weekday.addEventListener("click", function(event) {
    if (weekday.checked) {
        weekend.checked = false;
        everyday.checked = false;
    }
});