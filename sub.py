class subtitle:
    
    def __init__(self):
        print("initializing subtitle item");
        self._texts = []
        self._timeStartAndEnd = None
    
    @property
    def timeStartAndEnd(self):
        return self._timeStartAndEnd
    
    @timeStartAndEnd.setter
    def timeStartAndEnd(self, value):
        self._timeStartAndEnd = value
        
    def add_text(self, text):
        self.texts.append(text)
        
    @property
    def texts(self):
        return self._texts
    
    def add_text(self, text):
        self._texts.append(text)