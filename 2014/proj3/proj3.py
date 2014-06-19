import random
from itertools import *
from operator import *

pre_order = {'2':13, 'A':12, 'K':11, 'Q':10, 'J':9, '0':8, '9':7, '8':6,
                 '7':5,  '6':4,  '5':3,  '4':2,  '3':1 }

def preprocess(hand):
    '''
    >>> hand = ['JS','QD','KC','7S','9H','4C','0C','9C','5H','3C','JH','2H','8D']
    >>> pre_process(hand)
    [(9, 'S'), (10, 'D'), (11, 'C'), (5, 'S'), (7, 'H'), (2, 'C'), (8, 'C'), (7, 'C'), 
     (3, 'H'), (1, 'C'), (9, 'H'), (13, 'H'), (6, 'D')]
    '''
    return [(pre_order[item[0]],item[1]) for item in hand]

 
def postprocess(hand):
    '''
    >>> hand = [(9, 'S'), (10, 'D'), (11, 'C'), (5, 'S'), (7, 'H'), (2, 'C'), (8, 'C'), (7, 'C'), 
     (3, 'H'), (1, 'C'), (9, 'H'), (13, 'H'), (6, 'D')]
    >>> postprocess(hand)
    ['KC', 'JS', 'JH', 'QD', '0C', '3C', '2H', '5H', '4C', '7S', '9H', '9C', '8D']
    '''
    return [item1[0]+item2[1] for item1,item2 in list(product(pre_order.items(),hand)) if item1[1] == item2[0]]


def player0_2highest(hand):
    '''
    >>> hand = [(9, 'S'), (10, 'D'), (11, 'C'), (5, 'S'), (7, 'H'), (2, 'C'), 
                (8, 'C'), (7, 'C'), (3, 'H'), (1, 'C'), (9, 'H'), (13, 'H'), (6, 'D')]
    >>> player0_2highest(hand)
    ((13, 'H'), (11, 'C'))
    '''
    high1,high2 = '',''
    h1,h2 = 0,0
    for card in hand:
        if card[0]>h1:
            high1 = card
            h1 = card[0]
    hand.remove(high1)
    for card in hand:
        if card[0]>h2:
            high2 = card
            h2 = card[0]
    return (high1,high2)


def player1_1highest(hand):
    '''
    >>> hand = [(9, 'S'), (10, 'D'), (11, 'C'), (5, 'S'), (7, 'H'), (2, 'C'), 
                (8, 'C'), (7, 'C'), (3, 'H'), (1, 'C'), (9, 'H'), (13, 'H'), (6, 'D')]
    >>> player1_1highest(hand)
    (13, 'H')
    '''
    maximum,m = '',0
    for card in hand:
        if card[0]> m:
            maximum = card
            m = card[0]
    return maximum


def player2_1random(hand):
    '''
    Note: Assume randomly choose a card
    >>> hand = [(9, 'S'), (10, 'D'), (11, 'C'), (5, 'S'), (7, 'H'), (2, 'C'), 
                (8, 'C'), (7, 'C'), (3, 'H'), (1, 'C'), (9, 'H'), (13, 'H'), (6, 'D')]
    >>> player2_1random(hand)
    (11, 'C')
    '''
    return random.choice(hand)


def player3_2random(hand):
    '''
    Note: Assume randomly choose a card
    >>> hand = [(9, 'S'), (10, 'D'), (11, 'C'), (5, 'S'), (7, 'H'), (2, 'C'), 
                (8, 'C'), (7, 'C'), (3, 'H'), (1, 'C'), (9, 'H'), (13, 'H'), (6, 'D')]
    >>> player3_2random(hand)
    ((7, 'H'), (5, 'S'))
    '''
    cho1 = random.choice(hand)
    hand.remove(cho1)
    return (cho1,random.choice(hand))


def swap_cards(hand, pid):
    if pid == 0:
        return player0_2highest(hand)
    elif pid == 1:
        return player1_1highest(hand)
    elif pid == 2:
        return player2_1random(hand)
    elif pid == 3:
        return player3_2random(hand)
    else:
        return 'invalid input player id'
 

