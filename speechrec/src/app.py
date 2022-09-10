import argparse
import time
import azure.cognitiveservices.speech as speechsdk
import ffmpeg
from pymongo import MongoClient


def main(args):

    # MongoDB
    client = MongoClient(args.db_host, args.db_port)
    db = client[args.db_name]
    collection = db[args.db_collection_name]

    # Config a speech recognizer
    speech_config = speechsdk.SpeechConfig(subscription=args.api_key, region=args.region)
    speech_config.speech_recognition_language=args.lang
    stream = speechsdk.audio.PushAudioInputStream()
    audio_config = speechsdk.audio.AudioConfig(stream=stream)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    # Callbacks for speech recog
    def recognizing_cb(event):
        """ 認識中の結果をデータベースに挿入 """
        data = dict(timestamp=time.time(), state='recognizing', result=event.result.text)
        print(data)
        collection.insert_one(data)

    def recognized_cb(event):
        """ 認識完了の結果をデータベースに挿入 """
        data = dict(timestamp=time.time(), state='recognized', result=event.result.text)
        print(data)
        collection.insert_one(data)

    def session_started_cb(event):
        print('Speech recognition session started.')
        pass

    def session_stopped_cb(event):
        print('Speech recognition session stopped.')
        pass

    def canceled_cb(event):
        print('Speech recognition is canceled.')
        pass
    
    # Connect callbacks to the events fired by the speech recognizer
    speech_recognizer.recognizing.connect(recognizing_cb)
    speech_recognizer.recognized.connect(recognized_cb)
    speech_recognizer.session_started.connect(session_started_cb)
    speech_recognizer.session_stopped.connect(session_stopped_cb)
    speech_recognizer.canceled.connect(canceled_cb)

    # FFmpeg
    process = (
        ffmpeg
        .input(args.src, format='s16le', acodec='pcm_s16le', ac=1, ar='16k')
        .output('-', format='s16le', acodec='pcm_s16le', ac=1, ar='16k')
        .run_async(pipe_stdout=True)
    )

    # Start speech recognition
    speech_recognizer.start_continuous_recognition()
    try:
        while True:
            in_bytes = process.stdout.read(1024)
            if not in_bytes:
                break
            stream.write(in_bytes)
    except KeyboardInterrupt:
        pass
    speech_recognizer.stop_continuous_recognition()


if __name__ == '__main__':
    parse = argparse.ArgumentParser()
    parse.add_argument('--api_key', required=True, type=str)
    parse.add_argument('--region', default='japanwest', type=str)
    parse.add_argument('--lang', default='ja-JP', type=str)
    parse.add_argument('--src', default='udp://127.0.0.1:5001', type=str)
    parse.add_argument('--db_host', default='mongo', type=str)
    parse.add_argument('--db_port', default=27017, type=int)
    parse.add_argument('--db_name', default='robot_talking_to_people', type=str)
    parse.add_argument('--db_collection_name', default='speech_recognition', type=str)
    args = parse.parse_args()
    main(args)
