from ctypes import *


def py_error_handler(filename, line, function, err, fmt):
    None


ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

asound = cdll.LoadLibrary('libasound.so')
asound.snd_lib_error_set_handler(c_error_handler)


from src.components.speech_to_text import SpeechToText
import asyncio

if __name__=="__main__":
    stt = SpeechToText()

    asyncio.run(stt.get_transcript())