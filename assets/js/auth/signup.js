import axios from 'axios';
import formHandler from '../utils/formHandler';

import { signupConstraint } from'./dataContraints'

export const signup = (selector) => {
    let state = {
        first_name: '',
        last_name: '',
        email: '',
        password: '',
        confirm_password: ''
    };

    const handleSubmit = state => {
        console.log(state);
    };

    formHandler(selector, signupConstraint, state, handleSubmit);

};
