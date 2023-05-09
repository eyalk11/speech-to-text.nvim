# Thanks https://vi.stackexchange.com/users/23502/vivian-de-smedt
# for the help with the plugin.
import keyboard
import asyncio
import yaml
import neovim
import speech_recognition as sr
import concurrent.futures

import os
DEFAULT_CONFIG_PATH =os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../voice_config.yaml")
import nest_asyncio
nest_asyncio.apply() #bad practice, but the situation is problematic

@neovim.plugin
class SpeechToTextPlugin(object):
    def __init__(self, nvim):
        self.nvim = nvim
        self.r = sr.Recognizer()
        self.engine=None

        try: 
            with open(DEFAULT_CONFIG_PATH) as f:
                config = yaml.load(f, Loader=yaml.FullLoader)
        except FileNotFoundError:
            self.nvim.err_write("Error: config file not found\n")
            return

        self.engines = {
            name: getattr(self.r, method)
            for name, method in config["engines"].items()
        }
        self.default_args = config["default_args"]
        self.default_engine = config["default_engine"]
        self.engine = self.engines[self.default_engine]
        self.args = self.default_args.get(self.default_engine, {})

    @neovim.command("ConfigureVoice", range="", nargs="*", sync=True)
    def configure_params(self, args, range):
        if len(args)==0:
            self.nvim.out_write("Current engine is %s\n" % (self.engine,))
            self.nvim.out_write( "params %s\n" %  (self.args,))
            return
        eng = args[0]
        if not eng in self.engines:
            self.nvim.err_write("Error: engine not found\n")
            return
        if len(args) >= 1:
            if len(args) >= 2:
                if type(args[1]) is not dict:
                    self.nvim.err_write("Error: args must be a dict\n")
                    return

                self.args = args[1]
            else:
                self.args = self.default_args.get(eng, {})

            self.engine = self.engines[eng]
            self.nvim.out_write("Engine set to %s\n" % eng)
    @staticmethod
    async def async_task_and_spin(wait_for_inp, some_task, args):
        loop = asyncio.get_event_loop()
        # Run the synchronous function in an executor
        pool = concurrent.futures.ThreadPoolExecutor()

        try:
            task = loop.run_in_executor(pool, some_task, *args)
            event_task = loop.run_in_executor(pool, wait_for_inp)
            # Wait for the task or the event to complete
            done, pending = await asyncio.wait(
                {task, event_task}, return_when=asyncio.FIRST_COMPLETED
            )
            print('returned')
            # Cancel any pending tasks
            for t in pending:
                t.cancel()
            if task in done:
                result = await task
                return result
        finally:
            pool.shutdown(wait=False)

    @neovim.command("Voice", range="", nargs="*", sync=True)
    def voice(self, args, rgn):
        print('a')
        if len(args) > 0:
            self.configure_params(args, rgn)
        start_line, end_line = rgn

        try:
            text=self.get_voice()
        except Exception as e: 
            self.nvim.out_write("Error: %s\n" % e)


        if text is None or (len(text)==0):
            return

        lines = text.split("\r")

        if len(lines) < end_line + 1 - start_line:
            # Remove lines in excess:
            self.nvim.call("deletebufline", "%", start_line + len(lines), end_line)

        for i in range(len(lines) - (end_line + 1 - start_line)):
            # Insert missing blank lines:
            self.nvim.call("appendbufline", "%", end_line, "")

        for index, line in enumerate(lines):
            # Replace lines with the text:
            self.nvim.call("setbufline", "%", start_line + index, line)


    @neovim.function("GetVoice", sync=True)
    def get_voice(self,args=[]):
        if self.engine is None:
            self.nvim.err_write("Error: engine not set\n")
            return ""

        try:
            # use the microphone as source for input.
            with sr.Microphone() as source2:

                # wait for a second to let the recognizer
                # adjust the energy threshold based on
                # the surrounding noise level
                self.r.adjust_for_ambient_noise(source2, duration=0.4)


                # Using google to recognize audio

                def use_engine():
                    #listens for the user's input
                    audio2 = self.r.listen(source2)
                    return self.engine(audio2, **self.args)

                def wait_for_ended():
                   keyboard.wait('esc')

                loop = asyncio.get_event_loop()
                text= loop.run_until_complete(self.async_task_and_spin(wait_for_ended,use_engine,()))

                if text is None or (len(text)==0):
                    return ""
                return text

        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

        except sr.UnknownValueError:
            print("unknown error occurred")
        return ""
