// Selecting elements from the DOM
const chatForm = document.getElementById("chat-form");
const chatInput = document.getElementById("chat-input");
const chatHistory = document.getElementById("chat-history");

// Event listener for form submission
chatForm.addEventListener("submit", function (event) {
  event.preventDefault(); // Prevent default form submission
  const message = chatInput.value.trim(); // Get and trim input value

  if (message) {
    // Add the user's message to the chat history
    const userMessage = createMessageElement(message, "user");
    chatHistory.appendChild(userMessage);

    // Clear the input field
    chatInput.value = "";

    // Add an "AI is typing..." indicator
    const typingIndicator = createMessageElement(
      "AI is typing...",
      "ai-typing"
    );
    chatHistory.appendChild(typingIndicator);

    // Scroll to the bottom of the chat history
    chatHistory.scrollTop = chatHistory.scrollHeight;

    // Send the message to the server
    fetch("/index/response", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: new URLSearchParams({
        csrfmiddlewaretoken: document.querySelector(
          "[name=csrfmiddlewaretoken]"
        ).value,
        message: message,
      }),
    })
      .then((response) => {
        // Check for a valid response
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json(); // Parse JSON response
      })
      .then((data) => {
        const response = data.response; // Extract AI response text
        const audioUrl = data.audio_url; // Extract audio URL

        // Remove the typing indicator
        chatHistory.removeChild(typingIndicator);

        // Add the AI's response to the chat history
        const aiMessage = createMessageElement(response, "ai", audioUrl);
        chatHistory.appendChild(aiMessage);

        // Automatically play the audio response
        playAudio(audioUrl);

        // Scroll to the bottom of the chat history
        chatHistory.scrollTop = chatHistory.scrollHeight;
      })
      .catch((error) => {
        console.error("Error:", error);

        // Remove the typing indicator
        chatHistory.removeChild(typingIndicator);

        // Add an error message to the chat history
        const errorMessage = createMessageElement(
          "Oops! Something went wrong. Please try again later.",
          "error"
        );
        chatHistory.appendChild(errorMessage);

        // Scroll to the bottom of the chat history
        chatHistory.scrollTop = chatHistory.scrollHeight;
      });
  }
});

// Helper function to create chat message elements
function createMessageElement(content, sender, audioUrl = null) {
  // Create a wrapper for the message
  const messageWrapper = document.createElement("div");
  messageWrapper.classList.add("chat-message", sender);

  // Create the actual message element
  const messageElement = document.createElement("div");
  messageElement.classList.add("message", sender);
  messageElement.textContent = content;

  messageWrapper.appendChild(messageElement);

  // Add a replay button if audio URL is provided
  if (audioUrl) {
    const replayButton = document.createElement("button");
    replayButton.textContent = "Replay";
    replayButton.classList.add("replay-btn");
    replayButton.addEventListener("click", () => {
      playAudio(audioUrl);
    });
    messageWrapper.appendChild(replayButton);
  }

  return messageWrapper;
}

// Helper function to play audio
function playAudio(audioUrl) {
  const audio = new Audio(audioUrl);
  audio.play().catch((error) => {
    console.error("Audio playback failed:", error);
  });
}

