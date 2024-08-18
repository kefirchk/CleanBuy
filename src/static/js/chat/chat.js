import { initializeWebSocket, sendMessage } from "./websocket.js";
import { loadLastMessages } from "./message.js";


// Инициализация кнопок отправки сообщений
export function initializeMessageButtons() {
    const messageButtons = document.querySelectorAll(".write-message-btn");
    messageButtons.forEach(button => {
        button.addEventListener("click", async function() {
            const current_user_id = parseInt(this.getAttribute("data-current_user_id"));
            const other_user_id = parseInt(this.getAttribute("data-other_user_id"));
            const username = this.getAttribute("data-username");

            const chat_id = await fetchChatId(current_user_id, other_user_id);
            await openChat(current_user_id, other_user_id, username, chat_id);
        });
    });
}

// Рендеринг контейнера чата
function renderChatContainer(username) {
    const chatContainer = document.getElementById("chat_container");
    chatContainer.innerHTML = `
        <h2 class="text-xl font-bold mb-4">Chat with ${username}</h2>
        <ul id="messages" class="bg-gray-100 p-4 rounded-lg mb-4 h-64 overflow-y-auto"></ul>
        <form id="chat_form" class="flex flex-col">
            <input type="text" id="messageText" class="w-full p-2 border-2 border-gray-300 rounded-lg mb-2" placeholder="Write a message..." autocomplete="off"/>
            <input type="file" id="fileInput" class="mb-2">
            <button type="submit" class="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition">Send</button>
        </form>
    `;
}

// Инициализация формы отправки сообщений
function initializeChatForm(chat_id, current_user_id, ws) {
    const chatForm = document.getElementById("chat_form");
    chatForm.addEventListener("submit", async function(event) {
        event.preventDefault();
        await sendMessage(chat_id, current_user_id, ws);
    });
}

// Открытие чата
export async function openChat(current_user_id, other_user_id, username, chat_id) {
    renderChatContainer(username);
    const ws = initializeWebSocket(chat_id, current_user_id);
    initializeChatForm(chat_id, current_user_id, ws);
    await loadLastMessages(chat_id, current_user_id);
}

// Получение chat_id
export async function fetchChatId(current_user_id, other_user_id) {
    const response = await fetch(`/chat/id?user1_id=${current_user_id}&user2_id=${other_user_id}`);
    const data = await response.json();
    return data.chat_id;
}

