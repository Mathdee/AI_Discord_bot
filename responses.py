#imports
from random import choice,randint
from quote import quotes
from quote import riddles
import requests


#output only when condition is met
def get_response(user_input : str) -> str:
    lowered: str = user_input.lower()
    if '/flipcoin' in lowered:
        coins = randint(1,2)
        if coins == 2:
            return '`You landed on: Heads`'
        else:
            return '`You landed on: Tails`'
    elif '/info' in lowered:
        return '`My goal is to assist you` :grin:\n'
    elif '/quote' in lowered:
        return choice(quotes)
    elif '/riddle' in lowered:
        return choice(riddles)
    else:
        return ValueError
    


    
