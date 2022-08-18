import argparse
from pymongo import MongoClient
from sr import AzureSpeechRecognizer


if __name__ == '__main__':
    parse = argparse.ArgumentParser()
    parse.add_argument('--api_key', required=True, type=str)
    parse.add_argument('--db_host', default='mongo', type=str)
    parse.add_argument('--db_port', default=27017, type=int)
    args = parse.parse_args()
    src = 'udp://127.0.0.1:5001'
    client = MongoClient(args.db_host, args.db_port)
    db = client.robot_talking_to_people
    collection = db.speech_recognition
    with AzureSpeechRecognizer(src, args.api_key, collection) as sr:
        sr.start()
