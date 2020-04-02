import {
    signup,
    verify_email,
    login
} from './auth';
import navbar from './navbar';

document.addEventListener("DOMContentLoaded", function () {
    const location = window.location.pathname;

    // Handle navbar components:
    // open and close sidenav, handle logout
    navbar();

    // Added class 'auth-process' to current page and hide navbar and footer
    if (location === '/signup' || location === '/login') document.body.classList.add('auth-process');
    else document.body.classList.remove('auth-process');

    // Forms handler
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
