/*
JavaScript Document
Project Name: Dormant Neurons Website
Version:  1.0
Owner: Lea Schönherr
Developed By: Soumya Shaw */

function toggleAbout(clickedMember) {
    const modal = document.getElementById("about-modal");
    const overlay = document.querySelector(".about-overlay");
    const contentBox = document.getElementById("about-content");
    const aboutText = clickedMember.nextElementSibling?.innerHTML;
  
    if (!aboutText) return;
  
    // Insert content and make modal visible
    contentBox.innerHTML = aboutText;
    modal.style.visibility = "visible";
    overlay.style.visibility = "visible";
  
    // Trigger fade-in
    modal.classList.add("active");
    overlay.classList.add("active");
}
  
function closePopup() {
    const modal = document.getElementById("about-modal");
    const overlay = document.querySelector(".about-overlay");
  
    // Trigger fade-out
    modal.classList.remove("active");
    overlay.classList.remove("active");
  
    // Hide after transition ends (300ms)
    setTimeout(() => {
      modal.style.visibility = "hidden";
      overlay.style.visibility = "hidden";
    }, 300);
}