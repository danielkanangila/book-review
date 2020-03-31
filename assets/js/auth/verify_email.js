import axios from '../utils/formHandler';
import formHandler from '../utils/formHandler';

export const verify_email = (selector) => {
    let token = '';
    const formEl = document.querySelector(selector);
    const inputs = formEl.querySelectorAll('input');
    const submitBtn = formEl.querySelector("button");

    inputs[0].focus();

    submitBtn.disabled = true;

    const moveCursor = (currentEl, nextId) => {
        const length = currentEl.value.length;
        const maxLength = currentEl.getAttribute('maxlength');

        if (length == maxLength) {
            if (nextId !== 'n6') {
                document.getElementById(nextId).focus();
                token += currentEl.value;
                console.log(token)
            } else {
                 submitBtn.disabled = false;
                if (token.length < 5) {
                     token += currentEl.value
                } else {
                }

            }
        }
    };

    const checkToken = (e) => {
        e.preventDefault();
    };

    inputs.forEach((input, i) => input.addEventListener('keyup', event => moveCursor(event.target, `n${i+2}`)));
    submitBtn.addEventListener('click', checkToken)
};