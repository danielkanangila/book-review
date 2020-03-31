const html = String.raw

export const error = (id, message) => {
    const error_el_str = html`
        <span id="${id}" class="error">${message}</span>
    `;
    return new DOMParser().parseFromString(error_el_str, 'text/html').body.firstChild;
};