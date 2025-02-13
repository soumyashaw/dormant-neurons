console.log('parallax.js loaded');

let barElement1 = document.getElementById("bar-1");
let barElement2 = document.getElementById("bar-2");

window.addEventListener("scroll", () => {
    let scrollY = window.scrollY; // Get current scroll position
    let speed1 = parseFloat(barElement1.dataset.speed) || 1;
    let speed2 = parseFloat(barElement2.dataset.speed) || 1; 
    let translateY1 = scrollY * speed1;
    let translateY2 = scrollY * speed2;

    barElement1.style.transform = `translate(0px, ${translateY1}px)`;
    barElement2.style.transform = `translate(0px, ${translateY2}px)`;
});