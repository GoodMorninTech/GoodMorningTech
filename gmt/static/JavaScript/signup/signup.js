const email = document.getElementById('email');
const sources = document.getElementById('source-list');

email.addEventListener("input", function (event) {
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
    toggleButton();
})

sources.addEventListener("change", () => {
        toggleButton();
    }
)

const toggleButton = () => {
    let check_amount = 0;
    for (let i = 0; i < sources.children.length; i++) {
        if (sources.children[i].children[0].checked) {
            check_amount++;
        }
    }
    document.getElementById("subscribeButton").disabled = check_amount < 3;
    if (document.getElementById("subscribeButton").disabled) {
        document.getElementById("button-tooltip").style.display = "block";
    } else {
        document.getElementById("button-tooltip").style.display = "none";
    }
}
