import render from '../render';

const html = String.raw;

export const alert = (type, message) => {
    return render(html`
        <p class="alert ${type}">
            ${message}
        </p>
    `);
};