import azure.cognitiveservices.speech as speechsdk
import ffmpeg
import time
from pymongo.collection import Collection

class AzureSpeechRecognizer:
    def __init__(self, src:str, api_key:str, collection:Collection, region='japanwest', lang='ja-JP'):
        # FFmpeg
        self.__process = (
            ffmpeg
            .input(src, format='s16le', acodec='pcm_s16le', ac=1, ar='16k')
            .output('-', format='s16le', acodec='pcm_s16le', ac=1, ar='16k')
            .run_async(pipe_stdout=True)
        )
        # Config a speech recognizer
        speech_config = speechsdk.SpeechConfig(subscription=api_key, region=region)
        speech_config.speech_recognition_language=lang
        self.__stream = speechsdk.audio.PushAudioInputStream()
        audio_config = speechsdk.audio.AudioConfig(stream=self.__stream)
        self.__speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
        # Connect callbacks to the events fired by the speech recognizer
        self.__speech_recognizer.recognizing.connect(self.__recognizing_cb)
        self.__speech_recognizer.recognized.connect(self.__recognized_cb)
        self.__speech_recognizer.session_started.connect(self.__session_started_cb)
        self.__speech_recognizer.session_stopped.connect(self.__session_stopped_cb)
        self.__speech_recognizer.canceled.connect(self.__canceled_cb)
        # AmqClient
        self.__collection = collection
        self.__running = False

    def start(self):
        """ 音声認識を開始する """
        self.__running = True
        self.__speech_recognizer.start_continuous_recognition()
        try:
            while self.__running:
                in_bytes = self.__process.stdout.read(1024)
                if not in_bytes:
                    break
                self.__stream.write(in_bytes)
        except KeyboardInterrupt:
            pass

    def __recognizing_cb(self, evt):
        """ 認識中の結果を送信 """
        data = dict(timestamp=time.time(), state='recognizing', result=evt.result.text)
        self.__collection.insert_one(data)

    def __recognized_cb(self, evt):
        """ 認識完了の結果を送信 """
        data = dict(timestamp=time.time(), state='recognized', result=evt.result.text)
        self.__collection.insert_one(data)

    def __session_started_cb(self, evt):
        pass

    def __session_stopped_cb(self, evt):
        self.__running = False

    def __canceled_cb(self, evt):
        self.__running = False

    def __enter__(self):
        return self

    def __exit__(self, ex_type, ex_value, trace):
        self.__running = False
        self.__speech_recognizer.stop_continuous_recognition()

