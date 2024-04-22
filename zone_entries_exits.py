## Fauzan Lodhi
## flodhi@uwaterloo.ca
## Undergraduate, University of Waterloo Faculty of Math
## 2024 HBDC
## This script consumes the provided BDC Womens Data csv file and 
## produces multiple csv files:
## 1) Appending new columns to the provided file that classify applicable plays by the quality of zone exit (1-5), both its start and end
## 2) Listing all players in the dataset based on their overall zone exit score 


import pandas as pd
from scipy import stats
from functools import reduce

## reading the csv as a Pandas dataframe
df1 = pd.read_csv("BDC_2024_Womens_Data.csv",encoding='UTF-8')
USCAN = df1


## convert game time to seconds into period i.e. 3 = 19:57
USCAN['Time'] = USCAN['Clock'].apply(lambda x: 1200 - (int(x.split(':')[0]) * 60 + int(x.split(':')[1])))

## tracking the x coordinate in case possession changes (and x coordinate flips)
USCAN['Breakout_End X Coordinate'] = USCAN['X Coordinate']


def current_event(df, index):

    ## current_event consumes a dataframe and index and returns a concatenated list of details of the indexth play in df
    ## current_event: df, int -> list

    return df.loc[index, ['Period', 'Time', 'Team', 'Player', 'Zone', 'Event', 'Detail 1', 'Player 2']]


## details of successful zone exit play
successful_zone_exits = []

## play number of successful exit i.e 3 = third play in df
successful_exit_no = [] 


## details of a successful zone exit play where possession was lost on the exit
successful_zone_exit_lost = []

## play no.
successful_exit_lost_no = []

## any turnover in the defensive zone is an unsuccessful zone exit
unsuccessful_zone_exit = []
unsuccessful_exit_no = []


## length of dataframe
length = len(USCAN)



for i in range(length - 1):

    ## current play
    first = current_event(USCAN, i)

    ## following play
    second = current_event(USCAN, i + 1)

    ## want to exclude plays that result in penalties or stoppages (except goals)
    if 'Penalty Taken' in [first['Event'], second['Event']] or 'Faceoff Win' in [first['Event'], second['Event']]:
        continue
    
    ## if the first play occurs in the defensive zone + next play occurs in nZone or oZone + team retains possession
    ## this is a successful zone exit
    elif first['Zone'] == "Defensive" and second['Zone'] != "Defensive" and first['Team'] == second['Team']:
        successful_zone_exits.append([first, second])
        successful_exit_no.append(i)
    

    ## if the first play occurs in the defensive zone + next play occurs in nZone or oZone but other team has possession
    ## this is a succesful zone exit with lost possession
    elif first['Zone'] == "Defensive" and second['Zone'] in ["Defensive", "Netural"] and first['Team'] != second['Team']:
        successful_zone_exit_lost.append([first, second])
        successful_exit_lost_no.append(i)

    ## if the first play occurs in the defensive zone + next play occurs in dZone but other team has possession
    ## this is an unsuccessful zone exit 
    elif first['Zone'] == "Defensive" and second['Zone'] == "Offensive" and first['Team'] != second['Team']:
        unsuccessful_zone_exit.append([first, second])
        unsuccessful_exit_no.append(i)

## Zone Exits:
## Level 1 = Unsuccessful 
## Level 2 = Successful + lost possession or immediate re-entry (within 10 seconds)
## Level 3 = Successful + possession + stoppage or zone entry or no immediate re-entry (> 10 seconds)
## Level 4 = Successful + Possession + zone entry + shot (within 15 seconds)
## Level 5 = Successful + continous possession + goal (within 30 seconds)


levelone = []
levelone_startend ={}
levelone_break = {}

leveltwo = []
leveltwo_startend = {}
leveltwo_break = {}

levelthree = []
levelthree_startend = {}
levelthree_break = {}

levelfour = []
levelfour_startend = {}
levelfour_break = {}

levelfive = []
levelfive_startend = {}
levelfive_break = {}

## Breakout Level 5
for i in successful_exit_no:
    
    ## current play
    play = current_event(USCAN, i)

    ## next play
    nextplay = current_event(USCAN, i + 1)
    
    possession = True
    j = i + 1

    while possession == True and j < length:
        
        nextplay = current_event(USCAN, j)
        
        ## if possession changes or a faceoff occurs (stoppage) then this does not meet criteria for Level 5
        if (nextplay['Team'] != play['Team']) or (nextplay['Event'] == 'Faceoff Win') or (nextplay['Zone'] == 'Defensive') or (nextplay['Time'] > play['Time'] + 30):
            possession = False

        
        ## if the exit leads to a goal, this is a Level 5 exit
        elif (nextplay['Event'] == 'Goal'):
            levelfive.append(i)
            levelfive_startend[i] = j
            levelfive_break[i] = i + 1
            possession = False
        
        else:
            j = j + 1


## Breakout Level 4
for i in successful_exit_no:
    play = current_event(USCAN, i)
    
    possession = True
    j = i + 1

    while possession == True and j < length:
        
        nextplay = current_event(USCAN, j)

        if (nextplay['Team'] != play['Team']) or (nextplay['Time'] > play['Time'] + 30) or (nextplay['Zone'] == 'Defensive'):
            possession = False

        elif (nextplay['Zone'] == 'Offensive') and nextplay['Event'] == 'Shot' and i not in levelfive:
            levelfour.append(i)
            levelfour_startend[i] = j
            levelfour_break[i] = i + 1
            possession = False
        
        else:
            j = j + 1
            


