const navbar = () => {
    const navbarEl = document.querySelector('.navbar');
    const openMenuBtn = navbarEl.querySelector('#menu');
    const closeBtn = navbarEl.querySelector('#closeBtn');
    const logoutBtn = navbarEl.querySelector('#logoutBtn');

    const logout = e => {
        e.preventDefault();
        localStorage.removeItem('access_token');
        window.location.replace('/logout');
    };

    const closeSidenav = () => {
        document.getElementById('mySidenav').style.width = "0";
    };

    const openSidenav = () => {
         document.getElementById('mySidenav').style.width = "350px";
    };

    logoutBtn.addEventListener('click', logout);
    closeBtn.addEventListener('click', closeSidenav);
    openMenuBtn.addEventListener('click', openSidenav);
};

export default navbar;