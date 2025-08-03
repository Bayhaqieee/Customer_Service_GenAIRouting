document.addEventListener('DOMContentLoaded', () => {
    // ... (no changes to the variable declarations at the top) ...
    const userInfoForm = document.getElementById('user-info-form');
    const chatContainer = document.getElementById('chat-container');
    const startChatBtn = document.getElementById('start-chat-btn');
    const sendBtn = document.getElementById('send-btn');
    const messageInput = document.getElementById('message-input');
    const chatBox = document.getElementById('chat-box');

    const styleLink = document.querySelector('link[rel="stylesheet"]');
    const botAvatarUrl = styleLink.dataset.botAvatarUrl;

    let userName = '';
    let userRole = '';

    // ... (no changes to Start Chat and Send Message logic) ...
    startChatBtn.addEventListener('click', () => {
        const nameInput = document.getElementById('user-name');
        const roleInput = document.getElementById('user-role');

        if (nameInput.value.trim() && roleInput.value.trim()) {
            userName = nameInput.value.trim();
            userRole = roleInput.value.trim();
            
            userInfoForm.classList.add('hidden');
            chatContainer.classList.remove('hidden');
            appendMessage(`Hello ${userName}! I'm your AI assistant. How can I help you today?`, 'bot', 'Hybrid AI');
        } else {
            alert('Please enter your name and role.');
        }
    });

    const sendMessage = async () => {
        const message = messageInput.value.trim();
        if (!message) return;

        appendMessage(message, 'user');
        messageInput.value = '';
        messageInput.style.height = 'auto'; // Reset height

        const typingIndicator = appendMessage('', 'bot', 'Typing...');
        typingIndicator.classList.add('typing');

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name: userName, role: userRole, message: message }),
            });

            typingIndicator.remove();

            if (!response.ok) throw new Error('Network response error.');

            const data = await response.json();
            const agentInfo = `${data.agent_name} (${data.agent_specialization})`;
            appendMessage(data.response, 'bot', agentInfo);

        } catch (error) {
            typingIndicator.remove();
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
    
    messageInput.addEventListener('input', () => {
        messageInput.style.height = 'auto';
        messageInput.style.height = (messageInput.scrollHeight) + 'px';
    });


    // --- Helper Function to Append Messages ---
    function appendMessage(text, type, agentInfo = null) {
        const messageWrapper = document.createElement('div');
        messageWrapper.classList.add('message', `${type}-message`);

        const messageContentDiv = document.createElement('div');
        messageContentDiv.classList.add('message-content');
        
        if (type === 'bot') {
            const avatar = document.createElement('img');
            avatar.src = botAvatarUrl;
            avatar.alt = "Bot Avatar";
            avatar.classList.add('bot-avatar');
            messageWrapper.appendChild(avatar);
            
            if (agentInfo) {
                const agentInfoDiv = document.createElement('div');
                agentInfoDiv.classList.add('agent-info');
                agentInfoDiv.textContent = agentInfo;
                messageContentDiv.appendChild(agentInfoDiv);
            }
        }
        
        const p = document.createElement('p');
        
        // MODIFIED: Use marked.parse() to render markdown, else just set text
        if (type === 'bot') {
            p.innerHTML = marked.parse(text);
        } else {
            p.textContent = text;
        }

        messageContentDiv.appendChild(p);
        
        messageWrapper.appendChild(messageContentDiv);
        chatBox.appendChild(messageWrapper);
        chatBox.scrollTop = chatBox.scrollHeight;
        return messageWrapper;
    }
});