const book = ({$this, $}) => {
    let state = {
        comment: '',
        rating: 0
    };
    const form = $this.querySelector('form#review');
    const textarea = form.querySelector('textarea[name=comment]');
    const ratingScale = form.querySelectorAll('span.rating');

    const handleChange = e => {
        state = {
            ...state,
            comment: e.target.value
        }
    };

    const handleRating = e => {
        const value = e.target.getAttribute('aria-valuetext');
        state = {
            ...state,
            rating: value
        };
        for (let i=0; i < value; i++) {
            ratingScale[i].classList.add('checked');
        }
        for (let i=value; i < ratingScale.length; i++) {
            ratingScale[i].classList.remove('checked');
        }
    };

    const handleSubmit = e => {
        e.preventDefault();
    };


    form.addEventListener('submit', handleSubmit);
    textarea.addEventListener('change', handleChange);
    ratingScale.forEach(
        rating => rating.addEventListener('click', handleRating));

    // set checked class to ratings class of Goodreads review data
    // select scale spans in rating card
    const grScaleSpans = $this.querySelectorAll('.rating-card .rating');
    // get rating value stored in hidden input
    const averageRating = parseInt($this.querySelector('input[name=average_rating]').value);

    for (let i=0; i < averageRating; i++) {
        grScaleSpans[i].classList.add('checked');
    }
};

export default book;