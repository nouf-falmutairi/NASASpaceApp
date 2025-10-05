document.addEventListener("DOMContentLoaded", () => {
    const searchButton = document.getElementById("search-button");
    const searchInput = document.getElementById("search-input");
    const resultsContainer = document.getElementById("results-container");
    const loadingBanner = document.getElementById("loading-banner");

    function showLoading() {
        loadingBanner.classList.add("visible");
    }

    function hideLoading() {
        loadingBanner.classList.remove("visible");
    }

    async function fetchStudies(query) {
        showLoading();
        resultsContainer.innerHTML = "";

        try {
            const response = await fetch(`/semantic-search?query=${encodeURIComponent(query)}`);
            const data = await response.json();

            if (data.error) {
                resultsContainer.innerHTML = `<p style="color:red;">${data.error}</p>`;
            } else if (data.length === 0) {
                resultsContainer.innerHTML = `<p>No results found.</p>`;
            } else {
                data.forEach(study => {
                    const card = document.createElement("div");
                    card.className = "card";
                    card.innerHTML = `
                        <div class="title">${study["study Title"]}</div>
                        <div class="description">${study["study description"]}</div>
                        <div class="meta">
                            Study ID: ${study["study ID"]} | Relevance: ${study["Relevance"]}% 
                            ${study["study URL"] ? `| <a href="${study["study URL"]}" target="_blank">Link</a>` : ""}
                        </div>
                    `;
                    resultsContainer.appendChild(card);
                });
            }
        } catch (err) {
            resultsContainer.innerHTML = `<p style="color:red;">Error fetching studies: ${err}</p>`;
        } finally {
            hideLoading();
        }
    }

    searchButton.addEventListener("click", () => {
        const query = searchInput.value.trim();
        if (query) fetchStudies(query);
    });

    searchInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter") {
            const query = searchInput.value.trim();
            if (query) fetchStudies(query);
        }
    });
});
