const render = (str_template) => {
    return new DOMParser().parseFromString(str_template, 'text/html').body.firstChild;
};

export default render;