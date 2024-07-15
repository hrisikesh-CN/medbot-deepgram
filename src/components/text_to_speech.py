from io import BytesIO

import requests
from pydub import AudioSegment
from pydub.playback import play

from src.constant import *


class TextToSpeech:
    def __init__(self):

        try:
            self.api_key = DEEPGRAM_API_KEY
        except Exception:
            raise EnvironmentError("DEEPGRAM_API_KEY is not set")

    def get_audio_response(self, text: str,
                           model_name: str = "aura-helios-en",

                           ):

        # Define the API endpoint
        url = f"https://api.deepgram.com/v1/speak?model={model_name}"

        # Define the headers
        headers = {
            "Authorization": f"Token {self.api_key}",
            "Content-Type": "application/json"
        }

        # Define the payload
        payload = {
            "text": text
        }

        # Make the POST request
        response = requests.post(url, headers=headers, json=payload)

        return response.content

    def play_audio_from_bytes(self, text, format="mp3"):
        """Plays audio from a byte string."""

        audio_bytes = self.get_audio_response(text)
        # Convert bytes to AudioSegment (assuming format is known)
        audio = AudioSegment.from_file(BytesIO(audio_bytes), format=format)

        # Play the audio
        print("PLAYING THE AUDIO")
        play(audio)
