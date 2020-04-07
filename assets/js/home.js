import axios from 'axios';
import resultItem from "./components/result-item";
import suggestionList from "./components/suggestion-list";

const home = ({$this}) => {
    let query = '';
    let searchResult = [];
    const resultBox = $this.querySelector('.result-items');
    const searchBar = $this.querySelector('.search-bar');
    const searchInput = $this.querySelector('input.search');
    const btnSearch = $this.querySelector('button.search-btn');
    const resultCountEl = $this.querySelector('.result-count');
    const notResultTitleEl = $this.querySelector('.not-found');

    const removeSuggestionList = () => {
        if (searchBar.querySelector('.suggestion-list')) {
            searchBar.querySelector('.suggestion-list').remove();
        }
        return false
    };

    const handleClick = e => {
        e.preventDefault();
        removeSuggestionList()
    };

    const resetView = () => {
        resultCountEl.textContent = null;
        resultBox.innerHTML = null;
    };

    const addResultToDOM = () => {
        if (!searchResult.length) {
            resetView();
            notResultTitleEl.classList.remove('hide');
            return false;
        }
        notResultTitleEl.classList.add('hide');
        const resultCount = searchResult.length;
        resultCountEl.textContent = `Books found: ${resultCount}`;
        searchResult.forEach(book => {
            resultBox.append(resultItem({...book}));
        });
    };

    const handleChange = e => {
        query = e.target.value;
        if (!e.target.value) {
            removeSuggestionList();
            resetView();
            return false
        }

        axios.get(`/book/search?q=${query}`)
            .then(res => {
                removeSuggestionList();
                resetView();
                searchResult = res.data.result;
                addResultToDOM();
                let first10 = [];
                if (res.data.result.length > 10) first10 = searchResult.slice(0, 10);
                else first10 = res.data.result;
                const sugList = suggestionList(first10);
                searchBar.append(sugList);
            })
            .catch(err => console.log(err));
    };

    searchInput.addEventListener('keyup', handleChange);
    searchInput.addEventListener('change', handleChange);
    btnSearch.addEventListener('click', handleClick);
};

export default home;