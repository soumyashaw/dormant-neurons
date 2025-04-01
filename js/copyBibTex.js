function copyBibtex(elementId) {
    const bibtex = document.getElementById(elementId).innerText;

    navigator.clipboard.writeText(bibtex)
        .then(() => {
            alert("BibTeX copied to clipboard!");
        })
        .catch(err => {
            console.error("Failed to copy BibTeX:", err);
        });
}