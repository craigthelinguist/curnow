__author__ = 'craig'

from sys import exit

class Grammar(object):

    def __init__(me):
        me.rules = {}

    def addRule(me, rule_name, definition):
        if rule_name in me.rules:
            print("Error: adding rule {}, but this has already been defined.".format(rule_name))
            exit(1)
        me.rules[rule_name] = definition
