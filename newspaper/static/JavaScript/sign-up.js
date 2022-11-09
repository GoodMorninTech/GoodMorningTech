const counter = document.querySelector(".slider-counter");
const slider = document.querySelector(".slider");

counter.innerHTML = `Count: ${slider.value} articles`;
slider.oninput = function() {
    counter.innerHTML = `Count: ${this.value} articles`;
}

const checkbox_input_div = document.querySelector(".days-input");
const checkbox_input = document.querySelector(".checkbox");

//Making sure that only 1 out 3 checkboxes can be selected in the document at any time
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

//Making sure that the email input is not empty
const email = document.querySelector(".email-address");
email.addEventListener("input", function(event) {
    if (email.validity.typeMismatch) {
        email.style.borderColor = "#F43434";
    } else if (email.validity.valueMissing) {
        email.style.borderColor = "#f2f2f2";
    } else {
        email.style.borderColor = "#62A539";
    }
});

//Checking if email already exists in the database, if it does, then the email border color will turn yellow
