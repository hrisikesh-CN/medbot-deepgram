from src.components.audio_io.speech_to_text import SpeechToText
from src.components.llm_components.llm_response import LanguageModelProcessor
from src.components.audio_io.text_to_speech import TextToSpeech


class Agent:
    def __init__(self):
        self.llm = LanguageModelProcessor()
        self.stt = SpeechToText()
        self.tts = TextToSpeech()

    async def main(self):

        # Loop indefinitely until "goodbye" is detected
        while True:
            await self.stt.get_transcript()
            transcription_response = self.stt.final_transcription_response
            print("User: ", transcription_response)
            llm_response = self.llm.process(transcription_response)
            print("llm response: %s" % llm_response)
            self.tts.play_audio_from_bytes(text=llm_response)


