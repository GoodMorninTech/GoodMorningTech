let totalSteps = document.getElementById('totalSteps');
let currentStep = document.getElementById('currentStep');

let email = document.getElementById('userEmail');
let name = document.getElementById('username');
let displayName = document.getElementById('displayName');

let stepOne = document.getElementById('stepOne');
let stepOneBtn = document.getElementById('nextBtnStepOne');

stepOneBtn.addEventListener('click', function () {
    if (email.value == '' || name.value == '' || displayName.value == '') {
        if (email.value == '') {
            email.classList.add('border-red-500', 'border-2');
        }
        if (name.value == '') {
            name.classList.add('border-red-500', 'border-2');
        }
        if (displayName.value == '') {
            displayName.classList.add('border-red-500', 'border-2');
        }
    } else {
        stepOne.classList.add('hidden');
        stepTwo.classList.remove('hidden');
        currentStep.textContent = 2;
    }
});

email.addEventListener('blur', function () {
    email.classList.remove('border-red-500', 'border-2');
});
name.addEventListener('blur', function () {
    name.classList.remove('border-red-500', 'border-2');
});
displayName.addEventListener('blur', function () {
    displayName.classList.remove('border-red-500', 'border-2');
});

email.addEventListener('keyup', function () {
    if (email.value.includes('@') && email.value.includes('.')) {
        email.classList.remove('border-red-500', 'border-2');
        email.classList.add('border-green-500', 'border-2');
    } else {
        email.classList.remove('border-green-500', 'border-2');
        email.classList.add('border-red-500', 'border-2');
    }
});

let goBackBtnStepTwo = document.getElementById('backBtnStepTwo');
let stepTwoBtn = document.getElementById('nextBtnStepTwo');
let stepTwo = document.getElementById('stepTwo');

let password = document.getElementById('password');
let repeatPassword = document.getElementById('repeatPassword');

goBackBtnStepTwo.addEventListener('click', function () {
    stepTwo.classList.add('hidden');
    stepOne.classList.remove('hidden');
    currentStep.textContent = 1;
});

stepTwoBtn.addEventListener('click', function () {
    if (password.value == '' || repeatPassword.value == '') {
        if (password.value == '') {
            password.classList.add('border-red-500', 'border-2');
        }
        if (repeatPassword.value == '') {
            repeatPassword.classList.add('border-red-500', 'border-2');
        }
    } else {
        if (password.value == repeatPassword.value) {
            stepTwo.classList.add('hidden');
            stepThree.classList.remove('hidden');
            currentStep.textContent = 3;
        } else {
            password.classList.add('border-red-500', 'border-2');
            repeatPassword.classList.add('border-red-500', 'border-2');
            window.alert('Your passwords do not match!');
        }
    }
});

password.addEventListener('blur', function () {
    password.classList.remove('border-red-500', 'border-2');
});

repeatPassword.addEventListener('blur', function () {
    repeatPassword.classList.remove('border-red-500', 'border-2');
});

let goBackBtnStepThree = document.getElementById('backBtnStepThree');
let stepThree = document.getElementById('stepThree');

goBackBtnStepThree.addEventListener('click', function () {
    stepThree.classList.add('hidden');
    stepTwo.classList.remove('hidden');
    currentStep.textContent = 2;
});

let submitFormBtn = document.getElementById('submitFormBtn');
let aboutMe = document.getElementById('aboutMe');
let timezone = document.getElementById('timezone');
let checkbox = document.getElementById('terms');

// if (aboutMe.value == '' && checkbox.checked == false) {
//     submitFormBtn.disabled = true;
// } else {
//     submitFormBtn.disabled = false;
// }
// @LevaniVashadze Could you fix this, it must only enable the button if the checkbox is checked and the textarea is not empty...