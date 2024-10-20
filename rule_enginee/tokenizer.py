import re
def tokenize(rule_string):
    tokens = re.findall(r"\w+|[><=()]|AND|OR|'[^']+'", rule_string)
    for i, token in enumerate(tokens):
        if token.isdigit():
            tokens[i] = int(token)
        elif token.startswith("'") and token.endswith("'"):
            tokens[i] = token.strip("'")
    return tokens