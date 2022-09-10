import argparse
import queue
import threading
import time
import pymongo
import behaviors


def main(args):

    # MongoDB
    client = pymongo.MongoClient(args.db_host, args.db_port)
    db = client[args.db_name]

    # Variables
    q = queue.Queue()
 
    # Function executed by another thread
    def poll():
        """ DBをポーリングして状態変化を通知 """
        prev_document = None
        while True:
            document = db['state'].find_one(sort=[('_id', pymongo.DESCENDING)])
            if document == prev_document:
                time.sleep(args.interval)
                continue
            q.put(document)
            prev_document = document

    threading.Thread(target=poll, daemon=True).start()

    # データベース挿入用関数
    def insert(behavior:behaviors.Behavior, status:str):
        timestamp = time.time()
        document = behavior.to_document()
        document.update(timestamp=timestamp, status=status)
        db['behavior'].insert_one(document)

    try:
        behavior = behaviors.Init(db, {})
        insert(behavior, status='start')
        while True:
            document = q.get()
            behavior.stop()
            insert(behavior, status='stop')
            behavior = eval(f"behaviors.{document['name']}")(db, document)
            behavior.start()
            insert(behavior, status='start')
    except KeyboardInterrupt:
        pass



if __name__ == '__main__':
    parse = argparse.ArgumentParser()
    parse.add_argument('--interval', default=0.5, type=float)
    parse.add_argument('--db_host', default='mongo')
    parse.add_argument('--db_port', default=27017, type=int)
    parse.add_argument('--db_name', default='robot_talking_to_people', type=str)
    args = parse.parse_args()
    main(args)
