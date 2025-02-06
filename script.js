const ENDPOINT = "http://localhost:11434/api/generate";

const formElement = document.getElementById("form");
const responseElement = document.getElementById("response");
const inputElement = document.getElementById("input");

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
  const prompt = inputElement.value;

  const requestBody = {
    model: "deepseek-r1:32b",
    prompt,
  };
  try {
    responseElement.innerText = "Loading...";

    const response = await fetch(ENDPOINT, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(requestBody),
    });
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
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
      responseElement.innerText += current.response;
    }
  } catch (error) {
    console.error("Error:", error);
  } finally {
    formElement.reset();
  }
});
