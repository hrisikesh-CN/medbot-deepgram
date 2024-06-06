from src.components.speech_to_text import SpeechToText
from src.components.llm_response import LanguageModelProcessor
from src.components.text_to_speech import TextToSpeech


class Agent:
    def __init__(self):
        # self.transcription_response = ""
        self.llm = LanguageModelProcessor()
        self.stt = SpeechToText()
        self.tts = TextToSpeech()

    async def main(self):
        def get_transcription_callback(final_transcription):
            self.transcription_response = final_transcription

        # Loop indefinitely until "goodbye" is detected
        while True:
            await self.stt.get_transcript()
            transcription_response = self.stt.final_transcription_response
            print("User: ", transcription_response)
            llm_response = self.llm.process(transcription_response)
            print("llm response: %s" % llm_response)
            self.tts.play_audio_from_bytes(text=llm_response)


            #
            # # Reset transcription_response for the next loop iteration
            # self.transcription_response = ""
