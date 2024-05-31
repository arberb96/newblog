let header = document.querySelector('header')

window.addEventListener('scroll', () => {

    console.log("scroll event triggered")
    header.classList.toggle('shadow', window.scrollY > 0)
})