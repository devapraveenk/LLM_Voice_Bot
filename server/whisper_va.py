from pydub import AudioSegment
from gtts import gTTS
from pydub.playback import play
from lightning_rag import rag_chain, conversation
import os
from playaudio import playaudio

# import wave
# import pyaudio
# import playsound
import threading

# os.environ["PATH"] += os.pathsep + r"C:\Users\navab\Downloads\ticketbooking-bot\ffpemg_downloaders"
# os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
# from teest_rag import conversational_rag_chain

# import pydub
# pydub.AudioSegment.converter = r"C:\Users\navab\Downloads\ticketbooking-bot\ffpemg_downloaders\ffmpeg.exe"
import pyaudio
import wave

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 7
WAVE_OUTPUT_FILENAME = "voice.wav"


def record():
    p = pyaudio.PyAudio()

    stream = p.open(
        format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK
    )

    print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, "wb")
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b"".join(frames))
    wf.close()


from groq import Groq

os.environ["GROQ_API_KEY"] = "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"

client = Groq()

from langchain_core.messages import AIMessage, HumanMessage


def record_audio(file_path):

    print("transcribing........")
    with open(file_path, "rb") as file:
        transcription = client.audio.transcriptions.create(
            file=(file_path, file.read()),  # Required audio file
            model="whisper-large-v3-turbo",  # Required model to use for transcription
            # prompt="Specify context or spelling",  # Optional
            response_format="json",  # Optional
            # Optional
            temperature=0.0,  # Optional
        )
    print(f"user: {transcription.text}")
    return transcription.text


def mac_text_to_speech(text):
    file_path = "audio_assets/welcome.mp3"
    myobj = gTTS(text=text, slow=False)
    myobj.save(file_path)

    playaudio(file_path)


def text_to_speech(text):
    file_path = "audio_assets/welcome.mp3"
    myobj = gTTS(text=text, slow=False)
    myobj.save(file_path)

    audio = AudioSegment.from_file(file_path)
    play(audio)
    if os.path.exists(file_path):
        os.remove(file_path)


import uuid

id = None


def set_id():
    global id
    id = uuid.uuid4()


chat_history = []


def llm_result(question):
    response = rag_chain.invoke({"input": question, "chat_history": chat_history})
    print(question)
    chat_history.extend(
        [
            HumanMessage(content=question),
            AIMessage(content=response["answer"]),
        ]
    )

    #     response = conversational_rag_chain.invoke(
    #     {"input": question},
    #     config={
    #         "configurable": {"session_id": id}
    #     },  # constructs a key "abc123" in `store`.
    # )["answer"]
    #     return response
    # response = conversation.predict(input=question)
    # print(response['answer'])

    return response["answer"]


def response():
    transcriptions = record_audio("voice.wav")
    result = llm_result(transcriptions)
    print(f"bot:{result}")
    mac_text_to_speech(result)
    return transcriptions, result


def main():
    while True:
        record()
        tr, res = response()
        if "exit" in tr or "bye" in tr:
            break


main()
