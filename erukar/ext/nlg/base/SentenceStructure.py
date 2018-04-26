class SentenceStructure():
    def create(payload):
        return '{subject} {verb} {object}.'.format(**payload).capitalize()
