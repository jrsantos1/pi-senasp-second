const menu = document.querySelector('.menu');
const NavMenu = document.querySelector('.nav-menu');
const navigation = document.querySelector('.navigation');

menu.addEventListener('click', () => {
    menu.classList.toggle('ativo');
    NavMenu.classList.toggle('ativo');
})

NavMenu.addEventListener('click', () => {
    menu.classList.toggle('ativo');
    NavMenu.classList.toggle('ativo');
})