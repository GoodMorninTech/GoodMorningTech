const slider = document.querySelector(".slider");
const counter = document.querySelector(".counter");
counter.innerHTML = `COUNT: ${slider.value} ARTICLES`;
slider.oninput = function() {
    counter.innerHTML = `COUNT: ${this.value} ARTICLES`;
}

const email = document.querySelector(".email-address");
//Checking if email is entered correctly, if it is not, turns to #F43434, if it is left empty then default and if correct then green
email.addEventListener("input", function(event) {
    if (email.validity.typeMismatch) {
        email.style.borderColor = "#F43434";
    } else if (email.validity.valueMissing) {
        email.style.borderColor = "#f2f2f2";
    } else {
        email.style.borderColor = "#62A539";
    }
});
//Checking if form is submitted correctly, if it is not, then mark the missing fields red
const form = document.querySelector("form");
form.addEventListener("submit", function(event) {
    if (!email.validity.valid) {
        email.style.borderColor = "#F43434";
        event.preventDefault();
    }
});