def n_of_a_kind(hand):
    '''
    >>> hand = [(9, 'S'), (10, 'D'), (11, 'C'), (5, 'S'), (7, 'H'), (2, 'C'), 
                (8, 'C'), (7, 'C'), (3, 'H'), (1, 'C'), (9, 'H'), (13, 'H'), (6, 'D')]
    >>> n_of_a_kind(hand)
    [[(1, 'C')], [(2, 'C')], [(3, 'H')], [(5, 'S')], [(6, 'D')], [(7, 'C'), (7, 'H')], 
     [(8, 'C')], [(9, 'H'), (9, 'S')], [(10, 'D')], [(11, 'C')], [(13, 'H')]]
    '''
    return [list(v) for k,v in groupby(sorted(hand),key=lambda x:x[0])]


def straight(nums):
    '''
    >>> list(enumerate(seasons))
    [(0,'Spring'),(1,'Summer'),(2,'Autumn'),(3,'Winter')]
    >>> num1 = [(1, 'H'), (2, 'H'), (3, 'H'), (4, 'H')]    
    >>> straight(num1)
    [[(1, 'H'), (2, 'H'), (3, 'H'), (4, 'H')]]
    >>> num2 = [(1, 'H'), (2, 'H'), (4, 'H')]
    >>> straight(num2)
    []
    >>> num3 = [(1, 'H'), (2, 'H'), (3, 'S')]
    >>> straight(num3)
    []
    >>> num4 = [(1, 'H'), (2, 'H'), (3, 'H'), (4, 'H'),(5,'S'),(7,'D'),(8,'D'),(9,'D')]
    [[(1, 'H'), (2, 'H'), (3, 'H'), (4, 'H')], [(7, 'D'), (8, 'D'), (9, 'D')]]
    '''
    result = []
    sorted_nums = sorted(nums,key=lambda x:x[0])
    for k,v in groupby(enumerate(sorted_nums),lambda(i,x):i-x[0]):
        g = map(itemgetter(1),v) # get cards with same number
        g = [list(v) for k,v in groupby(g,lambda x:x[1])][0] # get cards with same suit
        suit = [item[1] for item in g]
        if len(g) >= 3:
            result.append(g)
    return result


def generate_plays(hand):
    '''
    Note: non-pass plays
    >>> hand = [(13, 'S'), (1, 'S'), (2, 'H'), (3, 'D'), (11, 'S'), (6, 'H'), (12, 'S')]
    >>> generate_plays(hand)
    [[(1, 'S')], [(2, 'H')], [(3, 'D')], [(6, 'H')], [(11, 'S')], [(12, 'S')], [(13, 'S')], 
     [(11, 'S'), (12, 'S'), (13, 'S')]]
    '''
    result = n_of_a_kind(hand)
    for item in straight(hand):
        if len(item) > 0:
            result.append(item)
    return result

def check_play_type(last_play):
    '''
    Output:
    0 - a pass
    1 - n-of-a-kind
    2 - straight

    >>> last_play = [(3, 'S'), (3, 'C')]
    >>> last_play = [(3, 'S'), (4, 'S')]
    '''
    num = [item[0] for item in last_play]
    suit = [item[1] for item in last_play]
    if len(last_play) == 0:
        return 0
    elif len(last_play) == 1:
        return 1
    elif all(x == num[0] for x in num):
        return 1
    elif all(x == suit[0] for x in suit):
        return 2
    else:
        return 'Unknown play type'        


def compare_value(play,last_Nonpass_play):
    '''
    >>> play = [(2, 'D'), (2, 'H')]
    >>> last_Nonpass_play = [(1, 'D'), (1, 'S')]
    '''
    play_value = [item[0] for item in play]
    last_value = [item[0] for item in last_Nonpass_play]
    if max(play_value) > max(last_value):
        return True
    else:
        return False


def check_suit_1kind(play,last_2Nonepass_play):
    '''
    Note: Assume input is 1-of-a-kind
    >>> play = [(2, 'H')]
    >>> last_2Nonepass_play = [[(3, 'C')],[(4, 'C')]]
    >>> check_suit_1kind(play,last_2Nonepass_play) 
    False
    '''
    suit = [item[0][1] for item in last_2Nonepass_play]
    if not all(x == suit[0] for x in suit):
        return True
    elif all(x == suit[0] for x in suit) and play[0][1] != suit[-1]:
        return False
    elif all(x == suit[0] for x in suit) and play[0][1] == suit[-1]:
        return True
    else:
        return 'Uncover situation in check_suit_1kind function'


