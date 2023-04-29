let totalSteps = document.getElementById('totalSteps');
let currentStep = document.getElementById('currentStep');

let email = document.getElementById('userEmail');
let contact = document.getElementById('userContact');
let displayName = document.getElementById('username');

let stepOne = document.getElementById('stepOne');
let stepOneBtn = document.getElementById('nextBtnStepOne');

const progressBar = document.getElementById('progressBar');

stepOneBtn.addEventListener('click', function () {
    if (email.value === '' || contact.value === '' || displayName.value === '') {
        if (email.value === '') {
            email.classList.add('border-red-500', 'border-2');
        }
        if (contact.value === '') {
            contact.classList.add('border-red-500', 'border-2');
        }
        if (displayName.value === '') {
            displayName.classList.add('border-red-500', 'border-2');
        }
    } else {
        stepOne.classList.add('hidden');
        stepTwo.classList.remove('hidden');
        currentStep.textContent = 2;
        progressBar.classList.remove('w-1/3');
        progressBar.classList.add('w-2/3');
    }
});

email.addEventListener('blur', function () {
    email.classList.remove('border-red-500', 'border-2');
});
contact.addEventListener('blur', function () {
    contact.classList.remove('border-red-500', 'border-2');
});
displayName.addEventListener('blur', function () {
    displayName.classList.remove('border-red-500', 'border-2');
});

const checkEmail = () => {
    if (email.value.includes('@') && email.value.includes('.')) {
        email.classList.remove('border-red-500', 'border-2');
        email.classList.add('border-green-500', 'border-2');
    } else {
        email.classList.remove('border-green-500', 'border-2');
        email.classList.add('border-red-500', 'border-2');
    }
}
email.addEventListener('click', checkEmail);
email.addEventListener('input', checkEmail);
email.addEventListener('blur', checkEmail);

let goBackBtnStepTwo = document.getElementById('backBtnStepTwo');
let stepTwoBtn = document.getElementById('nextBtnStepTwo');
let stepTwo = document.getElementById('stepTwo');

let whyWrite = document.getElementById('whyWrite');
let topics = document.getElementById('topics');

goBackBtnStepTwo.addEventListener('click', function () {
    stepTwo.classList.add('hidden');
    stepOne.classList.remove('hidden');
    currentStep.textContent = 1;
    progressBar.classList.remove('w-2/3');
    progressBar.classList.add('w-1/3');
});

stepTwoBtn.addEventListener('click', function () {
    if (whyWrite.value === '' || topics.value === '') {
        if (whyWrite.value === '') {
            whyWrite.classList.add('border-red-500', 'border-2');
        }
        if (topics.value === '') {
            topics.classList.add('border-red-500', 'border-2');
        }
    } else {
        stepTwo.classList.add('hidden');
        stepThree.classList.remove('hidden');
        currentStep.textContent = 3;
        progressBar.classList.remove('w-2/3');
        progressBar.classList.add('w-full');
        }
    }
);

whyWrite.addEventListener('blur', function () {
    whyWrite.classList.remove('border-red-500', 'border-2');
});

topics.addEventListener('blur', function () {
    topics.classList.remove('border-red-500', 'border-2');
});

let goBackBtnStepThree = document.getElementById('backBtnStepThree');
let stepThree = document.getElementById('stepThree');

goBackBtnStepThree.addEventListener('click', function () {
    stepThree.classList.add('hidden');
    stepTwo.classList.remove('hidden');
    currentStep.textContent = 2;
    progressBar.classList.remove('w-full');
    progressBar.classList.add('w-2/3');
});

let submitFormBtn = document.getElementById('submitFormBtn');
let sample = document.getElementById('sample');
let article = document.getElementById('article');
let checkbox = document.getElementById('terms');

const checkButton = () => {
    submitFormBtn.disabled = article.value === '' || checkbox.checked === false;
}

document.addEventListener('DOMContentLoaded', checkButton);
article.addEventListener('input', checkButton);
checkbox.addEventListener('click', checkButton);

