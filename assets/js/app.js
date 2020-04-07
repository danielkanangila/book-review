import Router from './router';
import {
    signup,
    verify_email,
    login
} from './auth';
import navbar from './navbar';
import books from './books';
import book from "./book";
import home from "./home";

const app = () => {
    const $this = Router;

    ($this.request.pathname === '/signup' || $this.request.pathname === '/login') ? document.body.classList.add('auth-process') : document.body.classList.remove('auth-process');
    navbar($this.request.pathname);
    $this.route({path: '/', component: home, element: '.container.home'});
    $this.route({path: '/library', component: books, element: '.container.book-list'});
    $this.route({path: '/login', component: login, element: 'form.login'});
    $this.route({path: '/signup', component: signup, element: 'form.signup'});
    $this.route({path: '/email-verification', component: verify_email, element: 'form.check-email'});
    $this.route({path: '/book/:id', component: book, element: '.container.book-section'});
    return $this;
};

export default app();
