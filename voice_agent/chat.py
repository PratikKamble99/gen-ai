import speech_recognition as sr
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

#------ASYNC OPEN AI-----#
import asyncio
from openai import AsyncOpenAI
from openai.helpers import LocalAudioPlayer

openai = AsyncOpenAI()

client = OpenAI()

async def tts(speech: str) -> None:
    async with openai.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="coral",
        input=speech,
        instructions="Speak in a cheerful and positive tone.",
        response_format="pcm",
    ) as response:
        await LocalAudioPlayer().play(response)

def main():
    r = sr.Recognizer() # Speech to text

    with sr.Microphone() as source: # Mic Access
        r.adjust_for_ambient_noise(source)
        r.pause_threshold = 2

        print("Speak something..")
        audio = r.listen(source)

        print('Processing Audio')

        stt = r.recognize_google(audio)

        SYSTEM_PROMPT=""" 
            You are an expert voice agent. You are given the transcript of what user has said using voice. 
            You need to output as if you are an voice agent and what ever you speak 
            will be converted back to audio using AI and played back to user.
         """

        client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role":"system", "content": SYSTEM_PROMPT},
                {"role":"user", "content":stt}
            ]
        )

        print(f"You said: {stt}")
        asyncio.run(tts(speech=stt))

main()
