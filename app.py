import asyncio
from ctypes import *
from src.voice_agent import Agent



# To suppress the alsa error in ubuntu systems
def py_error_handler(filename, line, function, err, fmt):
    None


ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)
asound = cdll.LoadLibrary('libasound.so')
asound.snd_lib_error_set_handler(c_error_handler)

# calling the agent
agent = Agent()
asyncio.run(agent.main())
