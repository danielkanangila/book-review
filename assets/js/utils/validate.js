import validate from 'validate.js';

export const validator = (data, constraints) => {
 return validate(data, constraints)
};