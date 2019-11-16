class ChatState:
    def __init__(self, id_, last_anecs=[], won=0, lost=0):
        self.id_ = id_
        self.last_anecs = last_anecs
        self.won = won
        self.lost = lost
