const counter = document.querySelector(".slider-counter");
const slider = document.querySelector(".slider");

counter.innerHTML = `Count: ${slider.value} articles`;
slider.oninput = function() {
    counter.innerHTML = `Count: ${this.value} articles`;
}

const checkbox_input_div = document.querySelector(".days-input");

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
email.addEventListener("input", function() {
    if (email.validity.typeMismatch) {
        email.style.borderColor = "#F43434";
    } else if (email.validity.valueMissing) {
        email.style.borderColor = "#ffb300";
    } else {
        email.style.borderColor = "#62A539";
    }
});

//Creating a function to return users IP address using ipify API and then using that IP address to get the timezone abbreivation of the user using worldtimeapi api and then using that timezone abbreivation to select the option in the document which has the same class as the timezone abbreivation
// fetch("https://api.ipify.org/?format=json")
//     .then(response => response.json())
//     .then(data => {
//         fetch(`http://worldtimeapi.org/api/ip/${data.ip}`)
//             .then(response => response.json())
//             .then(data => {
//                 const timezone = data.abbreviation;
//                 console.log(timezone);
//                 const timezone_option = document.querySelector(`.${timezone}`);
//                 timezone_option.selected = true;
//             })
// })

let ip;

const API = async () => {
    const IP = await fetch("https://api.ipify.org/?format=json");
    const IP_data = await IP.json();
    ip = IP_data.ip;
    return ip;
}


let timezone_abbr;

const timezone = async () => {
    const ip = await API();
    const timezone_data = await fetch(`https://worldtimeapi.org/api/ip/${ip}`);
    const timezone_data_json = await timezone_data.json();
    timezone_abbr = timezone_data_json.abbreviation;
    return timezone_abbr;
}

document.addEventListener("DOMContentLoaded", function() {
    timezone().then(timezone_abbr => {
        const timezone_option = document.querySelector(`.${timezone_abbr}`);
        timezone_option.selected = true;
    })
})
