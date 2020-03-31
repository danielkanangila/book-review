import axios from 'axios';
import formHandler from '../utils/formHandler';
import { alert } from './../components';

import { signupConstraint } from'./dataContraints'

export const signup = (selector) => {
    let state = {
        first_name: '',
        last_name: '',
        email: '',
        password: '',
        confirm_password: ''
    };

    const handleError = (wrapperSelector, message, remove = false) => {
        const wrapper = document.querySelector(selector);
        const alertEl = alert('danger', message);
        if (wrapper.querySelector('.alert') && remove === true) {
            wrapper.querySelector('.alert').remove();
            return;
        }
        if (message) wrapper.querySelector('h2.form-title').after(alertEl);
    };

    const handleSubmit = (state) => {
        handleError(selector, '', true);
        if (state) {
            const {confirm_password, ...data} = state;

            axios.post('/signup', data)
                .then(response => {
                    console.log(response);
                })
                .catch(error => {
                    handleError(selector, error.response.data.error);
                });
        }
    };

    formHandler(selector, signupConstraint, state, handleSubmit);
};
