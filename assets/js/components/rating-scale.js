const ratingScale = (rating) => {
    const averageRating = parseInt(rating);
    const notCheckedValue = 5 - averageRating;
    let checkedRating = '';
    let notCheckedRating = '';

    if (averageRating) {
         checkedRating = [...Array(averageRating).keys()].map(i => {
            return `<span aria-valuetext="${i+1}" class="fa fa-star rating checked"></span>`
        }).join('');
    }
    if (notCheckedValue) {
         notCheckedRating = [...Array(notCheckedValue).keys()].map(i => {
            return `<span aria-valuetext="${i+1}" class="fa fa-star rating"></span>`
        }).join('');
    }

    return `
        <div class="scale">
            ${checkedRating}
            ${notCheckedRating}
        </div>
    `
};

export default ratingScale;