import axios from 'axios';
import formHandler from '../utils/formHandler';
import { handleError } from '../utils';

import { signupConstraint } from'./dataContraints'

export const signup = ({$this, location}) => {
    let state = {
        first_name: '',
        last_name: '',
        email: '',
        password: '',
        confirm_password: ''
    };

    const handleSubmit = (state) => {

        document.querySelector('.loader-wrapper').classList.remove('hide');
        handleError($this, '', true);
        if (state) {
            const {confirm_password, ...data} = state;

            axios.post('/signup', data)
                .then(response => {
                    document.querySelector('.loader-wrapper').classList.add('hide');
                    localStorage.setItem('access_token', response.data.access_token);
                    location.replace('/');
                })
                .catch(error => {
                    document.querySelector('.loader-wrapper').classList.add('hide');
                    handleError($this, error.response.data.error);
                });
        }
    };

    formHandler($this, signupConstraint, state, handleSubmit);
};
