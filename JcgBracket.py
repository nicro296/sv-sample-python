import requests
import pandas as pd
import numpy as np
import json
import copy
import datetime
import openpyxl
from openpyxl.styles.alignment import Alignment
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
            if int(player_id) == jcgEntryPlayer.username:
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
    username : int
        6 digit number
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

'''サンプルjsonファイル作成用
# tournament_id = 'vsySSXEFrxP1'
# jcgBracket = JcgBracket(tournament_id)

# with open('sample/jcgBracketSample.json', 'w', encoding='utf-8') as f:
#     jb = json.dumps(jcgBracket.bracket)
#     print(jb, file=f)

# jcgBracket.set_matches()
# with open('sample/jcgBracketMatchSample.json' ,'w', encoding='utf-8') as f:
#     jb = json.dumps(jcgBracket.matches)
#     print(jb, file=f)

# jcgEntry = JcgEntry(tournament_id)
# jcgEntry.set_archetype()
# jcgEntry.write_json('sample/playersInJcgEntrySample.json')
'''


#分析パート 用意できていないので無理矢理くっつけておく

dt_now = datetime.datetime.now()
Arch_Name = [
    [
        'テンポエルフ',
        'コントロールエルフ'
    ],
    [
        'コントロールロイヤル',
        'その他ロイヤル'
    ],
    [
        '秘術ウィッチ',
        'スペルウィッチ'
    ],
    [
        'コントロールドラゴン',
        'その他ドラゴン'
    ],
    [
        'ラスワ進化ネクロ',
        'ハイドラネクロ'
    ],
    [
        'ハンドレスヴァンパイア',
        '進化ヴァンパイア'
    ],
    [
        '結晶ビショップ',
        '回復ビショップ'
    ],
    [
        'AFネメシス',
        'その他（人形）'
    ]
    ]
def get_archetype_index(deck):
    for i in range(len(Arch_Name[(deck.clan-1)])):
        if Arch_Name[(deck.clan-1)][i] == deck.archetype_name:
            return i
    raise Exception('unvalid archetype name.')

DATA = [
    [[],[]], # CLASS_A,CLASS_B
    [[],[]], # WIN, LOSE
    [[],[]]  # arche_A,arche_B
    ]
Head = ['デッキ1','デッキ２','勝率','データ数']

class main():
    def make_DATA(self):
        for match in self.jcgBracket.matches:
            for _round in match['rounds']: 
                for round_match in _round['matches']:
                    for i in range(2):
                        win = round_match['teams'][i]['wins']
                        player_id = round_match['teams'][i]['users'][0]['username']
                        player = self.jcgEntry.get_player(player_id)
                        DATA[0][i].append(player.decks[0].clan)
                        DATA[0][i].append(player.decks[0].clan)
                        DATA[0][i].append(player.decks[1].clan)
                        DATA[0][i].append(player.decks[1].clan)
                        DATA[1][i].append(win)
                        DATA[1][i].append(win)
                        DATA[1][i].append(win)
                        DATA[1][i].append(win)
                        DATA[2][i].append(get_archetype_index(player.decks[0]))
                        DATA[2][i].append(get_archetype_index(player.decks[0]))
                        DATA[2][i].append(get_archetype_index(player.decks[1]))
                        DATA[2][i].append(get_archetype_index(player.decks[1]))
    def anal(self):
        ANL_DATA = ([],[],[],[])
        sum_win = 0 
        sum_lose = 0
        n = 0
        wb = openpyxl.Workbook()
        for i in range(1,9):
            for k in range(len(Arch_Name[i-1])):
                for j in range(1,9):
                    for K in range(len(Arch_Name[j-1])):
                        for N in range(len(DATA[0][0])):
                            if DATA[0][0][N] == i and DATA[0][1][N] == j and DATA[2][0][N] == k and DATA[2][1][N] == K:
                                n = n + 1
                                sum_win = sum_win + int(DATA[1][0][N])
                                sum_lose = sum_lose + int(DATA[1][1][N])
                            if DATA[0][0][N] == j and DATA[0][1][N] == i and DATA[2][0][N] == K and DATA[2][1][N] == k:
                                n = n + 1
                                sum_win = sum_win + int(DATA[1][1][N])
                                sum_lose = sum_lose + int(DATA[1][0][N])
                        ANL_DATA[0].append(Arch_Name[i-1][k])
                        ANL_DATA[1].append(Arch_Name[j-1][K])
                        ANL_DATA[3].append(n)
                        if sum_win == 0:
                            ANL_DATA[2].append(0)
                        else:
                            ANL_DATA[2].append(100*sum_win/(sum_win+sum_lose))
                sheet = wb.create_sheet(ANL_DATA[0][0])
                SR = 2
                SC = 1
                # SR =
                for I in range(4):
                    sheet.cell(
                        row = 1,
                        column = I + 1 ,
                        value = Head[I]
                        # horizontal = "center"
                    ) 
                for I in range(len(ANL_DATA)):
                    for J in range(len(ANL_DATA[0])):
                        sheet.cell(
                            row = SR + J,
                            column = SC + I,
                            value = ANL_DATA[I][J] #,
                            # horizontal = "center"
                            )
                for row in sheet:
                    for cell in row:
                        cell.alignment = Alignment(horizontal = 'center')
                sheet.column_dimensions['A'].width = 25
                sheet.column_dimensions['B'].width = 25
                sum_win = 0 
                sum_lose = 0
                n = 0
                ANL_DATA = ([],[],[],[])
        wb = wb.save(str(dt_now.year)+str(dt_now.month).zfill(2)+str(dt_now.day).zfill(2)+'勝率.xlsx')

    def __main__(self):
        tournament_id = 'vsySSXEFrxP1'
        self.jcgBracket = JcgBracket(tournament_id)
        self.jcgBracket.set_matches()
        self.jcgEntry = JcgEntry(tournament_id)
        self.jcgEntry.set_archetype()
        main.make_DATA()
        main.anal()

main = main()
if __name__ == '__main__':
    main.__main__()