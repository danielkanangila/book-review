import {
    validator,
    addErrorsToDOM,
    removeAllError,
    handleSingleError
} from '../utils';
import {signupConstraint} from "../auth/dataContraints";

/**
 *
 * @param selector from selector
 * @param dataValidationConstraint constraint to validate inputs
 * @param state object representing the form data
 * @param submitHandler callback function to handle form submit
 * @param changeHandler callback function to handle input change event
 */
const formEventHandler = (selector, dataValidationConstraint, state, submitHandler, changeHandler,) => {
    const form = document.querySelector(selector);
    const inputs = form.querySelectorAll('input');
    const submitBtn = form.querySelector("button");

    /** Handle inputs change event and pass the
     * target value and name to callback handle change event
     * @param event
     * */
    const handleChange = event => {
        state = {
            ...state,
            [event.target.name]: event.target.value
        };
        if (changeHandler) {
            changeHandler(event.target.name, event.target.value);
        }
        handleSingleError(dataValidationConstraint, event.target.name, event.target.value)
    };

    /**
     * Handle form submit event and pass to the callback function
     * state when successful validate data
     * @param event
     */
    const handleSubmit = event => {
        event.preventDefault();
        removeAllError();
        const errors = validator(state, signupConstraint);
        if (errors) {
            addErrorsToDOM(errors);
        } else {
            submitHandler(state, event);
        }
    };

    // Bind "keyup  and change" event on all inputs in the selected form
    inputs.forEach(input => input.addEventListener('keyup', handleChange));
    inputs.forEach(input => input.addEventListener('change', handleChange));

    // bind click event handler to form submit
    submitBtn.addEventListener('click', handleSubmit);
};

export default formEventHandler;