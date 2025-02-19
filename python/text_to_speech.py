from fastapi import FastAPI, Request, Query
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from ollama import Client
import kokoro
import pyaudio
from queue import Queue
from threading import Thread
import time
import sys

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pipeline = kokoro.KPipeline('a')

p = pyaudio.PyAudio()

client = Client(host='http://localhost:11434/')

# A small server that streams audio from a text prompt. First the text is sent to the chat model and then the text is sent to the text-to-speech model.
# Currently not working fast because the text-to-speech model is running only on one CPU core. I have to add multi-threading to make it work faster.
@app.get('/stream_audio')
async def stream_audio(request: Request, prompt: str = Query(...) ):
    print('prompt: ' + str(prompt))

    # queue for audio chunks
    audio_queue = Queue()

    # queue for sentences
    sentence_queue = Queue()

    stream = p.open(format=pyaudio.paFloat32, channels=1, rate=24000, output=True)
    stream.start_stream()
    stream.get_read_available()

    def is_sentence_end(text):
        return text.endswith('.') or text.endswith('!') or text.endswith('?')

    def chat_worker(sentence_queue: Queue):
        words = []

        for response in client.chat(model='deepseek-r1:7b', messages=[{'role': 'user', 'content': prompt}], stream=True):
            text_chunk = response['message']['content']
            done = response['done']
            if done:
                sentence_queue.put(None)
                print('chat_worker done')
                break
            words.append(text_chunk)
            if (is_sentence_end(text_chunk)):
                sentence = ''.join(words)
                words = []
                print('sentence: ' + str(sentence))
                sentence_queue.put(sentence)
                time.sleep(0.1)


    chat_thread= Thread(target=chat_worker, args=(sentence_queue,))
    chat_thread.start()

    def audio_worker(sentence_queue: Queue, audio_queue: Queue):
        while True:
            if (sentence_queue.empty()):
                print('no work for audio_worker')
                time.sleep(0.2)
                continue
            else:
                next_sentence = sentence_queue.get()
                print('next_sentence: ' + str(next_sentence))
                if next_sentence is None:
                    audio_queue.put(None)
                    break
                print('next_sentence: ' + str(next_sentence))
                phoneme, _ = pipeline.g2p(next_sentence)
                print('phoneme: ' + str(phoneme))
                start_time = time.time()
                print('start_time: ' + str(start_time))
                for result in pipeline.generate_from_tokens(tokens=phoneme, speed=1, voice="af_heart"):
                    print('time since start: ' + str(time.time() - start_time))
                    audio_queue.put(result.audio.numpy().tobytes())
                    time.sleep(0.01)

    audio_thread = Thread(target=audio_worker, args=(sentence_queue, audio_queue,))
    audio_thread.start()

    def stream_worker(audio_queue: Queue):
        while True:
            if (audio_queue.empty()):
                print('no work for stream_worker')
                time.sleep(0.2)
                continue
            else:
                print('stream_worker working')
                audio_chunk = audio_queue.get()
                if audio_chunk is None:
                    print('stream_worker finished')
                    stream.stop_stream()
                    break
                print('audio_chunk size: ' + str(sys.getsizeof(audio_chunk)))
                if (stream.get_write_available() > 0):
                    stream.write(audio_chunk)

    stream_thread = Thread(target=stream_worker, args=(audio_queue,))
    stream_thread.start()

    def streaming_generator():
        while True:
            if (stream.get_read_available() > 10):
                stream_chunk = stream.read(10)
                print('stream_chunk: ' + str(stream_chunk))
                yield stream_chunk
            if not stream.is_active():
                yield stream.read(stream.get_read_available())
                break

    return StreamingResponse(streaming_generator(), media_type='audio/wav')

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
