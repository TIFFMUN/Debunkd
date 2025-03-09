const inputContainer = document.getElementById('inputContainer');
const userInput = document.getElementById('userInput');
const chatContainer = document.getElementById('chatContainer');
const uploadBtn = document.getElementById('uploadBtn');
const plusPopup = document.getElementById('plusPopup');
const sampleTextBtn = document.getElementById('sampleText');
const documentUploadBtn = document.getElementById('documentUpload');

const sessionId = localStorage.getItem('sessionId') || generateSessionId();
if (!localStorage.getItem('sessionId')) {
    localStorage.setItem('sessionId', sessionId);
}

function generateSessionId() {
    return 'session_' + Math.random().toString(36).substr(2, 9);
}

// Show/hide the plus button popup
uploadBtn.addEventListener('click', (event) => {
    event.stopPropagation();
    plusPopup.style.display = plusPopup.style.display === "flex" ? "none" : "flex";
});

// Hide popup when clicking outside
document.addEventListener('click', function (event) {
    if (!plusPopup.contains(event.target) && event.target !== uploadBtn) {
        plusPopup.style.display = "none";
    }
});

// Send predefined sample text
sampleTextBtn.addEventListener('click', () => {
    plusPopup.style.display = "none";
    sendMessageFromPopup("This is a sample misinformation text.");
});

// Simulate document upload
documentUploadBtn.addEventListener('click', () => {
    plusPopup.style.display = "none";
    alert("Document upload feature coming soon!");
});

// Function to send a message from popup
function sendMessageFromPopup(text) {
    addUserMessage(text);
    addProcessingMessage();
    fetch('http://localhost:5000/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            message: text,
            session_id: sessionId
        })
    })
    .then(response => response.json())
    .then(data => {
        removeProcessingMessage();
        if (data.error) {
            addChatbotMessage(data.error);
        } else {
            addChatbotMessage(data.response);
        }
    })
    .catch(error => {
        removeProcessingMessage();
        addChatbotMessage(`Error: ${error.message}`);
        console.error('Fetch error:', error);
    });
}

// Send message from input field
function sendMessage() {
    const messageText = userInput.value.trim();
    if (messageText) {
        addUserMessage(messageText);
        userInput.value = '';
        addProcessingMessage();
        fetch('http://localhost:5000/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: messageText,
                session_id: sessionId
            })
        })
        .then(response => response.json())
        .then(data => {
            removeProcessingMessage();
            if (data.error) {
                addChatbotMessage(data.error);
            } else {
                addChatbotMessage(data.response);
            }
        })
        .catch(error => {
            removeProcessingMessage();
            addChatbotMessage(`Error: ${error.message}`);
            console.error('Fetch error:', error);
        });
    }
}

// Add processing message
function addProcessingMessage() {
    const processingDiv = document.createElement('div');
    processingDiv.className = 'chatbot-message processing';
    processingDiv.innerHTML = `
        <div class="message bot">Processing...</div>
        <img src="images/chatbot-icon.png" alt="Chatbot" class="chatbot-icon">
    `;
    processingDiv.id = 'processingMessage';
    chatContainer.appendChild(processingDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Remove processing message
function removeProcessingMessage() {
    const processingDiv = document.getElementById('processingMessage');
    if (processingDiv) {
        chatContainer.removeChild(processingDiv);
    }
}

// Add messages to chat
function addUserMessage(text) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'user-message';
    messageDiv.innerHTML = `
        <img src="images/user-icon.png" alt="User" class="user-icon">
        <div class="message user">${text}</div>
    `;
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function addChatbotMessage(text) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'chatbot-message';
    messageDiv.innerHTML = `
        <div class="message bot">${text}</div>
        <img src="images/chatbot-icon.png" alt="Chatbot" class="chatbot-icon">
    `;
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Add initial chatbot message
document.addEventListener('DOMContentLoaded', () => {
    addInitialMessage();
});

function addInitialMessage() {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'chatbot-message';
    messageDiv.innerHTML = `
        <div class="message bot">Hi there, what questions do you have regarding misinformation?</div>
        <img src="images/chatbot-icon.png" alt="Chatbot" class="chatbot-icon">
    `;
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Enter key to send message
userInput.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        event.preventDefault();
        sendMessage();
    }
});

