document.addEventListener("DOMContentLoaded", () => {
    console.log("Loading team members...");

    fetch("./data/trial_members.json")
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

                const img = document.createElement("img");
                img.src = member.image || "img/team/boss.png";
                img.alt = member.name;

                const nameP = document.createElement("p");
                nameP.classList.add("name");
                nameP.textContent = member.name;

                const positionP = document.createElement("p");
                positionP.classList.add("position");
                positionP.textContent = member.position;

                memberDiv.appendChild(img);
                memberDiv.appendChild(nameP);
                memberDiv.appendChild(positionP);

                teamContainer.appendChild(memberDiv);
            });
        })
        .catch(error => {
            console.error("Error loading team members:", error);
        });
});