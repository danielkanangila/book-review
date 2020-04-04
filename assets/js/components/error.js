import render from "../render";

const html = String.raw

export const error = (id, message) => {
    return render(html`
        <span id="${id}" class="error">${message}</span>
    `);
};