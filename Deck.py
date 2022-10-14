import Archetypes as Arches
import Archetype

class Deck:
    '''
    clan : int
        shadowverse leader class number
        1 : ForestCraft
        2 : SwordCraft
        ...
        8 : PortalCraft
        (0 : Neutral)
    codes : list[str]
        list of 64-digit card codes in deck
    archetype_name : str

    parameters
    ----------
    deck-url : str
    clan : int
    hash : str

    you can use this class with deck-url or clan & hash
    For example
        Deck(clan=1,hash="3.1.5zvAY.5zvAY.5zvAY./~ ~/.5zxco.5zxco.5zxco")
        Deck(deck_url="https://shadowverse-portal.com/deck/3.1.5zvAY.5zvAY.5zvAY./~ ~/.5zxco.5zxco.5zxco?lang=ja")
        Deck(deck_url="https://shadowverse-portal.com/deckbuilder/create/1?hash=3.1.5zvAY.5zvAY.5zvAY./~ ~/.5zxco.5zxco.5zxco?lang=ja")
    '''
    
    def __init__(self, deck_url=None ,clan=None, hash=None):
        if(deck_url!= None):
            self.set_from_deckurl(deck_url)
            return
        if(clan!=None and hash!= None):
            self.set_from_clan_hash(clan,hash)
            return
        raise Exception('Unvalid deck data.')
    def set_from_deckurl(self,deck_url):
        deck_url_ini = 'https://shadowverse-portal.com/deck/'
        deckbuild_url_ini = 'https://shadowverse-portal.com/deckbuilder/create/'
        if(deck_url_ini in deck_url):
            self.clan = int(deck_url[38:39])
            self.codes = deck_url[40:40+239].split('.')
            return
        if(deckbuild_url_ini in deck_url):
            self.clan = int(deck_url[59:60])
            self.codes = deck_url[61:61+239].split('.')
            return
        raise Exception('Unvalid deck data.') 
    def set_from_clan_hash(self,clan,hash):
        self.clan = clan
        self.codes = hash[4:].split('.')
    def set_archetype(self):
        '''
        need to 'import Archetypes as Arches'
        '''
        for archetype in Arches.archetypes:
            if archetype.clan != self.clan:
                continue
            if archetype.is_valid_deck(self):
                self.archetype_name = archetype.archetype_name
                return
        # If there is no suitable archetype, name it 'Unclassified'
        self.archetype_name = 'Unclassified'


