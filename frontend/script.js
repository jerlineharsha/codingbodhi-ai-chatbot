const chatbotButton = document.getElementById("chatbotButton");
const chatbotWindow = document.getElementById("chatbotWindow");
const closeButton = document.getElementById("closeButton");
const newChatButton = document.getElementById("newChatButton");
const chatMessages = document.getElementById("chatMessages");
const userInput = document.getElementById("userInput");
const sendButton = document.getElementById("sendButton");

const USER_ID_KEY = "codingbodhi.userId";
const CONVERSATION_ID_KEY = "codingbodhi.conversationId";
const WELCOME_MESSAGE = `👋 Hello! Welcome to CodingBodhi!

How can we help you today?

1️⃣ Courses
2️⃣ Internships
3️⃣ Services
4️⃣ Contact Us`;
document.getElementById("welcomeMessage").textContent = WELCOME_MESSAGE;
let userId = Number(localStorage.getItem(USER_ID_KEY));
if (!Number.isSafeInteger(userId) || userId < 1) {
    userId = Math.floor(Math.random() * 1_000_000_000) + 1;
    localStorage.setItem(USER_ID_KEY, String(userId));
}

let conversationId = Number(localStorage.getItem(CONVERSATION_ID_KEY)) || null;
let isSending = false;
let conversationReady = Promise.resolve();

chatbotButton.addEventListener("click", () => {
    chatbotWindow.style.display = "flex";
    chatbotButton.style.display = "none";
    scrollToBottom();
    userInput.focus();
});

closeButton.addEventListener("click", () => {
    chatbotWindow.style.display = "none";
    chatbotButton.style.display = "flex";
});

newChatButton.addEventListener("click", () => {
    if (isSending) {
        return;
    }

    conversationId = null;
    localStorage.removeItem(CONVERSATION_ID_KEY);
    chatMessages.replaceChildren();
    addMessage(WELCOME_MESSAGE, "bot");
    userInput.focus();
});

function scrollToBottom() {
    requestAnimationFrame(() => {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    });
}

function addMessage(message, sender) {
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message", sender === "user" ? "user-message" : "bot-message");

    const content = document.createElement("div");
    content.classList.add("message-content");

    const paragraph = document.createElement("p");
    paragraph.textContent = message;
    content.appendChild(paragraph);
    messageDiv.appendChild(content);
    chatMessages.appendChild(messageDiv);
    scrollToBottom();

    return messageDiv;
}

async function loadConversation() {
    if (!conversationId) {
        return;
    }

    try {
        const response = await fetch(
            `/conversations/${conversationId}/messages?user_id=${userId}`
        );
        if (!response.ok) {
            if (response.status === 404) {
                conversationId = null;
                localStorage.removeItem(CONVERSATION_ID_KEY);
            }
            return;
        }

        const data = await response.json();
        chatMessages.replaceChildren();
        data.messages.forEach((message) => addMessage(message.message, message.sender));
    } catch (error) {
        console.error("Could not restore chat history:", error);
    }
}

async function sendMessage(message) {
    message = message.trim();
    if (!message || isSending) {
        return;
    }

    isSending = true;
    sendButton.disabled = true;
    userInput.disabled = true;
    newChatButton.disabled = true;
    let typingMessage;

    try {
        await conversationReady;
        addMessage(message, "user");
        userInput.value = "";
        typingMessage = addMessage("Typing...", "bot");

        const response = await fetch("/chat", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            signal: AbortSignal.timeout(60000),
            body: JSON.stringify({
                user_id: userId,
                conversation_id: conversationId,
                message,
            }),
        });

        const data = await response.json();
        if (!response.ok) {
            const detail = typeof data.detail === "string"
                ? data.detail
                : "The message could not be sent. Please try again.";
            throw new Error(detail);
        }

        conversationId = data.conversation_id;
        localStorage.setItem(CONVERSATION_ID_KEY, String(conversationId));
        typingMessage.remove();
        addMessage(data.bot_message, "bot");
    } catch (error) {
        console.error("Chatbot error:", error);
        if (typingMessage) {
            typingMessage.remove();
        }
        const errorMessage = error.name === "TimeoutError"
            ? "The response is taking too long. Please try again."
            : error instanceof TypeError
                ? "Can't reach the chatbot server. Refresh this page and make sure the backend is running."
            : error.message || "Could not connect to the chatbot. Please try again.";
        addMessage(errorMessage, "bot");
    } finally {
        isSending = false;
        sendButton.disabled = false;
        userInput.disabled = false;
        newChatButton.disabled = false;
        userInput.focus();
    }
}

sendButton.addEventListener("click", () => sendMessage(userInput.value));

userInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        sendMessage(userInput.value);
    }
});

conversationReady = loadConversation();
