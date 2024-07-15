from deepgram import DeepgramClient, DeepgramClientOptions, LiveTranscriptionEvents, LiveOptions
from dotenv import load_dotenv
load_dotenv()
from src.constant import *
API_KEY = DEEPGRAM_API_KEY


def main():
    try:
        config = DeepgramClientOptions(
            options={"keepalive": "true"}  # Comment this out to see the effect of not using keepalive
        )

        deepgram = DeepgramClient(API_KEY, config)

        dg_connection = deepgram.listen.live.v("1")

        def on_message(self, result, **kwargs):
            sentence = result.channel.alternatives[0].transcript
            if len(sentence) == 0:
                return
            print(f"speaker: {sentence}")

        def on_metadata(self, result, **kwargs):
            print(f"\n\n{result}\n\n")

        def on_error(self, error, **kwargs):
            print(f"\n\n{error}\n\n")

        dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)
        dg_connection.on(LiveTranscriptionEvents.Metadata, on_metadata)
        dg_connection.on(LiveTranscriptionEvents.Error, on_error)

        options = LiveOptions(
            model="nova-2",
            language="en-US",
            smart_format=True,
        )

        dg_connection.start(options)

    except Exception as e:
        print(f"Could not open socket: {e}")


if __name__ == "__main__":
    main()
