import requests
from dotenv import load_dotenv
import subprocess
import shutil
import time
from deepgram import Deepgram
from ctypes import *


def py_error_handler(filename, line, function, err, fmt):
    None


ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

asound = cdll.LoadLibrary('libasound.so')
asound.snd_lib_error_set_handler(c_error_handler)

# brew install portaudio

# Load environment variables
load_dotenv()

# Set your Deepgram API Key and desired voice model
# DG_API_KEY = os.getenv("DEEPGRAM_API_KEY")
MODEL_NAME = "aura-asteria-en"  # Example model name, change as needed

import asyncio
from dotenv import load_dotenv

from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    LiveTranscriptionEvents,
    LiveOptions,
    Microphone,
)

load_dotenv()


class TranscriptCollector:

    def __init__(self):
        self.final_transcription = None
        self.transcription = None
        self.reset()

    def add_part(self, text: str):
        self.transcription.append(text)

    def reset(self):
        self.transcription = []

    def form_final_transcription(self, speech_final: str = None):
        if not speech_final:   # implementation for utterance end
            if not self.final_transcription:  # if is_final is not in http response

                self.final_transcription = " ".join(self.transcription)


        else:  # implementation for is_final response

            self.add_part(speech_final)
            self.final_transcription = " ".join(self.transcription)



class SpeechToText:

    def __init__(cls):
        cls.transcript_collector = TranscriptCollector()

    async def get_transcript(cls):
        try:
            config = DeepgramClientOptions(options={"keepalive": "true"})
            deepgram: DeepgramClient = DeepgramClient("", config)

            dg_connection = deepgram.listen.asynclive.v("1")

            async def on_message(self, result, **kwargs):
                sentence = result.channel.alternatives[0].transcript
                if len(sentence) == 0:
                    return
                if result.is_final:
                    # We need to collect these and concatenate them together when we get a speech_final=true
                    # See docs: https://developers.deepgram.com/docs/understand-endpointing-interim-results

                    # Speech Final means we have detected sufficent silence to consider this end of speech Speech
                    # final is the lowest latency result as it triggers as soon an the endpointing value has triggered
                    if result.speech_final:
                        cls.transcript_collector.form_final_transcription(speech_final=sentence)
                        print(f"Speech Final: {cls.transcript_collector.final_transcription}")

                    else:
                        # These are useful if you need real time captioning and update what the Interim Results produced
                        cls.transcript_collector.add_part(sentence)
                        # print(f"Is Final: {sentence}")
                else:
                    # These are useful if you need real time captioning of what is being spoken
                    print(f"Interim Results: {sentence}")

            async def on_error(self, error, **kwargs):
                print(f"\n\n{error}\n\n")

            async def on_utterance_end(self, utterance_end, **kwargs):

                if cls.transcript_collector.transcription and \
                        len(cls.transcript_collector.transcription) > 0:
                    cls.transcript_collector.form_final_transcription()
                    print("Speaker: ", cls.transcript_collector.final_transcription)
                    cls.transcript_collector.reset()

            dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)
            dg_connection.on(LiveTranscriptionEvents.Error, on_error)
            dg_connection.on(LiveTranscriptionEvents.UtteranceEnd, on_utterance_end)

            options = LiveOptions(
                language="en-US",
                model="nova-2",
                smart_format=True,
                # punctuate=True,
                encoding="linear16",
                channels=1,
                sample_rate=16000,
                # To get UtteranceEnd, the following must be set:
                interim_results=True,
                utterance_end_ms="1000",
                vad_events=True,
                # Time in milliseconds of silence to wait for before finalizing speech

                endpointing=300,

            )

            addons = {
                # Prevent waiting for additional numbers
                "no_delay": "true"
            }

            print("\n\nStart talking! Press Ctrl+C to stop...\n")
            if await dg_connection.start(options, addons=addons) is False:
                print("Failed to connect to Deepgram")
                return

            # Open a microphone stream on the default input device
            microphone = Microphone(dg_connection.send)

            # start microphone
            microphone.start()

            while True:
                if not microphone.is_active():
                    break
                await asyncio.sleep(1)

            # Wait for the microphone to close
            microphone.finish()

            # Indicate that we've finished
            dg_connection.finish()

            print("Finished")

        except Exception as e:
            print(f"Could not open socket: {e}")
            return


if __name__ == "__main__":
    stt = SpeechToText()
    asyncio.run(stt.get_transcript())
