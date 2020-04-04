const state = (initialState) => {
    return new Proxy(initialState, {
            set: function (target, property, value) {
                target[property] = value;
                return true;
            }
    })
};

export default state;