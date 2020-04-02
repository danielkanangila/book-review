import {
    signup,
    verify_email,
    login
} from './auth';
document.addEventListener("DOMContentLoaded", function () {

    if (document.querySelector('form')) {

        const formClasses = [...document.querySelector('form').classList];
        const fromSelector = formClasses.join('.');
        switch (fromSelector) {
            case 'form.signup':
                signup('form.signup');
                break;
            case 'form.check-email':
                verify_email('form.check-email');
                break;
            case 'form.login':
                login(fromSelector);
                break;
            default:
                return ''
        }
    }
});
