import {
    signup,
    verify_email,
} from './auth';
document.addEventListener("DOMContentLoaded", function () {

    if (document.querySelector('form')) {

        const formClasses = [...document.querySelector('form').classList];

        switch (formClasses.join('.')) {
            case 'form.signup':
                signup('form.signup');
                break;
            case 'form.check-email':
                verify_email('form.check-email');
                break;
            default:
                return ''
        }
    }
});
