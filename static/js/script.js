const chatForm = document.getElementById('chat-form');
const chatInput = document.getElementById('chat-input');
const chatHistory = document.getElementById('chat-history');

chatForm.addEventListener('submit', function (event) {
    event.preventDefault();
    const message = chatInput.value.trim()
    if (message) {
        const messageWrapper = document.createElement('div');
        messageWrapper.classList.add('chat-message', 'user');

        const messageElement = document.createElement('div');
        messageElement.classList.add('message', 'user');
        messageElement.textContent = message;

        messageWrapper.appendChild(messageElement);
        chatHistory.appendChild(messageWrapper);
        chatInput.value = '';

        fetch("/index/response", {
          method: "POST",
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
          body: new URLSearchParams({
            csrfmiddlewaretoken: document.querySelector(
              "[name=csrfmiddlewaretoken]"
            ).value,
            message: message,
          }),
        })
          .then((response) => {
            if (!response.ok) throw new Error("Network response was not ok");
            return response.json();
          })
          .then((data) => {
            const response = data.response;
            const messageWrapper2 = document.createElement("div");
            messageWrapper2.classList.add("chat-message", "ai");

            const messageElement2 = document.createElement("div");
            messageElement2.classList.add("message", "ai");
            messageElement2.textContent = response;

            messageWrapper2.appendChild(messageElement2);
            chatHistory.appendChild(messageWrapper2);
          });


        chatHistory.scrollTop = chatHistory.scrollHeight;
    }
})
