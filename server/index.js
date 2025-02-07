const ENDPOINT = "http://localhost:11434/api/generate";

const express = require("express");
const bodyParser = require("body-parser");
const cors = require("cors");

const app = express();
const port = 3000;

app.use(bodyParser.json(), cors());

app.post("/api/prompt", async (req, res) => {
  const { prompt } = req.body;

  if (!prompt) {
    return res.status(400).json({ error: "Prompt is required" });
  }

  console.log("Received prompt:", prompt);

  try {
    const response = await fetch(ENDPOINT, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        model: "deepseek-r1:32b",
        prompt,
        stream: true,
      }),
    });
    if (!response.ok) {
      res.status(500).json({ error: "Internal Server Error" });
      return;
    }
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    res.setHeader("Content-Type", "application/x-ndjson");
    res.setHeader("Cache-Control", "no-cache");
    res.setHeader("Connection", "keep-alive");
    res.status(200);
    let current = {};
    while (true) {
      const { done, value } = await reader.read();
      if (done) {
        console.log("Stream finished");
        break;
      }
      console.log("Received chunk:", decoder.decode(value, { stream: true }));
      current = JSON.parse(decoder.decode(value, { stream: true }));
      res.write(
        JSON.stringify({
          response: current.response,
          done: current.done,
        })
      );

      if (current.done) {
        res.end();
        break;
      }
    }
  } catch (error) {
    console.error("Error:", error);
    res.status(500).json({ error: "Internal Server Error" });
  }
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
