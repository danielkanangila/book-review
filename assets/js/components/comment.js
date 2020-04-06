import render from '../render';

const comment = ({comment, rating, created_at}) => {
    const averageRating = parseInt(rating);
    const notCheckedValue = 5 - averageRating;

    const checkedSpan = [...Array(averageRating).keys()].map(i => {
        return `<span aria-valuetext="${i+1}" class="fa fa-star rating checked"></span>`
    }).join('');
    const notCheckedSpan = [...Array(notCheckedValue).keys()].map(i => {
        return `<span aria-valuetext="${i+1}" class="fa fa-star rating"></span>`
    }).join('');

    return render(`
        <div class="comment">
            <p>${ comment }</p>
            <p class="created-at">On: ${ created_at }</p>
            <div class="scale">
                ${checkedSpan}
                ${notCheckedSpan}
            </div>
    `);
};

export default comment;