from .node import Node
def parse_tokens(tokens):
    def parse_expression(index):
        lhs, index = parse_term(index)
        while index < len(tokens) and tokens[index] in ('AND', 'OR'):
            operator = tokens[index]
            index += 1
            rhs, index = parse_term(index)
            lhs = Node(node_type="operator", value=operator, left=lhs, right=rhs)
        return lhs, index

    def parse_term(index):
        if index >= len(tokens):
            raise ValueError("Unexpected end of tokens while parsing")

        if tokens[index] == '(':
            index += 1
            expr, index = parse_expression(index)
            if index >= len(tokens) or tokens[index] != ')':
                raise ValueError("Expected ')' after expression")
            index += 1  # Skip ')'
            return expr, index
        else:
            # Parse condition: e.g., "age > 30"
            if index + 2 >= len(tokens):
                raise ValueError("Not enough tokens to parse a condition")

            key = tokens[index]
            operator = tokens[index + 1]
            value = tokens[index + 2]
            index += 3
            return Node(node_type="operand", value=(key, operator, value)), index

    ast, index = parse_expression(0)
    if index < len(tokens):
        raise ValueError("Unused tokens after parsing: " + str(tokens[index:]))
    return ast