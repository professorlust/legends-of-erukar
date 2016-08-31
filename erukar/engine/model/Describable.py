from .Interactible import Interactible

class Describable(Interactible):
    Visuals = {
        0.0: 'Completely Black',
        0.33: 'Barely Visible',
        0.66: 'Highly Visible',
        1.0: 'Completely Visible'
    }

    Senses = {
        0.0: 'Completely Silent',
        0.33: 'Slightly Audible',
        0.66: 'Highly Audible',
        1.0: 'Perfectly Audible'
    }

    '''
    The Ranges here indicate a nminimal success and a full success. This is the 
    difference between a 0.00 and a 1.0 score. The range is used to find the 
    percentage success value, e.g. a range of 4 min and 8 ideal would yield 0.5
    for an acuity roll of 6 and 1.0 for a roll of 8 or higher.
    '''
    MinimumAcuity = 0
    IdealAcuity = 1
    MinimumSense = 0
    IdealSense = 1

    def visual_description(self, lifeform, acuity):
        return ''

    def sensed_description(self, lifeform, sense):
        return ''

    def describe(self):
        pass

    def necessary_sense(self):
        return 0

    def necessary_acuity(self):
        return 0

