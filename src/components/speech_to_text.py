import asyncio
import sys

from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    LiveTranscriptionEvents,
    LiveOptions,
    Microphone)
from dotenv import load_dotenv

load_dotenv()

from src.constant import *
from src.exception import CustomException

# def py_error_handler(filename, line, function, err, fmt):
#     None


# ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
# c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

# asound = cdll.LoadLibrary('libasound.so')
# asound.snd_lib_error_set_handler(c_error_handler)

# brew install portaudio

# Load environment variables

# Set your Deepgram API Key and desired voice model
# DG_API_KEY = os.getenv("DEEPGRAM_API_KEY")
MODEL_NAME = "aura-asteria-en"  # Example model name, change as needed


class TranscriptCollector:

    def __init__(self):
        self.final_transcription = None
        self.transcription = None
        self.reset()

    def add_part(self, text: str):
        self.transcription.append(text)

    def reset(self):
        self.transcription = []

    def form_final_transcription(self,
                                 speech_final: str = None,
                                 ):
        try:
            if not speech_final:  # implementation for utterance end
                if not self.final_transcription:  # if is_final is not in http response

                    self.final_transcription = " ".join(self.transcription)

            else:  # implementation for is_final response

                self.add_part(speech_final)
                self.final_transcription = " ".join(self.transcription)

        except Exception as e:
            raise CustomException(e, sys)


class SpeechToText:

    def __init__(cls):
        cls.transcript_collector = TranscriptCollector()
        cls.final_transcription_response = None

    async def get_transcript(cls):
        transcription_complete = asyncio.Event()

        try:
            config = DeepgramClientOptions(options={"keepalive": "true"})
            deepgram: DeepgramClient = DeepgramClient(api_key=DEEPGRAM_API_KEY, config=config)

            dg_connection = deepgram.listen.asynclive.v("1")

            async def on_message(self, result, **kwargs):
                sentence = result.channel.alternatives[0].transcript
                confidence = result.channel.alternatives[0].confidence
                if len(sentence) == 0:
                    return
                if result.is_final:
                    # We need to collect these and concatenate them together when we get a speech_final=true
                    # See docs: https://developers.deepgram.com/docs/understand-endpointing-interim-results

                    # Speech Final means we have detected sufficent silence to consider this end of speech Speech
                    # final is the lowest latency result as it triggers as soon an the endpointing value has triggered
                    if result.speech_final:
                        cls.transcript_collector.form_final_transcription(speech_final=sentence)
                        final_transcription = cls.transcript_collector.final_transcription
                        print(f"Speech Final: {final_transcription}")
                        cls.final_transcription_response = final_transcription
                        # callback(cls.final_transcription_response)
                        cls.transcript_collector.reset()
                        transcription_complete.set()




                    else:
                        # These are useful if you need real time captioning and update what the Interim Results produced
                        cls.transcript_collector.add_part(sentence)
                        # print(f"Is Final: {sentence}")
                else:
                    # These are useful if you need real time captioning of what is being spoken
                    print(f"Interim Results: {sentence}")
                    print("condifence", confidence)

            async def on_error(self, error, **kwargs):
                print(f"\n\n{error}\n\n")

            async def on_utterance_end(self, utterance_end, **kwargs):

                if not cls.final_transcription_response:

                    if cls.transcript_collector.transcription and \
                            len(cls.transcript_collector.transcription) > 0:
                        cls.transcript_collector.form_final_transcription()
                        print("Speaker: ", cls.transcript_collector.final_transcription)
                        cls.final_transcription_response = cls.transcript_collector.final_transcription
                        # callback(cls.final_transcription_response)
                        cls.transcript_collector.reset()
                        transcription_complete.set()
                    # cls.final_transcription_response = cls.transcript_collector.final_transcription
                transcription_complete.clear()

            dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)
            dg_connection.on(LiveTranscriptionEvents.Error, on_error)
            dg_connection.on(LiveTranscriptionEvents.UtteranceEnd, on_utterance_end)


            options = LiveOptions(
                language="en-US",
                model="nova",
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

                endpointing=300)

            addons = {
                # Prevent waiting for additional numbers
                "no_delay": "true"
            }

            print("\n\nStart talking! Press Ctrl+C to stop...\n")

            await dg_connection.start(options, addons=addons)

            # Open a microphone stream on the default input device
            microphone = Microphone(dg_connection.send)
            microphone.start()

            await transcription_complete.wait()

            # Wait for the microphone to close
            microphone.finish()

            # Indicate that we've finished
            await dg_connection.finish()

        except Exception as e:
            raise CustomException(e, sys)
