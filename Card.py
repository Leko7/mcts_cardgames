# Card.py
class BeloteCard(object):
    def __init__(self, id : int):
        self.id = id

        if 0 <= id <= 5:
            self.color = 'carreau'
        elif 6 <= id <= 11:
            self.color = 'coeur'
        elif 12 <= id <= 17:
            self.color = 'trèfle'
        elif 18 <= id <= 23:
            self.color = 'pique'

        base_indices = [0, 6, 12, 18]
        if id in base_indices :
            self.label = '9'
        elif id in [x + 1 for x in base_indices]:
            self.label = '10'
        elif id in [x + 2 for x in base_indices]:
            self.label = 'V'
        elif id in [x + 3 for x in base_indices]:
            self.label = 'D'
        elif id in [x + 4 for x in base_indices]:
            self.label = 'R'
        elif id in [x + 5 for x in base_indices]:
            self.label = 'A'

        if self.color == 'pique':
            if self.label == 'V':
                self.value = 20
            elif self.label == '9':
                self.value = 14
            elif self.label == 'A':
                self.value = 11
            elif self.label == '10':
                self.value = 10
            elif self.label == 'R':
                self.value = 4
            elif self.label == 'D':
                self.value = 3
        else:
            if self.label == 'A':
                self.value = 11
            elif self.label == '10':
                self.value = 10
            elif self.label == 'R':
                self.value = 4
            elif self.label == 'D':
                self.value = 3
            elif self.label == 'V':
                self.value = 2
            elif self.label == '9':
                self.value = 0

    def display(self):
        return (self.label,self.color,self.id)