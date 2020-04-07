import render from "../render";

const suggestionList = (books) => {
    return render(`
        <ul class="suggestion-list">
            ${books.map(book => {
                return `
                    <li class="item">
                        <a href="/book/${book.id}">${book.title}</a>
                     </li>
                `
                }).join('')}
         </ul>
    `);
};

export default suggestionList;