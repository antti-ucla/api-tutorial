## API Tutorial files

This is a collection of several tutorial and demos about AI APIs.

### Basic tutorial

The basic tutorial is in the `python/tutorial.ipynb` file. It is a Jupyter notebook that can be run in a Jupyter environment. It demonstrates how to use the remove OpenAI API to generate text.

1. To use, you need to have a OpenAI API key. You can get one from https://platform.openai.com/api-keys.

2. Follow the instructions in the Jupyter notebook file `python/tutorial.ipynb` to run the tutorial. You can open it in a Jupyter environment or use an IDE like VSCode that supports Jupyter notebooks.

### A bit more involved demo: Web client and server demo for text streaming

The directory `client` contains a simple browser client that allows you prompt a local chat AI model and get the responses as a stream of text. The server for it is in the `python/text_streaming.py` file.

1. To use the text streaming server, you need to have Ollama installed and running. You can get it from https://ollama.ai/.

2. You need to download the "deepseek-r1:7b" model from Ollama and start it. You can do this by running `ollama run deepseek-r1:7b` in a terminal.

3. Open the client by opening the "client/index.html" file in a browser.

4. Start the text streaming server by first running `cd ~/api-tutorial/python` in a terminal and then `pipenv run python3 text_streaming.py`.

### Other in progress work

There's also an audio streaming server, which is currently commented out in the client code because the TTS service is slow in its current configuration.
