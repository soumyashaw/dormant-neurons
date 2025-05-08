/*
JavaScript Document
Project Name: Dormant Neurons Website
Version:  1.0
Owner: Lea Schönherr
Developed By: Soumya Shaw */

document.addEventListener("DOMContentLoaded", () => {
    console.log("Loading latest news...");

    fetch("./data/news.json")
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(newsItems => {
            const newsContainer = document.querySelector(".latest-news-inner");

            newsItems.forEach(news => {
                const itemDiv = document.createElement("div");
                itemDiv.classList.add("latest-news-item");

                // Date
                const dateDiv = document.createElement("div");
                dateDiv.classList.add("news-item-date");

                // Format 'DD-MM-YYYY' to 'DD Month YYYY'
                const [day, month, year] = news.date.split("-");
                const dateObject = new Date(`${year}-${month}-${day}`);
                const formattedDate = dateObject.toLocaleDateString("en-GB", {
                    day: "numeric",
                    month: "long",
                    year: "numeric"
                });

                dateDiv.innerHTML = `<p><i>${formattedDate}</i></p>`;

                // Container for header and body
                const contentContainer = document.createElement("div");
                contentContainer.classList.add("news-item-container");

                // Header
                const headerDiv = document.createElement("div");
                headerDiv.classList.add("news-item-header");
                headerDiv.innerHTML = `<h1>${news.header}</h1>`;

                // Divider line
                const hr = document.createElement("hr");
                hr.classList.add("news-item-line");

                // Body
                const bodyDiv = document.createElement("div");
                bodyDiv.classList.add("news-item-content");

                // Convert markdown-style link [text](url) to actual <a> element
                const parsedBody = news.body.replace(
                    /\[([^\]]+)\]\(([^)]+)\)/g,
                    '<a href="$2" target="_blank">$1</a>'
                );

                bodyDiv.innerHTML = `<p>${parsedBody}</p>`;

                // Compose and append
                contentContainer.appendChild(headerDiv);
                contentContainer.appendChild(hr);
                contentContainer.appendChild(bodyDiv);

                itemDiv.appendChild(dateDiv);
                itemDiv.appendChild(contentContainer);

                newsContainer.appendChild(itemDiv);
            });
        })
        .catch(error => {
            console.error("Error loading news items:", error);
        });
});