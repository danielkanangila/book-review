import render from "../render";
import ratingScale from "./rating-scale";

const resultItem = ({id, title, author, year, isbn, average_rating}) => {
    return render(`
        <div class="result-item">
            <h2 class="result-item__book-title">
                <a href="/book/${id}">${title}</a>
            </h2>
            <p class="result-item__book-author">${author}</p>
            <p class="result-item__book-details">
                <span>Year: ${year}</span>
                <span>ISBN: ${isbn}</span>
            </p>
            <div class="result-item__book-rating">
                ${ratingScale(average_rating)}
                <span>${average_rating}</span>
            </div>
        </div>
    `);
};

export default resultItem;