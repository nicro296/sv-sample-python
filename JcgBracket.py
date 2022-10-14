import requests
import pandas as pd
import numpy as np
import json
import copy
from bs4 import BeautifulSoup as bs

import Archetypes as Arches
from Deck import Deck


class JcgBracket:
    '''
    bracket : 
        an example is sample/jcgBracketSample.json
    {
        apiUrl : str
        bracket : dict
        groups : list[{
            id : int
                code : str
                group number
            name : str
            rounds : list[]
            sioName : str
        }]
        myUsername : str
        myTeamId : int
        myGroupCode : ""
        isa : bool
        settings : dict
    }
      
    matches : list[
        each match data json list 
        https://sv.j-cg.com/api/competition/group/XXXXXX (X=number)
        an example is sample/jcgBracketMatchSample.json
    {
        succes : bool
        rounds : list[{
            startAt : str
            name : str
            matches : list[{
                winner : int
                code : int
                id : int
                bo : int
                blockId : int
                groupCode : str
                teams : list[{
                    id : int
                    nameAbbr : str
                    name : str
                    nameKana : None
                    nicename : str
                    logo : str
                    win : bool
                    lose : bool
                    lost : bool
                    draw : bool
                    default : bool
                    wins : int
                    users : list[]
                }]
            }]
        }]
    }]
        
    parameters
    ----------
    url_id : str
        12 characters in URL
        https://sv.j-cg.com/competition/ *url_id* /home
    '''

    def __init__(self, url_id:str):
        url_groups  = 'https://sv.j-cg.com/competition/'+url_id+'/bracket#/1'
        source = requests.get(url_groups).text
        soup = bs(source, 'lxml')
        allscr = soup.find_all('script')
        tjson = allscr[7].text
        cleanedjson = tjson[tjson.find('{"apiUrl":"'):]
        self.bracket = json.loads(cleanedjson)
    def get_group_ids(self):
        group_ids = []
        for group in self.bracket['groups']:
            group_ids.append(group['id'])
        return group_ids
    def set_matches(self):
        self.matches = []
        group_ids = self.get_group_ids()
        for group_id in group_ids:
            bracketjson = 'https://sv.j-cg.com/api/competition/group/' + str(group_id)
            response = requests.get(bracketjson)
            self.matches.append(response.json())

class JcgEntry:
    '''
    players : list[{
        JcgEntryPlayer
    }]

    parameters
    ----------
    url_id : str
        12 characters in URL
        https://sv.j-cg.com/competition/ *url_id* /home
    '''
    def __init__(self, url_id:str):
        self.players = []
        url_entries = 'https://sv.j-cg.com/competition/'+url_id+'/entries'
        html = requests.get(url_entries)
        soup = bs(html.content, "html.parser")
        all_script = soup.find_all('script')
        dljson = all_script[7].string
        cleanedjson = dljson[dljson.find('list'):dljson.find('listFiltered')]
        finaljson = cleanedjson.replace('list:','').strip()[:-1]
        data = json.loads(finaljson)
        for player in data:
            self.players.append(JcgEntryPlayer(player))
    def get_player(self,player_id):
        for jcgEntryPlayer in self.players:
            if player_id == player.player_id:
                return jcgEntryPlayer
        raise Exception('dont find player_id')
    def write_json(self,file_uri):
        output = {'players':[]}
        for jcgEntryPlayer in self.players:
            output['players'].append(jcgEntryPlayer.get_dict())
        with open(file_uri ,'w', encoding='utf-8') as f:
            output_json = json.dumps(output)
            print(output_json, file=f)
    def set_archetype(self):
        for jcgEntryPlayer in self.players:
            jcgEntryPlayer.set_archetype()

class JcgEntryPlayer:
    '''PlayerData
    player_name : str
    player_id : int
        7 digit number
    username : str
        6 digit number, but str
    nicename : str
        24 characters [0-9,a-z,A-z]
    result : int
        0 : not elected
        1 : elected
    decks : list[Deck]

    parameters
    -----------
    player : dict{
        id : int
        name :str
        username : str
        nicename : str
        result : int
        channel : None
        avatar : str
        comment : str
        show : bool
        sv_decks : list[{
            clan : int
            hash : str
        }]
    }
    '''
    def __init__(self,player):
        self.player_name = player['name']
        self.player_id = player['id']
        self.username = int(player['username'])
        self.nicename = player['nicename']
        self.result = player['result']
        self.decks = []
        for sv_deck in player['sv_decks']:
            deck = Deck(clan=sv_deck['clan'],hash=sv_deck['hash'])
            self.decks.append(deck)
    def set_archetype(self):
        for deck in self.decks:
            deck.set_archetype()
    def get_dict(self):
        output = copy.deepcopy(self)
        output.decks = []
        for deck in self.decks:
            output.decks.append(vars(deck))
        return vars(output)


tournament_id = 'vsySSXEFrxP1'
jcgBracket = JcgBracket(tournament_id)

with open('sample/jcgBracketSample.json', 'w', encoding='utf-8') as f:
    jb = json.dumps(jcgBracket.bracket)
    print(jb, file=f)

jcgBracket.set_matches()
with open('sample/jcgBracketMatchSample.json' ,'w', encoding='utf-8') as f:
    jb = json.dumps(jcgBracket.matches)
    print(jb, file=f)

jcgEntry = JcgEntry(tournament_id)
jcgEntry.set_archetype()
jcgEntry.write_json('sample/playersInJcgEntrySample.json')