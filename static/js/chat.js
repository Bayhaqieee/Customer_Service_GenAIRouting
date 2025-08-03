// File: static/js/chat.js
document.addEventListener('DOMContentLoaded', () => {
    const userInfoForm = document.getElementById('user-info-form');
    const chatContainer = document.getElementById('chat-container');
    const startChatBtn = document.getElementById('start-chat-btn');
    const sendBtn = document.getElementById('send-btn');
    const messageInput = document.getElementById('message-input');
    const chatBox = document.getElementById('chat-box');

    let userName = '';
    let userRole = '';

    // Start Chat
    startChatBtn.addEventListener('click', () => {
        const nameInput = document.getElementById('user-name');
        const roleInput = document.getElementById('user-role');

        if (nameInput.value.trim() && roleInput.value.trim()) {
            userName = nameInput.value.trim();
            userRole = roleInput.value.trim();
            
            userInfoForm.classList.add('hidden');
            chatContainer.classList.remove('hidden');
        } else {
            alert('Please enter your name and role.');
        }
    });

    // Send Message
    const sendMessage = async () => {
        const message = messageInput.value.trim();
        if (!message) return;

        // Display user message
        appendMessage(message, 'user');
        messageInput.value = '';

        // Display typing indicator
        appendMessage('...', 'bot', 'Typing');

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    name: userName,
                    role: userRole,
                    message: message,
                }),
            });

            // Remove typing indicator
            chatBox.removeChild(chatBox.lastChild);

            if (!response.ok) {
                throw new Error('Network response was not ok.');
            }

            const data = await response.json();
            const agentInfo = `${data.agent_name} (${data.agent_specialization})`;
            appendMessage(data.response, 'bot', agentInfo);

        } catch (error) {
            console.error('Error:', error);
            appendMessage('Sorry, something went wrong. Please try again.', 'bot', 'System');
        }
    };

    sendBtn.addEventListener('click', sendMessage);
    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    // Helper Function to Append Messages
    function appendMessage(text, type, agentInfo = null) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', `${type}-message`);
        
        let messageContent = '';
        if (agentInfo) {
            messageContent += `<div class="agent-info">${agentInfo}</div>`;
        }
        messageContent += `<p>${text.replace(/\n/g, '<br>')}</p>`;
        
        messageDiv.innerHTML = messageContent;
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }
});