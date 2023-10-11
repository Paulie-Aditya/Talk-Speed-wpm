# Talk Speed Research

import wave
from api_communication import *

filename = "input.wav"

obj = wave.open(filename,"rb")

sample_freq = obj.getframerate()
n_samples = obj.getnframes()
obj.close()

t_audio =  n_samples/sample_freq  # total time in seconds.

print(f'Length of Audio: {t_audio}')

audio_url = upload(filename)
number_of_words = save_transcript(audio_url=audio_url, filename=filename)

print(f"Words per minute: {int((number_of_words/t_audio)*60)}")



