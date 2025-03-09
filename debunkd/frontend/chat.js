// const inputContainer = document.getElementById('inputContainer');
// const userInput = document.getElementById('userInput');
// const chatContainer = document.getElementById('chatContainer');
// const uploadBtn = document.getElementById('uploadBtn');
// const uploadPopup = document.getElementById('uploadPopup');
// const closePopup = document.getElementById('closePopup');
// const imageInput = document.getElementById('imageInput');
// const submitImage = document.getElementById('submitImage');

// const sessionId = localStorage.getItem('sessionId') || generateSessionId();
// if (!localStorage.getItem('sessionId')) {
//     localStorage.setItem('sessionId', sessionId);
// }

// function generateSessionId() {
//     return 'session_' + Math.random().toString(36).substr(2, 9);
// }

// if (!inputContainer || !userInput || !chatContainer || !uploadBtn || !uploadPopup || !closePopup || !imageInput || !submitImage) {
//     console.error('One or more DOM elements not found:', { inputContainer, userInput, chatContainer, uploadBtn, uploadPopup, closePopup, imageInput, submitImage });
// }

// // Initialize Tesseract worker
// async function initWorker() {
//     const worker = await Tesseract.createWorker();
//     await worker.load();
//     await worker.loadLanguage('eng');
//     await worker.initialize('eng');
//     return worker;
// }

// function sendMessage() {
//     const messageText = userInput.value.trim();
//     if (messageText) {
//         addUserMessage(messageText);
//         userInput.value = '';
//         fetch('http://localhost:5000/chat', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json',
//             },
//             body: JSON.stringify({
//                 message: messageText,
//                 session_id: sessionId
//             })
//         })
//         .then(response => response.json())
//         .then(data => {
//             if (data.error) {
//                 addChatbotMessage(data.error);
//             } else {
//                 addChatbotMessage(data.response);
//             }
//         })
//         .catch(error => {
//             addChatbotMessage(`Error: ${error.message}`);
//             console.error('Fetch error:', error);
//         });
//     } else {
//         console.log('No message to send');
//     }
// }

// function addUserMessage(text) {
//     const messageDiv = document.createElement('div');
//     messageDiv.className = 'user-message';
//     messageDiv.innerHTML = `
//         <img src="images/user-icon.png" alt="User" class="user-icon">
//         <div class="message user">${text}</div>
//     `;
//     chatContainer.appendChild(messageDiv);
//     chatContainer.scrollTop = chatContainer.scrollHeight;
//     console.log('User message added:', text);
// }

// function addChatbotMessage(text) {
//     const messageDiv = document.createElement('div');
//     messageDiv.className = 'chatbot-message';
//     messageDiv.innerHTML = `
//         <div class="message bot">${text}</div>
//         <img src="images/chatbot-icon.png" alt="Chatbot" class="chatbot-icon">
//     `;
//     chatContainer.appendChild(messageDiv);
//     chatContainer.scrollTop = chatContainer.scrollHeight;
//     console.log('Chatbot message added:', text);
// }

// uploadBtn.addEventListener('click', () => {
//     uploadPopup.style.display = 'flex';
//     imageInput.value = '';
// });

// // Hide popup when close button is clicked
// closePopup.addEventListener('click', () => {
//     uploadPopup.style.display = 'none';
// });

// // Handle image upload and text extraction
// submitImage.addEventListener('click', async () => {
//     const file = imageInput.files[0];
//     if (file) {
//         uploadPopup.style.display = 'none';
//         addUserMessage('Processing image...');

//         try {
//             // Extract text using Tesseract
//             const worker = await initWorker();
//             const { data: { text } } = await worker.recognize(file);
//             await worker.terminate();

//             const extractedText = text.trim();
//             if (!extractedText) {
//                 addChatbotMessage('No text detected in the image.');
//                 return;
//             }

//             // Show extracted text in chat
//             addUserMessage(`Extracted text: "${extractedText}"`);

//             // Send extracted text for verification
//             setTimeout(() => {
//                 fetch('http://localhost:5000/chat', {
//                     method: 'POST',
//                     headers: {
//                         'Content-Type': 'application/json',
//                     },
//                     body: JSON.stringify({
//                         message: extractedText,
//                         session_id: sessionId
//                     })
//                 })
//                 .then(response => response.json())
//                 .then(data => {
//                     if (data.error) {
//                         addChatbotMessage(data.error);
//                     } else {
//                         addChatbotMessage(`Image verification Result: ${data.response}`);
//                     }
//                 })
//                 .catch(error => {
//                     addChatbotMessage(`Error verifying text: ${error.message}`);
//                     console.error('Verification error:', error);
//                 });
//             }, 1500); // 1.5-second delay
//         } catch (error) {
//             addChatbotMessage(`Error processing image: ${error.message}`);
//             console.error('OCR error:', error);
//         }
//     } else {
//         alert('Please select an image to upload.');
//     }
// });

// document.addEventListener('DOMContentLoaded', () => {
//     console.log('DOM fully loaded');
//     addInitialMessage();
// });

// function addInitialMessage() {
//     const messageDiv = document.createElement('div');
//     messageDiv.className = 'chatbot-message';
//     messageDiv.innerHTML = `
//         <div class="message bot">What questions do you have regarding misinformation or deepfakes?</div>
//         <img src="images/chatbot-icon.png" alt="Chatbot" class="chatbot-icon">
//     `;
//     chatContainer.appendChild(messageDiv);
//     chatContainer.scrollTop = chatContainer.scrollHeight;
//     console.log('Initial message added');
// }

// // Add event listener for the Enter key
// userInput.addEventListener('keydown', (event) => {
//     if (event.key === 'Enter') {
//         event.preventDefault();
//         sendMessage();
//     }
// });



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
        if (data.error) {
            addChatbotMessage(data.error);
        } else {
            addChatbotMessage(data.response);
        }
    })
    .catch(error => {
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
            if (data.error) {
                addChatbotMessage(data.error);
            } else {
                addChatbotMessage(data.response);
            }
        })
        .catch(error => {
            addChatbotMessage(`Error: ${error.message}`);
            console.error('Fetch error:', error);
        });
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
        <div class="message bot">What questions do you have regarding misinformation or deepfakes?</div>
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
