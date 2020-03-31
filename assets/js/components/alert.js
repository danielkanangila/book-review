const html = String.raw;

export const alert = (type, message) => {
    const str_template = html`
        <p class="alert ${type}">
            ${message}
        </p>
    `;

    return new DOMParser().parseFromString(str_template, 'text/html').body.firstChild;
};