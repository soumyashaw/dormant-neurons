/*
JavaScript Document
Project Name: Dormant Neurons Website
Version:  1.0
Owner: Lea Schönherr
Developed By: Soumya Shaw */

function copyBibtex(button) {
    const bibtex = button.closest('.bibtex').querySelector('.bibtex-entry').innerText;
    navigator.clipboard.writeText(bibtex).then(() => {
        const icon = button.querySelector('i');
        const originalIcon = icon.className;
        const originalText = button.innerHTML;

        // Change icon and text
        icon.className = 'fa-solid fa-check';
        button.innerHTML = '<i class="fa-solid fa-check"></i> Copied!';

        button.classList.add('copied');

        // Revert back after 1.5 seconds
        setTimeout(() => {
            button.innerHTML = `<i class="${originalIcon}"></i> Copy BibTeX`;
            button.classList.remove('copied');
        }, 1500);
    });
}