import render from '../render';
import ratingScale from "./rating-scale";

const html = String.raw;

export const card = ({id, title, author, year, isbn, average_rating}) => {
    return render(html`
        <div id="${id}" class="book-card">
            <a class="book-card__link" id="${id}" href="/book/${id}"></a>
            <div class="book-card__cover-illustrator">
                <i class="far fa-image"></i>
            </div>
            <h2 class="book-card__title">${title}</h2>
            <p class="book-card__author-name">By ${author}</p>
            <p class="book-card__details">
                <span class="year">Year: ${year}</span>
                <span class="isbn">ISBN: ${isbn}</span>
            </p>
            <div class="book-card__rating">
                ${ratingScale(average_rating)}
                <span>${average_rating}</span>
            </div>
        </div>
    `);
};