const searchForUser = () => {
    const searchInputValue = document.getElementById("user_search").value;
    window.location.href = `/pages/chat/?username=${searchInputValue}`;
}

window.onload = () => {
    const searchInput = document.getElementById("user_search");
    searchInput.addEventListener("keydown", function(event) {
        if (event.key === "Enter") {
            event.preventDefault();
            searchForUser();
        }
    });

    const messageButtons = document.querySelectorAll(".write-message-btn");
    messageButtons.forEach(button => {
        button.addEventListener("click", function() {
            const username = this.getAttribute("data-username");
            openChat(username);
        });
    });
};

function openChat(username) {
    const chatContainer = document.getElementById("chat_container");
    chatContainer.innerHTML = `
        <h2 class="text-xl font-bold mb-4">Chat with ${username}</h2>
        <ul id="messages" class="bg-gray-100 p-4 rounded-lg mb-4 h-64 overflow-y-auto"></ul>
        <form id="chat_form" class="flex flex-col">
            <input type="text" id="messageText" class="w-full p-2 border-2 border-gray-300 rounded-lg mb-2" placeholder="Write a message..." autocomplete="off"/>
            <button type="submit" class="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition">Send</button>
        </form>
    `;

    let client_id = Date.now();
    let ws = new WebSocket(`ws://localhost:8000/chat_api/ws/${client_id}`);
    ws.onmessage = function(event) {
        append_message(event.data);
    };

    const chatForm = document.getElementById("chat_form");
    chatForm.addEventListener("submit", function(event) {
        event.preventDefault();
        sendMessage();
    });

    function sendMessage() {
        const input = document.getElementById("messageText");
        ws.send(input.value);
        input.value = '';
    }

    function append_message(msg, isHeader = false) {
        let messages = document.getElementById('messages');
        let message = document.createElement('li');
        if (isHeader) {
            message.classList.add('message-header');
        } else {
            message.classList.add('text-sm', 'text-gray-800', 'bg-white', 'p-2', 'mb-1', 'rounded-lg', 'shadow');
        }
        let content = document.createTextNode(msg);
        message.appendChild(content);
        messages.appendChild(message);
    }

    // Load last messages
    async function getLastMessages() {
        const response = await fetch(`/chat_api/last_messages?username=${username}`, { method: 'GET' });
        return response.json();
    }

    getLastMessages()
        .then(messages => {
            append_message('Last 10 messages:', true);
            messages.forEach(msg => {
                append_message(msg.message);
            });
            append_message('New messages:', true);
        });
}
