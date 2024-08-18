// Инициализация поиска пользователя
export function initializeSearch() {
    const searchInput = document.getElementById("user_search");
    searchInput.addEventListener("keydown", function(event) {
        if (event.key === "Enter") {
            event.preventDefault();
            searchForUser();
        }
    });
}

export function searchForUser() {
    const searchInputValue = document.getElementById("user_search").value;
    window.location.href = `/pages/chat/?username=${searchInputValue}`;
}
