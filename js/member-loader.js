/*
JavaScript Document
Project Name: Dormant Neurons Website
Version:  1.0
Owner: Lea Schönherr
Developed By: Soumya Shaw */

document.addEventListener("DOMContentLoaded", () => {
    console.log("Loading team members...");

    fetch("./data/members.json")
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(members => {
            const teamContainer = document.querySelector(".team-container");

            members.forEach(member => {
                const memberDiv = document.createElement("div");
                memberDiv.classList.add("team-member");
                memberDiv.setAttribute("onclick", "toggleAbout(this)");

                const imageContainer = document.createElement("div");
                imageContainer.classList.add("team-image");

                const imgDefault = document.createElement("img");
                imgDefault.classList.add("img-default");
                imgDefault.src = member.image || "img/team/placeholder.png";
                imgDefault.alt = member.name;

                const imgHover = document.createElement("img");
                imgHover.classList.add("img-hover");
                imgHover.src = member.image_alt || member.image;
                imgHover.alt = member.name;

                imageContainer.appendChild(imgDefault);
                imageContainer.appendChild(imgHover);

                const nameP = document.createElement("p");
                nameP.classList.add("name");
                nameP.textContent = member.name;

                const positionP = document.createElement("p");
                positionP.classList.add("position");
                positionP.textContent = member.position;

                memberDiv.appendChild(imageContainer);
                memberDiv.appendChild(nameP);
                memberDiv.appendChild(positionP);

                const aboutHidden = document.createElement("div");
                aboutHidden.classList.add("about-hidden");
                aboutHidden.style.display = "none";

                const nameH2 = document.createElement("h2");
                nameH2.textContent = member.name;

                const aboutP = document.createElement("p");
                aboutP.textContent = member.about;

                const attributesDiv = document.createElement("div");
                attributesDiv.classList.add("attributes");

                const interestsDiv = document.createElement("div");
                interestsDiv.classList.add("interests-container");

                let interests = [];
                try {
                    interests = JSON.parse(member.research.replace(/'/g, '"'));
                } catch (e) {
                    console.warn(`Failed to parse interests for ${member.name}`);
                }

                console.log(`Interests for ${member.name}:`, interests);

                interests.forEach(interest => {
                    const tag = document.createElement("span");
                    tag.classList.add("interest-tag");
                    tag.textContent = interest;
                    interestsDiv.appendChild(tag);
                });

                attributesDiv.appendChild(interestsDiv);
                aboutHidden.appendChild(nameH2);
                aboutHidden.appendChild(aboutP);
                aboutHidden.appendChild(attributesDiv);


                teamContainer.appendChild(memberDiv);
                teamContainer.appendChild(aboutHidden);
            });
        })
        .catch(error => {
            console.error("Error loading team members:", error);
        });
});