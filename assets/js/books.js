import axios from 'axios';
import loader from './components/loader';
import { card } from './components';

const books = ({$this , $window, $}) => {
    let fetching = 0;

    /**
     * Fetching data and append new card in the DOM
     */
    const fetchData = () => {
        // to be call once when user hit the bottom of $this element on scroll
        if (fetching === 1) {
            // getting next page query hidden in input
            const next_page = $this.find('input[name=next_page]').val();
            // if next page is empty stop function
            if (!next_page) return false;
            // axios get request call to retrieve books to append
            axios.get(`/books${next_page}`)
                .then(res => {
                    // find grid div as card wrapper
                    const $grid = $this.find('div.grid');

                    // check if offset equal row_count set next_page to null
                    if (res.data.offset === res.data.row_count) {
                        // update the value of hidden input where next page is stored
                        $this.find('input[name=next_page]').val('');
                    }
                    // append books to the DOM
                    res.data.result.forEach(book => $grid.append(card({...book})));

                    //rest fetching
                    fetching = 0;
                    // remove loader to the dom
                    $('.book-loader').remove();
                })
                .catch(err => console.error(err));
        }
    };

    $window.scroll(e => {
        const footerHeight = $('footer').innerHeight();
        const navbarHeight = $('.navbar').innerHeight();
        const scrollTo = $this.innerHeight() - navbarHeight - footerHeight - 484;
        const currentPosition = scrollTo - $window.scrollTop();
        if (currentPosition <= 0) {
            $this.append(loader({show: true}));
            fetching++;
            fetchData();
        } else {
            $('.book-loader').remove();
        }
    })
};

export default books;