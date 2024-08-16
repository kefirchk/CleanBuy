window.onload = () => {
    const searchForUser = () => {
        const searchInputValue = document.getElementById("user_search").value;
        window.location.href = `/pages/chat/?username=${searchInputValue}`;
    }

    const searchInput = document.getElementById("user_search");
    searchInput.addEventListener("keydown", function(event) {
        if (event.key === "Enter") {
            event.preventDefault();
            searchForUser();
        }
    });

    const messageButtons = document.querySelectorAll(".write-message-btn");
    messageButtons.forEach(button => {
        button.addEventListener("click", async function() {
            const current_user_id = parseInt(this.getAttribute("data-current_user_id"));
            const other_user_id = parseInt(this.getAttribute("data-other_user_id"));
            const username = this.getAttribute("data-username");

            // Get chat_id
            const response = await fetch(`/chat/id?user1_id=${current_user_id}&user2_id=${other_user_id}`);
            const data = await response.json();
            const chat_id = data.chat_id;

            openChat(current_user_id, other_user_id, username, chat_id);
        });
    });
};


function openChat(current_user_id, other_user_id, username, chat_id) {
    const chatContainer = document.getElementById("chat_container");
    chatContainer.innerHTML = `
        <h2 class="text-xl font-bold mb-4">Chat with ${username}</h2>
        <ul id="messages" class="bg-gray-100 p-4 rounded-lg mb-4 h-64 overflow-y-auto"></ul>
        <form id="chat_form" class="flex flex-col">
            <input type="text" id="messageText" class="w-full p-2 border-2 border-gray-300 rounded-lg mb-2" placeholder="Write a message..." autocomplete="off"/>
            <button type="submit" class="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition">Send</button>
        </form>
    `;

    let client_id = Date.now()
    let ws = new WebSocket(`wss://localhost:443/chat/ws/${client_id}`);

    // Handler for server messages:
    ws.onmessage = function(event) {
        const message_data = JSON.parse(event.data);
        if (message_data.chat_id === chat_id) {
            const displayMsg = generateMessageWithStyles(message_data);
            append_message(displayMsg, false, message_data.sender_id === current_user_id);
        }
    };

    // Handler for Enter key in the chat
    const chatForm = document.getElementById("chat_form");
    chatForm.addEventListener("submit", function(event) {
        event.preventDefault();
        sendMessage();
    });

    function sendMessage() {
        const input = document.getElementById("messageText");
        const timestamp = new Date().toLocaleString('en-GB', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        }).replace(/(\d+)\/(\d+)\/(\d+),/, '$3-$2-$1');

        const message = {
            chat_id: chat_id,
            sender_id: current_user_id,
            message: input.value,
            username: "You",
            timestamp: timestamp
        };

        // Send a message through WebSocket
        ws.send(JSON.stringify(message));

        // Add the message on the screen
        const displayMsg = generateMessageWithStyles(message);
        append_message(displayMsg, false, true);

        // Clean input field
        input.value = '';
    }

    function append_message(msg, isHeader = false, isSentByCurrentUser = false) {
        let messages = document.getElementById('messages');
        let message = document.createElement('li');

        if (isHeader) {
            message.classList.add('message-header');
        } else {
            message.classList.add('message-item');
            if (isSentByCurrentUser) {
                message.classList.add('sent');
            } else {
                message.classList.add('received');
            }
        }

        message.innerHTML = msg;
        messages.appendChild(message);
        messages.scrollTop = messages.scrollHeight;
    }

    async function getLastMessages() {
        const response = await fetch(`/chat/last_messages/${chat_id}`, { method: 'GET' });
        return response.json();
    }

    getLastMessages()
    .then(messages => {
        append_message('Last 10 messages:', true);
        messages.forEach(msg => {
            const displayMsg = generateMessageWithStyles(msg);
            append_message(displayMsg, false, msg.sender_id === current_user_id);
        });
        append_message('New messages:',  true);
    });

    function generateMessageWithStyles(msg) {
        if (msg.sender_id === current_user_id) {
            msg.username = "You";
        }
        return `
            <div class="message-header">
                <strong>${msg.username}</strong> 
                <span class="timestamp">${msg.timestamp}</span>
            </div>
            <div class="message-body">${msg.message}</div>
        `
    }
}