import { signup } from './auth';
document.addEventListener("DOMContentLoaded", function () {

    const signupForm = document.querySelector('form.signup');
    if (signupForm) {
        signup('form.signup');
    }
});
