import time
import pymongo


class State:
    """ 状態を表す抽象クラス """
    def __init__(self, db):
        self.db = db
        print(self.__class__.__name__)

    def equals(self, state) -> bool:
        return id(self) == id(state)

    def to_document(self) -> dict:
        """ MongoDBにinsertするデータ形式に変換 """
        return dict(name=self.__class__.__name__)

    def transition(self):
        pass


class Init(State):
    """ 初期状態 """
    def transition(self) -> State:
        return Idle(self.db)


class Idle(State):
    """ アイドル状態 """
    def transition(self) -> State:
        if self.person_appeared():
            d = self.db['human_recognition'].find_one(sort=[( '_id', pymongo.DESCENDING)])
            target_id = d['results'][0]['id']
            return Greet(self.db, target_id)
        return self

    def person_appeared(self) -> bool:
        """ 現時点から過去dt秒間に人がm回以上検出されたらTrue """
        dt = 10
        m = 1
        t = time.time()
        n = self.db['human_recognition'].count_documents({
            'timestamp': { '$gt': t - dt, '$lt': t },
            'results' : { '$ne': [] }
        })
        return n >= m


class Greet(State):
    """ あいさつ状態 """
    def __init__(self, db, target_id:str):
        super().__init__(db)
        self.target_id = target_id

    def to_document(self) -> dict:
        """ MongoDBにinsertするデータ形式に変換 """
        return dict(name=self.__class__.__name__, target_id=self.target_id)

    def transition(self) -> State:
        if self.person_disappeared():
            return Idle(self.db)
        return self

    def person_disappeared(self) -> bool:
        """ 現時点から過去dt秒間に標的の人が一度も検出されていなければTrue """
        dt = 10
        t = time.time()
        n = self.db['human_recognition'].count_documents({
            'timestamp': { '$gt': t - dt, '$lt': t },
            'results.0.id': self.target_id
        })
        return n == 0

