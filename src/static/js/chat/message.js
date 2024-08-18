// Добавление сообщения в чат
export function append_message(msg, isHeader = false, isSentByCurrentUser = false) {
    const messages = document.getElementById('messages');
    const message = document.createElement('li');

    message.classList.add('message-item');
    if (isHeader) {
        message.classList.add('message-header');
    } else {
        if (msg.length === 0) {
            return
        }
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

// Загрузка последних сообщений
export async function loadLastMessages(chat_id, current_user_id) {
    const response = await fetch(`/chat/last_messages/${chat_id}`, { method: 'GET' });
    const messages = await response.json();

    append_message('Last messages:', true);
    messages.forEach(msg => {
        const displayMsg = generateMessageWithStyles(msg, current_user_id);
        append_message(displayMsg, false, msg.sender_id === current_user_id);
    });
    append_message('New messages:', true);
}

// Генерация сообщений с различным стилем
export function generateMessageWithStyles(msg, current_user_id) {
    // Если сообщение отправлено текущим пользователем, изменить имя на "You"
    if (msg.sender_id === current_user_id) {
        msg.username = "You";
    }

    // Переменная для хранения содержимого сообщения
    let content = '';
    let file = msg.file

    if (file) {
        content = `
            <div class="file-details">
                <div>
                    <span class="file-name">${file.filename}</span>
                    <span class="file-size">(${(file.file_size / 1024).toFixed(2)} KB)</span>
                </div>
            </div>
            <a href="${file.file_url}" class="download-link" download>Download file</a>
            <div class="message-body">${msg.message}</div>
        `;
    } else {
        content = `<div class="message-body">${msg.message}</div>`;
    }

    // Возвращаем HTML-код для отображения сообщения
    return `
        <div class="message-header">
            <strong>${msg.username}</strong>
            <span class="timestamp">${msg.timestamp}</span>
        </div>
        ${content}
    `;
}