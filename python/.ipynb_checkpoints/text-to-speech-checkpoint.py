from kokoro import KPipeline

from IPython.display import display, Audio

import soundfile as sf

pipeline = KPipeline(lang_code='en-US')

text = """
The sky is blue.
The sun is bright.
The grass is green.
The trees are tall.
"""

generator = pipeline.generate(text, voice="en-US-Neural2-A", speed=1, split_pattern=r'\n+')

for i, audio in enumerate(generator):
    sf.write(f'output_{i}.wav', audio, 24000)
    display(Audio(audio, rate=24000, autoplay=True))
print('Done!')  