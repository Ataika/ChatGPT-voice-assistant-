
import pyaudio
import wave
import speech_recognition as sr
import requests
from gtts import gTTS
import simpleaudio as sa

def record_voice(filename, duration=5):
    chunk = 1024
    format = pyaudio.paInt16
    channels = 1
    rate = 44100

    p = pyaudio.PyAudio()
    stream = p.open(format=format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)

    print("Recording...")
    frames = []

    for i in range(0, int(rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)

    print("Finished recording.")
    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()

def recognize_speech_from_file(filename):
    r = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio_data = r.record(source)
        try:
            text = r.recognize_google(audio_data, language='ru-RU')
            return text
        except sr.UnknownValueError:
            return "Google Speech Recognition could not understand audio"
        except sr.RequestError as e:
            return "Could not request results from Google Speech Recognition service; {0}".format(e)

def send_text_to_chatbot(text, api_key):
    url = "Your URL"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "prompt": text,
        "max_tokens": 200  # Установим лимит токенов для ответа
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        return response.json()["choices"][0]["text"].strip()
    else:
        return "Error: " + response.text

def text_to_speech(text, lang='ru'):
    tts = gTTS(text=text, lang=lang)
    filename = 'response_audio.mp3'
    tts.save(filename)
    return filename

def play_audio(filename):
    wave_obj = sa.WaveObject.from_wave_file(filename)
    play_obj = wave_obj.play()
    play_obj.wait_done()

def main():
    filename = "my_voice_recording.wav"
    api_key = 'your API key'

    record_voice(filename)
    text = recognize_speech_from_file(filename)
    print("Recognized Text:", text)

    response_text = send_text_to_chatbot(text, api_key)
    print("Text Response from ChatGPT:", response_text)

    audio_file = text_to_speech(response_text)

    # Конвертация MP3 в WAV для воспроизведения

    # Преобразование текстового ответа в аудио
    audio_file = text_to_speech(response_text)

    play_audio(audio_file)


if __name__ == "main":
    main()