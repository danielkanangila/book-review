export const signupConstraint = {
    first_name: {
        presence: {
            message: 'is required'
        },
        length: {
            minimum: 3,
            message: 'must be at least 3 characters.'
        }
    },
    last_name: {
        presence: {
            message: 'Last name is required'
        },
        length: {
            minimum: 3,
            message: 'must be at least 3 characters.'
        }
    },
    email: {
        presence: true,
        email: true
    },
    password: {
        length: {
            minimum: 8,
            message: 'must be at least 8 characters. '
        },
        format: {
            pattern: ".*(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[$@#_\\-\\/.\\\\]).*",
            message: "must contain at least one uppercase and lowercase character, one numeric and one of the following special character: [ $ @ _ - \ / .]"
        }
    },
    confirm_password: {
        equality: "password"
    }
};