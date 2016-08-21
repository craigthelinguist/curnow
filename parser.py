
from grammar import Grammar

# These are significant characters.
DELIMS = ["[", "]", "<", ">", "*", "?", "+", '"']

oper2ast = {
    "?": "OPTIONAL",
    "+": "AT_LEAST_ONE",
    "*": "ANY"
}

def parse_err(msg):
    print "Parsing error: " + msg
    exit(1)

def parse_step(tokens):

    if tokens[0] == "<":
        result = ["RULE", tokens[1]]
        if not tokens[2] == ">":
            parse_err("< block began without an ending >")
            exit(1)
        return tokens[3:], result

    if tokens[0] == "[":
        try:
            endOfGroup = tokens.index("]")
            group = parse_ast(tokens[1:endOfGroup])
            if len(tokens) < endOfGroup + 1:
                parse_err("no operator modifying the group {}".format(group))
            oper = oper2ast[tokens[endOfGroup+1]]
            return [oper, group]
        except ValueError:
            parse_err("[ block began without an ending ]")

    if tokens[0] == '"':
        if not tokens[2] == '"':
            parse_err('" literal began without a closing "')
        if tokens[2] in DELIMS:
            parse_err("Misuse of operator: {}".format(tokens[1]))
        return ["LITERAL", tokens[1]]

def parse_ast(tokens):

    # A single token (string literal) compiles to itself.
    if len(tokens) == 1:
        if tokens[0] in DELIMS: parse_err("Malformed use of an operator: ".format(tokens[0]))
        return tokens[0]

    # Otherwise check the next token and act appropriately.
    defn = []
    while len(tokens) > 0:
        result, tokens = parse_step(tokens)
        if type(result) == list: defn += result
        else: defn.append(result)

    return defn






def parse_definition(text):
    # Split by significant tokens & characters.
    for line in text:
        for delim in DELIMS:
            line = line.replace(delim, " " + delim + " ")
        line = line.split()
        return parse_ast(line)



def parse_rule(text, grammar):

    # Get the name of the rule.
    name_of_rule = text[0].split()[0]
    text = text[1:]

    # Sanity check.
    if len(text) == 0:
        parse_err("The rule {} has no definitions.".format(name_of_rule))

    # Rule is a single definition.
    if len(text) == 1:
        defn = parse_definition(text, grammar)
        grammar.addRule(name_of_rule, defn)
        return

    # Rule has several definitions.
    defns = [parse_definition(l) for l in text]
    return ["OR"] + defns





def parse_grammar(fname):

    # Load contents of file into a string.
    text = None
    with open(fname, "rb") as f:
        text = f.read()

    # Keep parsing rules, while there are rules to parse.
    grammar = Grammar()
    text = text.split("\n")
    for line_num, line in enumerate(text):

        print "line {}: {}".format(line_num, line)

        line = line.lstrip().rstrip()
        if len(line) == 0: continue
        if ":=" in line:
            parse_rule(text[line_num:], grammar)
        else:
            print("Malformed file at line {}: {}".format(line_num, line))

    return grammar