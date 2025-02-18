## API Tutorial files

This is a collection of several tutorial and demos about AI APIs.

### Basic tutorial

The basic tutorial is in the "python/tutorial.ipynb" file. It is a Jupyter notebook that can be run in a Jupyter environment. It demonstrates how to use the remove OpenAI API to generate text.

1. To use, you need to have a OpenAI API key. You can get one from https://platform.openai.com/api-keys.

2. Follow the instructions in the Jupyter notebook file "python/tutorial.ipynb" to run the tutorial. You can open it in a Jupyter environment or use an IDE like VSCode that supports Jupyter notebooks.

### More involved: Web client and server demo for text streaming

Directory "client" contains a simple browser client that connects to two different local servers. The text streaming server is interacted with "Send Text" button and the audio streaming server is interacted with "Send Audio" button.

The text streaming server code is in the "server" directory.

1. To use the text streaming server, you need to have Ollama installed and running. You can get it from https://ollama.ai/.

2. Open the client by opening the "client/index.html" file in a browser.

3. Make sure that you have Node installed. You can get it from https://nodejs.org/.

4. Install the dependencies by running `npm install` in the "server" directory.

5. Start the server by running `npm run dev` in the "server" directory.

and the audio streaming server code is in the "python/text_to_speech" file.

There's also an audio streaming server, which is currently commented out in the client code because the TTS service is slow in its current configuration.
