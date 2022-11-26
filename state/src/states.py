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
            d = self.db['human_recognition'].find_one(sort=[( 'timestamp', pymongo.DESCENDING)])
            if len(d['results']) > 0:
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

        if self.ask_to_people():
            return Ask(self.db, self.target_id)
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

    def ask_to_people(self) -> bool:
        d = self.db['state'].find_one(sort=[( 'timestamp', pymongo.DESCENDING)])
        state_changetime = d['timestamp']

        dt = 5
        t = time.time()
        m = self.db['human_recognition'].count_documents({
            'timestamp': { '$gt': t - dt, '$lt': t }
        })
        n = self.db['human_recognition'].count_documents({
            'timestamp': { '$gt': t - dt, '$lt': t },
            'results' : { '$ne': [] }
        })
        if t - dt >= state_changetime:
            return n >= m
        return False

class Ask(State):
    def __init__(self, db, target_id:str):
        super().__init__(db)
        self.target_id = target_id

    def to_document(self) -> dict:
        return dict(name=self.__class__.__name__, target_id=self.target_id)

    def transition(self) -> State:
        if self.talk_to_people():
            return Talk(self.db, self.target_id)
        if self.bye_to_you():
            return Bye(self.db, self.target_id)
        if self.person_disappeared():
            return Idle(self.db)
        return self
    

    def person_disappeared(self) -> bool:
        dt = 10
        t = time.time()
        n = self.db['human_recognition'].count_documents({
            'timestamp':{'$gt': t - dt, '$lt': t},
            'results.0.id': self.target_id
        })
        return n == 0

    
    def talk_to_people(self) -> bool:
        d = self.db['state'].find_one(sort=[( 'timestamp', pymongo.DESCENDING)])
        state_changetime = d['timestamp']

        dt = 5
        m = 1
        t = time.time()
        n = self.db['speech_recognition'].count_documents({
            'timestamp': { '$gt': t - dt, '$lt': t },
            'state': {'$eq': "recognized"},
            'result' : { '$in': ["はい。"]}
        })
        
        if t - dt >= state_changetime:
            return n >= m
        
        return  False

    def bye_to_you(self) -> bool:
        d = self.db['state'].find_one(sort=[( 'timestamp', pymongo.DESCENDING)])
        state_changetime = d['timestamp']
        dt = 5
        m = 1
        t = time.time()
        n = self.db['speech_recognition'].count_documents({
            'timestamp': { '$gt': t - dt, '$lt': t },
            'state': {'$eq': "recognized"},
            'result' : { '$in': ["いいえ。"]}
        })
        if t - dt >= state_changetime:
            return n >= m


class Talk(State):
    def __init__(self, db, target_id:str):
        super().__init__(db)
        self.target_id = target_id

    def to_document(self) -> dict:
        return dict(name=self.__class__.__name__, target_id=self.target_id)

    def transition(self) -> State:
        if self.person_disappeared():
            return Idle(self.db)
        if self.goodbye():
            return Bye(self.db, self.target_id)

        return self

    def person_disappeared(self) -> bool:
        dt = 10
        t = time.time()
        n = self.db['human_recognition'].count_documents({
            'timestamp':{'$gt': t - dt, '$lt': t},
            'results.0.id': self.target_id
        })
        return n == 0

    def goodbye(self) -> bool:
        d = self.db['state'].find_one(sort=[( 'timestamp', pymongo.DESCENDING)])
        state_changetime = d['timestamp']
        dt = 5
        t = time.time()
        n = self.db['human_recognition'].count_documents({
            'timestamp':{'$gt': t - dt, '$lt': t},
            'results.0.id': self.target_id
        })
        if t - dt >= state_changetime:
            return n == 0

class Bye(State):
    def __init__(self, db, target_id:str):
        super().__init__(db)
        self.target_id = target_id
    
    def to_document(self) -> dict:
        return dict(name=self.__class__.__name__, target_id=self.target_id)

    def transition(self):
        if self.person_disappeared():
            return Idle(self.db)
        return self

    def person_disappeared(self):
        dt = 10
        t = time.time()
        n = self.db['human_recognition'].count_documents({
            'timestamp':{'$gt': t - dt, '$lt': t},
            'results.0.id': self.target_id
        })
        return n == 0
        





