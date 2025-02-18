const TEXT_ENDPOINT = "http://localhost:8001/api/prompt";
const AUDIO_ENDPOINT = "http://localhost:8000/stream_audio";

const formElement = document.getElementById("form");
const responseElement = document.getElementById("response");
const inputElement = document.getElementById("input");

const audioContext = new (window.AudioContext || window.webkitAudioContext)();
let sourceNode = null;

if (!formElement) {
  throw new Error("Form element not found");
}

if (!responseElement) {
  throw new Error("Response element not found");
}

if (!inputElement) {
  throw new Error("Input element not found");
}

formElement.addEventListener("submit", async (event) => {
  event.preventDefault();

  const textButton = document.getElementById("text-button");
  //const audioButton = document.getElementById("audio-button");

  if (!textButton) {
    throw new Error("Text button not found");
  }

  textButton.disabled = true;
  //audioButton.disabled = true;

  const prompt = inputElement.value;

  const button = event.submitter;

  try {
    responseElement.innerText = "Loading...";

    switch (button.id) {
      case "text-button":
        await handleTextStream(prompt);
        break;
      case "audio-button":
        await handleAudioStream(prompt);
        break;
      default:
        throw new Error("Unknown button clicked");
    }
  } catch (error) {
    console.error("Error:", error);
    responseElement.innerText = "Error: " + error.message;
  } finally {
    formElement.reset();
    textButton.disabled = false;
    //audioButton.disabled = false;
  }
});

/**
 * @argument {string} prompt
 */
const handleAudioStream = (prompt) => {
  try {
    const audioElement = document.getElementById("audio");
    audioElement.src = `${AUDIO_ENDPOINT}?prompt=${encodeURIComponent(prompt)}`;
    audioElement.play();
    responseElement.innerText = "Playing audio...";
  } catch (error) {
    console.error("Error:", error);
    responseElement.innerText = "Error: " + error.message;
  }
};

/**
 * @argument {string} prompt
 */
const handleTextStream = async (prompt) => {
  const response = await fetch(TEXT_ENDPOINT, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ prompt }),
  });

  responseElement.innerText = "";
  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let current = {};
  while (true) {
    const { done, value } = await reader.read();
    if (done) {
      console.log("Stream finished");
      break;
    }
    current = JSON.parse(decoder.decode(value, { stream: true }));
    if (current.done) {
      console.log("done received");
      break;
    }
    responseElement.innerText += current.message.content;
  }
};
