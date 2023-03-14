"""
Written by John Brilhart
Date: 2/8/2022

About:
Eliza Weizenbaum is a program created in the 1960s to replicate a Rogerian psychotherapist. Rogan psychotherapists are all person centric,
so they dont need to know any information about worldy matters. This makes writing a chatbot much easier.

Usage:
Start the program in a terminal, using python version 3 and type in your name as prompted, after that you can attempt to talk with the bot as if it was a real psychotherapist.
The one constraint is that every response given to the bot must be one sentance with a period at the end.

Example:
C:\> python eliza.py
Hello, my name is Eliza, what is yours?
>John
Hello, John. How can I help you?
>I want to be powerfull.
What if you never got to be powerfull?


Algorithm:
In the main function it will start the input response loop. For every loop it will take in a response, then look for rules in the findRules function. Where it will look for the keywords in the rules dictionary
and if found will save the groupname. With the list of found groups it will run the applyRules, where it will use the groups of words to decide which rules to use. The rule combinations are stored in the tranformRules list.
Every item in the transformRules list has its set of rules needed, and a corresponding function that will be used to build the response. applyRules will take that function and apply it to give the response back to the main loop.
Finally the main loop will reflect all first person pronouns into second person pronouns.
"""

import re
import random

# WORD GROUPS
rules = {"relationship":['parents?', '[a-z]*friend', 'brother', 'sister', 'my', 'me', 's?he', 'they'],
"desire": ['want', 'need', 'desire', 'crave'],
"feeling": ['hate', 'like', 'love', 'dislike'],
"aboutMe": ['i', 'me', 'my', 'mine', 'myself'],
"aboutOthers": ['[a-z]body'],#['nobody', 'somebody', 'anybody', 'everybody']),
"absolutes": ['never', 'always', '[a-z]body|no\sbody'],
"possesive": ["my", "her", "his", "have", "has"]}

ops = {"wordbefore":"(\S+)\s", "inclusivewordafter":"", "restafter":"\s(.+)"}

# If Eliza is confused it will pick one of these at random
genericResponse = ["Tell me more.", "Lets talk more about that.", "Can you restate that for me?", "I see.", "Do you feel that way?"]

def buildTransformFunction(pre, post, *regsfuncs):
# builds function for each ruleset

    def transformFunction(response):
        # combines pre post, and the result of all regex
        middle = " ".join([x(response) for x in regsfuncs])
        response = f"{pre} {middle}{post}"
        return(response)

    return(transformFunction)

def grabwithRules(rules, post='', pre='', pos=0):
    def thefunc(response):
        regex = joinrules(rules, pre, post)
        match = re.search(regex, response)
        result = match.group(pos)

        return(result)

    return(thefunc)

# Transform rules
# Using the found word groups we can have a pattern and a rank for different rules
# Rank is implied here by order of rules
transformRules = [({'absolutes'}, buildTransformFunction("Really?", "?", grabwithRules(rules['absolutes']))),
                    ({"feeling", "relationship"}, buildTransformFunction("Why does", "?", str)),
                    #({}, buildTransformFunction("Why does", "?", str)),
                    ({"possesive"}, buildTransformFunction("Why do you", "?", grabwithRules(rules['possesive'], post="\s(.+)", pos=0))),
                    ({'desire'}, buildTransformFunction("What if you never got", "?", grabwithRules(rules['desire'], post="\s(.+)", pos=1)))]#,
                    #({}, buildTransformFunction("Why does", "?", str)),
                    #({}, buildTransformFunction("Why does", "?", str))]  
                    # use a regex in fstring to reference words




def joinrules(rules, pre='', post=''):
    rules = [pre+x+post for x in rules] 
    return('|'.join(rules))

def findRules(response, ruleSet=rules):
    FoundRules = []
    for rulename, mapp in ruleSet.items():
        regularexps = mapp
        match = re.search('|'.join(regularexps), response)
        if match:
            FoundRules.append(rulename)

    return(FoundRules)

def applyRules(response, rules):
    rules = set(rules)

    for ruleset in transformRules:
        transform = ruleset[1]  # transform is just a function
        ruleset = ruleset[0]

        if ruleset.issubset(rules):
            # phrase has all of the rules, so use its transform regex

            response = transform(response)
            return(response)

    # If no rules are found then it will return a random generic
    return(random.choice(genericResponse))


        
# for flipping me to you, etc
reflective = {"my":"your", "myself":"yourself", "me":"you", "\bi\b":"you"}

def reflect(response):
    # takes respone and turns all me's into you's and so on
    for this, that in reflective.items():
        response = re.sub(this, that, response)

    return(response)

def inputIsValid(input):
    # Checks to make sure input is one sentance
    match = re.search('[\.\?\!]', input)
    if match:
        return True
    else:
        return False
    
def processResponse(response):
    # turn into all lowercase
    response = response.lower()

    if response == 'quit':
        quit()

    if not inputIsValid(response):
        raise ValueError

    response = response[:-1]

    rules = findRules(response)
    resp = applyRules(response, rules)
    resp = reflect(resp)

    return resp



def main():
    # starts convo, and runs question/statement loop till quit
    print("Hello, my name is Eliza, what is yours?")
    name = input()
    print(f"Hello, {name}. How can I help you?")
    while True:
        response = input(">")

        try:
            resp = processResponse(response)
        except ValueError:
            print("Could you say that again for me in a single sentance?")
            continue

        print(resp)


if __name__ == '__main__':
    main()