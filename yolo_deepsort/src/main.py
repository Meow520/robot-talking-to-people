import argparse
from pymongo import MongoClient
from vr import HumanRecognizer


if __name__ == '__main__':
    parse = argparse.ArgumentParser()
    parse.add_argument('--gpu', action='store_true')
    parse.add_argument('--db_host', default='mongo', type=str)
    parse.add_argument('--db_port', default=27017, type=int)
    args = parse.parse_args()
    device='cuda:0' if args.gpu else 'cpu'
    src = 'udp://127.0.0.1:5000'
    client = MongoClient(args.db_host, args.db_port)
    db = client.robot_talking_to_people
    collection = db.human_recognition
    with HumanRecognizer(src, device, collection) as hr:
        hr.start()
