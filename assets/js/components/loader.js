import render from '../render';

const loader = ({show}) => {
      if (!document.querySelector('.book-loader')) {
            return render(`
              <div class="book-loader ${show ? 'show' : 'hide'}">
                  <div class="loader books"></div>
              </div>
            `)
      }
};

export default loader;