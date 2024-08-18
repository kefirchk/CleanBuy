import { generateMessageWithStyles, append_message } from './message.js';
import { getCurrentTimestamp } from "./utils.js";


// Инициализация WebSocket
export function initializeWebSocket(chat_id, current_user_id) {
    const client_id = Date.now();
    const ws = new WebSocket(`https://localhost:443/chat/ws/${client_id}`);

    ws.onmessage = function(event) {
        const message_data = JSON.parse(event.data);
        if (message_data.chat_id === chat_id) {
            const displayMsg = generateMessageWithStyles(message_data, current_user_id);
            append_message(displayMsg, false, message_data.sender_id === current_user_id);
        }
    };

    return ws;
}

// Отправка сообщения
export async function sendMessage(chat_id, current_user_id, ws) {
    const input = document.getElementById("messageText");
    const fileInput = document.getElementById("fileInput");
    let fileData = {};

    // Не отправляем сообщения, если они пустые
    if (input.value.length === 0 && fileInput.value.length === 0) {
        console.log("[INFO] Don't send message")
        return
    }

    if (fileInput.files.length > 0) {
        const formData = new FormData();
        formData.append("file", fileInput.files[0]);

        const uploadResponse = await fetch("/files/upload_file", {
            method: "POST",
            body: formData
        });

        let uploadData = await uploadResponse.json();
        fileData = {
            file_url: `/files/${uploadData['file_id']}`,
            file_size: uploadData.file_size,
            filename: uploadData.filename,
            file_type: uploadData.file_type
        }
    } else {
        fileData = null;
    }

    const message = {
        chat_id: chat_id,
        sender_id: current_user_id,
        message: input.value,
        username: "You",
        timestamp: getCurrentTimestamp(),
        file: fileData
    };

    ws.send(JSON.stringify(message));

    const displayMsg = generateMessageWithStyles(message, current_user_id);
    append_message(displayMsg, false, true);

    input.value = '';
    fileInput.value = '';
}


