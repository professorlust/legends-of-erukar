class Observation:
    def __init__(self, acuity=0, sense=0, result=""):
        self.acuity = acuity
        self.sense = sense
        self.result = result

    def met(self, acuity, sense):
        return acuity >= self.acuity and sense >= self.sense

    def result_if_met(self, acuity, sense):
        return self.result if self.met(acuity, sense) else ""

    def score(self):
        return self.acuity + self.sense
