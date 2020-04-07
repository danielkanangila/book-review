import render from '../render';
import ratingScale from "./rating-scale";
const comment = ({comment, rating, created_at}) => {
    return render(`
        <div class="comment">
            <p>${ comment }</p>
            <p class="created-at">On: ${ created_at }</p>
            ${ratingScale(rating)}
    `);
};

export default comment;