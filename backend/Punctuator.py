from deepmultilingualpunctuation import PunctuationModel

class Punctuator:
    def __init__(self, model):
        self.model = model
    
    def punctuate_transcript(self, transcript):
        result = model.restore_punctuation(text)
        return result
        