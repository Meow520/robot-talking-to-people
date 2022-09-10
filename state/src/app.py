import argparse
import time
import states
from pymongo import MongoClient



def main(args):

    # MongoDB
    client = MongoClient(args.db_host, args.db_port)
    db = client[args.db_name]

    # データベース挿入用関数
    def insert(state:states.State):
        timestamp = time.time()
        document = state.to_document()
        document.update(timestamp=timestamp)
        db['state'].insert_one(document)

    try:
        state = states.Init(db)
        insert(state)
        while True:
            new_state = state.transition()
            if new_state.equals(state):
                time.sleep(args.interval)
                continue
            state = new_state
            insert(state)

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
