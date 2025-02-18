
def generate_speech(text):
    from kokoro import KPipeline

    from IPython.display import display, Audio

    import soundfile as sf

    pipeline = KPipeline(lang_code='en-US')
    generator = pipeline.generate_from_tokens(text, voice="en-US-Neural2-A", speed=1, split_pattern=r'\n+')

    for i, audio in enumerate(generator):
        sf.write(f'output_{i}.wav', audio, 24000)
        display(Audio(audio, rate=24000, autoplay=True))