def is_valid_play(play,rnd):
    '''
    Input: 
    play - a list of cards
    rnd - the round to date, in the form of a list of plays in sequential order,
          each of which is, in turn, a list of cards
    
    Output:
    a Boolean - True if given play is valid; False otherwise
    
    Note: 
    1. Assume play constitutes a legal combination of cards, including a pass (None)
    2. The current round is not lead

    >>> is_valid_play(['AD'],[['5S','5C'],['6H','6C']])
    False
    >>> is_valid_play([(12, 'D')],[[(3, 'S'), (3, 'C')],[(4, 'H'), (4, 'C')]])
    False
    '''
    if check_play_type(play) == 0:
        return True
    elif check_play_type(rnd[-1]) == 1 and check_play_type(play) != 1:
        return False
    elif check_play_type(rnd[-1]) == 1 and len(play) != len(rnd[-1]):
        return False
    elif check_play_type(rnd[-1]) == 2 and check_play_type(play) != 2:
        return False
    elif check_play_type(rnd[-1]) != 0 and not compare_value(play,rnd[-1]): 
        return False
    elif check_play_type(rnd[-1]) == 1 and not check_suit_1kind(play,rnd[:-2]):
        return False
    elif check_play_type(rnd[-1]) == 1 and check_suit_1kind(play,rnd[:-2]):
        return True
    else:
        return 'Uncover situation in is_valid_play function'

def tabulate_discard(discard):
    '''
    Input: discard - the history of the game so far
    >>> 
    '''
    return


def strategy1(rnd,hand,generate=generate_plays,valid=is_valid_play):
    '''
    Note: Always return the play that is valid and can get rid of most of cards
    '''
    generate.sort(lambda x,y:cmp(len(x),len(y)))
    card = []
    for item in generate:
        if valid(item) == True:
            card = item
    return card


def play(rnd, hand, discard, holding, generate=generate_plays,valid=is_valid_play):
    '''
    Input: rnd      - a list of plays from the round to date
           hand     - the current cards held by your player
           discard  - a list, containg the history of the game so far. Each element
                      in the list represents a round, in order of play in the game.
                      Each round is a list. The values in the list are the cards plays 
                      for the round, in the ordder they were played.
                      None represents a pass.
           holding  - a 4-tuple made up of int values representing how many cards 
                      each of the players is holding, indexed by the player ID
           generate - function generate_plays, optional argument
           valid    - function is_valid_play, optional argument

    Output: A list of cards or None
    
    Note: Aims to get rid of all the cards at hand as soon as possible. 
          Cards are given out according to the rnd
    
    >>> hand = ['JS','QD','KC','7S','9H','4C','0C','9C','5H','3C','JH','2H','8D']
    >>> hand = [(9, 'S'), (10, 'D'), (11, 'C'), (5, 'S'), (7, 'H'), (2, 'C'), 
                (8, 'C'), (7, 'C'), (3, 'H'), (1, 'C'), (9, 'H'), (13, 'H'), (6, 'D')]
    >>> generate_plays(hand)
    [[(1, 'C')], [(2, 'C')], [(3, 'H')], [(5, 'S')], [(6, 'D')], [(7, 'C'), (7, 'H')], 
     [(8, 'C')], [(9, 'H'), (9, 'S')], [(10, 'D')], [(11, 'C')], [(13, 'H')]]
    >>> play([],hand,[],[13,13,13,13])
    [(1, 'C')] # ['3C']
    >>> discard = [[[(3,'S')],[(4,'C')],[(5,'D')],[(6,'H')]],
                   [[(7,'H')],[(8,'D')],[(9,'S')],[(10,'S')]],
                   [[(11, 'S')],[(12, 'H')],[(13,'S'))],None]]
    '''
    generate = generate
    if len(rnd) = 0:
        for item in generate:
    else:
        
        rnd = []
        discard.append(rnd)
    holding = {id:int}



