import {alert, error} from '../components';
import {validator} from "./validate";

/**
 * add errors to the dom if inputs values are not valid.
 * @param {*} errors list errors message
 * */
export const addErrorsToDOM = errors => {
    Object.entries(errors).forEach((__error) => {
        // Retrieve input element with error
        const inputEl = document.querySelector(`input[name=${__error[0]}]`);
        // Set error class to the element
        inputEl.classList.add('error');
        // Retrieve parent of input element
        const parentEl = inputEl.parentElement;

        // Append error span with message at the bottom of the input
        parentEl.append(error(__error[0], __error[1]));
    })
};

/**
 *
 * @param currentField input element
 * @param fieldName name of attribute name on input
 * @param message error message
 */
export const addSingleError = (currentField, fieldName, message) => {
    // Select parent of input element
    const parentEl = currentField.parentElement;

    // Append error span with message at the bottom of the input.
    parentEl.append(error(fieldName, message));
};

/**
 * Remove all error element to the form
 */
export const removeAllError = () => {
    const errors = document.querySelectorAll('span.error');
    const inputs = document.querySelectorAll('input');
    if (errors) {
        errors.forEach(error => error.remove());
    }
    inputs.forEach(input => input.classList.remove('error'))
};

/**
 * Handle error span element if input is valid
 * @param constraints object for form validation
 * @param field current form field
 * @param value current form field value
 */
export const handleSingleError = (constraints, field, value) => {
    // select current input filed
    const inputEl = document.querySelector(`input[name=${field}]`);

    // Select span error element
    const errorEl = document.querySelector(`#${field}`);
    // Build single constraint for validation
    const constraint = {[field]: constraints[field]};

    // Format data for validation
    let data;
    if (field === 'confirm_password') {
        const password = document.querySelector('input[name=password]').value;
        data = {
            [field]: value,
            password
        }
    } else {
        data = {[field]: value};
    }

    // validate value
    const errorMessage = validator(data, constraint);

    // remove error span and error class to the input if exist and if value is valid.
    if (errorEl && !errorMessage) {
        removeError(inputEl, errorEl)
    } else {
        if (errorEl) removeError(inputEl, errorEl);
        if (errorMessage) {
            inputEl.classList.add('error');
            addSingleError(inputEl, field, errorMessage[field][0])
        }
    }
};

/**
 * Remove error span and error class on input
 * @param inputEl
 * @param errorSpan
 */
export const removeError = (inputEl, errorSpan) => {
    inputEl.classList.remove('error');
    errorSpan.remove();
};


/**
 * Added alert message to the DOM
 * @param wrapper
 * @param message
 * @param remove
 */
export const handleError = (wrapper, message, remove = false) => {

        const alertEl = alert('danger', message);
        if (wrapper.querySelector('.alert') && remove === true) {
            wrapper.querySelector('.alert').remove();
            return;
        }
        if (message) wrapper.querySelector('h2.form-title').after(alertEl);
};