## Breakout Level 3
for i in successful_exit_no:
    play = current_event(USCAN, i)
    nextplay = current_event(USCAN, i + 1)
    
    continuous = True
    j = i + 1

    while continuous == True and j < length:
        
        nextplay = current_event(USCAN, j)
        
        if (nextplay['Team'] != play['Team'] and nextplay['Zone'] != 'Defensive') or (nextplay['Team'] == play['Team'] and  nextplay['Zone'] == 'Defensive') or nextplay['Time'] > play['Time'] + 15:
            continuous = False
        
        elif (nextplay['Team'] == play['Team'] and nextplay['Zone'] == 'Offensive' and (i not in levelfour + levelfive)) :
            continuous = False
            levelthree.append(i)
            levelthree_startend[i] = j
            levelthree_break[i] = i + 1

        else:
            j = j + 1



## Breakout Level 2
for i in successful_exit_no:
    play = current_event(USCAN, i)
    nextplay = current_event(USCAN, i + 1)
    
    continuous = True
    j = i + 1

    while continuous == True and j < length:
        
        nextplay = current_event(USCAN, j)
        
        if (nextplay['Team'] == play['Team'] and nextplay['Zone'] in ['Offensive', 'Defensive']) or (nextplay['Event'] in ['Penalty Taken', 'Faceoff Won']):
            continuous = False

        elif nextplay['Team'] != play['Team'] and nextplay['Zone'] in ['Defensive', 'Neutral']:
            leveltwo.append(i)
            leveltwo_startend[i] = j
            leveltwo_break[i] = i + 1
            USCAN['Breakout_End X Coordinate'][j] = 200 - USCAN['X Coordinate'][j]
            continuous = False
        
        else:
            j = j + 1

for i in successful_exit_lost_no:
    if i < length - 1: 
        leveltwo.append(i)
        leveltwo_startend[i] = i + 1
        leveltwo_break[i] = i + 1
        USCAN['Breakout_End X Coordinate'][i + 1] = 200 - USCAN['X Coordinate'][i + 1]



## Breakout Level 1

for i in unsuccessful_exit_no:
    if i < length - 1:
        levelone.append(i)
        levelone_startend[i] = i + 1
        levelone_break[i] = i + 1
        USCAN['Breakout_End X Coordinate'][i + 1] = 200 - USCAN['X Coordinate'][i + 1]




## tracking individual player breakout attempts 
player_attempts = {}
player_score = {}


## counting all breakout attempts
for i in levelfive + levelfour + levelthree + leveltwo + levelone:

    player = USCAN.loc[i]['Player']
    if player in player_attempts:
        player_attempts[player] += 1
    
    else:
        player_attempts[player] = 1


## Level 5 breakout = 5 score
for i in levelfive:
    player = USCAN.loc[i]['Player']
    if player in player_score:
        player_score[player] += 5
    
    else:
        player_score[player] = 5


## Level 4 breakout = 4 score
for i in levelfour:
    player = USCAN.loc[i]['Player']
    if player in player_score:
        player_score[player] += 4
    
    else:
        player_score[player] = 4


## Level 3 breakout = 3 score
for i in levelthree:
    player = USCAN.loc[i]['Player']
    if player in player_score:
        player_score[player] += 3
    
    else:
        player_score[player] = 3


## Level 2 breakout = 2 score
for i in leveltwo:
    player = USCAN.loc[i]['Player']
    if player in player_score:
        player_score[player] += 2
    
    else:
        player_score[player] = 2


## Level 1 breakout = 1 score
for i in levelone:
    player = USCAN.loc[i]['Player']
    if player in player_score:
        player_score[player] += 1
    
    else:
        player_score[player] = 1


## calculating each player's individual score
for i in player_score:
    player_score[i] = 100 * player_score[i] / (player_attempts[i] * 5);


names = []

for i in player_attempts:
    names.append(i)

attempts = []
score = []

for i in names:
    attempts.append(player_attempts[i])
    score.append(round(player_score[i], 2))


dict = {'name': names, 'score': score, 'attempts': attempts}

USCAN['Breakout_Level'] = "N/A"
USCAN['Breakout_Pass'] = "N/A"
USCAN['Breakout_End'] = "N/A"


### Classifying plays by their respective breakout score, where applicable
for i in range(len(USCAN)):
    
    if (i in levelfive):
         USCAN['Breakout_Level'][i] = 5
         USCAN['Breakout_Pass'][levelfive_break[i]] = 5 
         USCAN['Breakout_End'][levelfive_startend[i]] = 5

    if (i in levelfour):
        USCAN['Breakout_Level'][i] = 4
        USCAN['Breakout_Pass'][levelfour_break[i]] = 4
        USCAN['Breakout_End'][levelfour_startend[i]] = 4

    if (i in levelthree):
        USCAN['Breakout_Level'][i] = 3
        USCAN['Breakout_Pass'][levelthree_break[i]] = 3
        USCAN['Breakout_End'][levelthree_startend[i]] = 3
    
    if (i in leveltwo):
        USCAN['Breakout_Level'][i] = 2
        USCAN['Breakout_Pass'][leveltwo_break[i]] = 2
        USCAN['Breakout_End'][leveltwo_startend[i]] = 2
    
    if (i in levelone):
        USCAN['Breakout_Level'][i] = 1
        USCAN['Breakout_Pass'][levelone_break[i]] = 1
        USCAN['Breakout_End'][levelone_startend[i]] = 1



## exporting player scores and updated event data with breakout scores as csv files
playerscores = pd.DataFrame(dict)

playerscores.to_csv("BDC_Player_Breakouts.csv", sep=',', index=False, encoding='utf-8')

USCAN.to_csv("BDC_Breakout_Levels_update.csv", sep=',', index=False, encoding='utf-8')