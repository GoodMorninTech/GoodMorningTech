const counter = document.querySelector(".slider-counter");
const slider = document.querySelector(".slider");

counter.innerHTML = `Count: ${slider.value} articles`;
slider.oninput = function() {
    counter.innerHTML = `Count: ${this.value} articles`;
}

const checkbox_input_div = document.querySelector(".days-input");
const checkbox_input = document.querySelector(".checkbox");

checkbox_input_div.addEventListener("click", function(e) {
    if (e.target.type === "checkbox") {
        const checkboxes = document.querySelectorAll(".checkbox");
        checkboxes.forEach(checkbox => {
            if (checkbox !== e.target) {
                checkbox.checked = false;
            }
        })
    }
})

const email = document.querySelector(".email-address");
email.addEventListener("input", function(event) {
    if (email.validity.typeMismatch) {
        email.style.borderColor = "#F43434";
    } else if (email.validity.valueMissing) {
        email.style.borderColor = "#ffb300";
    } else {
        email.style.borderColor = "#62A539";
    }
});
