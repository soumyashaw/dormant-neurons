console.log("Loading papers...");
document.addEventListener("DOMContentLoaded", () => {
    console.log("Script loaded and DOM fully loaded.");
    fetch("./data/trial_papers.json")
        .then(response => {
            console.log("Fetching JSON file...");
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log("JSON successfully loaded:", data); // Log JSON content
            const container = document.getElementById("papers-container");

            data.forEach((paper, index) => {
                // Create the outer div
                const paperOuter = document.createElement("div");
                paperOuter.classList.add("paper-outer");

                // Date div
                const dateDiv = document.createElement("div");
                dateDiv.classList.add("date");

                const calendarIcon = document.createElement("i");
                calendarIcon.classList.add("fa-solid", "fa-calendar-days");

                const dateStrong = document.createElement("strong");
                dateStrong.textContent = paper.date;

                dateDiv.appendChild(calendarIcon);
                dateDiv.appendChild(dateStrong);

                // Paper Inner Container
                const paperInner = document.createElement("div");
                paperInner.classList.add("paper-inner");

                // Title with link
                const paperTitle = document.createElement("div");
                paperTitle.classList.add("paper-title");

                const paperLink = document.createElement("a");
                paperLink.href = paper.link;
                paperLink.target = "_blank";
                paperLink.textContent = paper.title;

                paperTitle.appendChild(paperLink);

                // Authors
                const paperAuth = document.createElement("div");
                paperAuth.classList.add("paper-auth");
                paperAuth.textContent = paper.authors;

                // Journal / Conference
                const paperJournal = document.createElement("div");
                paperJournal.classList.add("paper-journal");
                paperJournal.textContent = paper.journal;

                // Append elements
                paperInner.appendChild(paperTitle);
                paperInner.appendChild(paperAuth);
                paperInner.appendChild(paperJournal);

                // Create BibTex button
                const bibtexContainer = document.createElement("div");
                bibtexContainer.classList.add("bibtex");

                const pre = document.createElement("pre");
                pre.classList.add("bibtex-entry");
                pre.textContent = paper.bibtex;

                const copyButton = document.createElement("button");
                copyButton.classList.add("copy-button");
                copyButton.innerHTML = '<i class="fa-solid fa-copy"></i> Copy BibTeX';
                copyButton.onclick = function () {
                    copyBibtex(this);
                };

                bibtexContainer.appendChild(pre);
                bibtexContainer.appendChild(copyButton);
                
                paperOuter.appendChild(dateDiv);
                paperOuter.appendChild(paperInner);
                paperOuter.appendChild(bibtexContainer);

                // Separator
                const separator = document.createElement("hr");
                paperOuter.appendChild(separator);

                // Append to container
                container.appendChild(paperOuter);
            });
        })
        .catch(error => console.error("Error loading papers:", error));
});