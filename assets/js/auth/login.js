import axios from 'axios';
import {alert} from '../components';
import {handleError} from "../utils";

export const login = (selector) => {
    let credentials = {
        email: "",
        password: ""
    };
    const form = document.querySelector(selector);
    const inputs = form.querySelectorAll('input');

    const handleChange = e => {
        credentials = {
            ...credentials,
            [e.target.name]: e.target.value
        };
    };

    const handleSubmit =  e => {
        e.preventDefault();
        form.querySelector('.loader-wrapper').classList.remove('hide')
        // get redirect url
        const queryString = new URLSearchParams(window.location.search);
        const redirect_url = queryString ? queryString.get('next') : '/';
        //window.location.replace(redirect_url);
        // remove alert type error if it exist in the DOm
        handleError(selector, "", true);
        // check if credentials is not empty
        if (!credentials.email || !credentials.password) {
             handleError(selector, "Email and password are required.");
             return false;
        }
        // API call
        axios.post('/login', credentials)
            .then(response => {
                form.querySelector('.loader-wrapper').classList.add('hide');
                localStorage.setItem('access_token', response.data.access_token);
                window.location.replace(redirect_url);
            })
            .catch(err => {
                form.querySelector('.loader-wrapper').classList.add('hide');
                handleError(selector, err.response.data.error || err);
            })
    };

    form.addEventListener('submit', handleSubmit);
    inputs.forEach(input => input.addEventListener('change', handleChange));
};