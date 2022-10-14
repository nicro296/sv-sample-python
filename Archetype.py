class Archetype:
    '''
    clan : int
        shadowverse leader class number
    archetype_name : str
    card_codes : list[str]
        list of 64-digit card codes for archetype classiification
    '''
    def __init__(self,clan,name,card_codes):
        self.clan = clan
        self.archetype_name = name
        self.card_codes = card_codes
    def is_valid_deck(self,deck):
        '''
        デッキを渡すとこのアーキタイプにふさわしいデッキならTrue,そうでないならFalseを返す
        '''
        for card_code in self.card_codes:
            if(card_code not in deck.codes):
                return False
        return True

