import openpyxl
import datetime
from openpyxl.styles.alignment import Alignment
from openpyxl.formatting.rule import ColorScaleRule, FormulaRule


class Matchup:
    def __init__(self,archetype_main:str,archetype_opposite:str):
        self.archetype_main = archetype_main
        self.archetype_opposite = archetype_opposite
        self.win_main = 0
        self.win_opposite = 0
        self.count = 0
        if self.archetype_main == self.archetype_opposite:
            self.treshold = 2
            return
        self.treshold = 1
    def add_wins(self,archetype1,win1,archetype2,win2):
        self.count += self.treshold *1
        self.add_win(archetype1,win1)
        self.add_win(archetype2,win2)
    def add_win(self,archetype,win):
        if self.archetype_main == archetype:
            self.win_main += win
            return
        if self.archetype_opposite == archetype:
            self.win_opposite += win
            return
        raise Exception('unvalid archetype.')
    def exist(self,archetype):
        if archetype == self.archetype_main:
            return True
        if archetype == self.archetype_opposite:
            return True
        return False
    def get_opponent(self,archetype_main):
        if archetype_main == self.archetype_main:
            return self.archetype_opposite
        if archetype_main == self.archetype_opposite:
            return self.archetype_main
        print(archetype_main)
        raise Exception('unvalid archetype')
    def get_win_percentage(self,archetype):
        even = 50
        if archetype == self.archetype_main:
            if self.archetype_main == self.archetype_opposite:
                return even
            return round((self.win_main/(self.win_main+self.win_opposite))*100, 2)
        if archetype == archetype_opposite:
            return round((self.win_opposite/(self.win_main+self.win_opposite))*100, 2)
        raise Exception('unvali archetype')
    def get_data_count(self):
        return self.count
