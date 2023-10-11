import speech_recognition
import wave


filename = "input.wav"
recognizer = speech_recognition.Recognizer()

def mic_check():
    with speech_recognition.Microphone() as mic:
        print("Mic Adjusting")
        recognizer.adjust_for_ambient_noise(mic, duration = 5)
        print("Mic Started")
        audio = recognizer.listen(mic, timeout=60)
        with open(filename, "wb") as f:
            f.write(audio.get_wav_data())
        
        print("Audio Done")
        return transcribe(audio)


def transcribe(audio):
    text = recognizer.recognize_google(audio)
    print(text)
    return text

def length_of_audio(filename):
    obj = wave.open(filename,"rb")
    sample_freq = obj.getframerate()
    n_samples = obj.getnframes()
    obj.close()
    return n_samples/sample_freq

def main():
    text = mic_check()
    time = length_of_audio(filename)
    number_of_words = len(text.split(" "))
    print("No. of words: ", number_of_words)
    print("Audio Length: ", time)

    print("Words per minute: " , int((number_of_words/time)*60))


main()