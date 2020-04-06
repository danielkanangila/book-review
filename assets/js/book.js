import axios from 'axios';
import {handleError} from "./utils";
import comment from './components/comment';

const book = ({$this, params}) => {
    let state = {
        comment: '',
        rating: 0
    };
    const form = $this.querySelector('form#review');
    const textarea = form.querySelector('textarea[name=comment]');
    const ratingScale = form.querySelectorAll('span.rating');

    // hide card link
    $this.querySelector('.book-card__link').classList.add('hide');
    // change cursor
    $this.querySelector('.book-card').classList.add('cursor-normal');

    const handleChange = e => {
        state = {
            ...state,
            comment: e.target.value
        };
        // Validation on keyup and on change
        if (e.target.value.length >= 8) {
            // Remove error
            textarea.classList.remove('error');
            handleError($this, '', true);
        } else {

        }
    };

    const handleRating = e => {
        state = {
            ...state,
            rating:  e.target.getAttribute('aria-valuetext')
        };
        for (let i = 0; i < state.rating; i++) {
            ratingScale[i].classList.add('checked');
        }
        for (let i = state.rating; i < ratingScale.length; i++) {
            ratingScale[i].classList.remove('checked');
        }
    };

    const showSuccessMessage = () => {
         form.querySelector('.success-message').classList.remove('hide');
        setTimeout(() => {
            form.querySelector('.success-message').classList.add('hide');
        }, 3000);
    };

    const resetRating = () => {
         for (let i = 0; i < 5; i++) {
            ratingScale[i].classList.remove('checked');
        }
    }

    const handleSubmit = e => {
        e.preventDefault();
        // remove error if exist
        handleError($this, '', true);
        textarea.classList.remove('error');

        // check in comment is not empty
        if (!state.comment || state.comment.length < 8) {
            textarea.classList.add('error');
            handleError(form, "Comment is required and must be at least 8 characters.");
            return false;
        }

        axios.post(`/book/${params.id}`, state)
            .then(res => {
                textarea.value = '';
                resetRating();

                showSuccessMessage();
                $this.querySelector('.comments').append(comment({...res.data.result[0]}));
            })
            .catch(err =>  handleError($this, err.response.data.error || err));
    };

    // Form event
    form.addEventListener('submit', handleSubmit);
    textarea.addEventListener('change', handleChange);
    textarea.addEventListener('keyup', handleChange);

    ratingScale.forEach(
        rating => rating.addEventListener('click', handleRating));

    // set checked class to ratings class of Goodreads review data
    // select scale spans in rating card
    const grScaleSpans = $this.querySelectorAll('.rating-card .rating');
    // get rating value stored in hidden input
    const averageRating = parseInt($this.querySelector('input[name=average_rating]').value);

    for (let i = 0; i < averageRating; i++) {
        grScaleSpans[i].classList.add('checked');
    }
};

export default book;