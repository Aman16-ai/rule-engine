class Node:
    def __init__(self, node_type, value=None, left=None, right=None):
        self.type = node_type  # "operator" or "operand"
        self.value = value      # Can hold the condition for operand nodes
        self.left = left        # Reference to the left child
        self.right = right      # Reference to the right child

    def evaluate(self, context):
        if self.type == "operand":
            return self.evaluate_condition(context)
        elif self.type == "operator":
            return self.evaluate_operator(context)

    def evaluate_condition(self, context):
        key, operator, value = self.value

        # Check if the key exists in the context and is not None
        if key not in context or context[key] is None:
            raise ValueError(f"Key '{key}' is not present in the context or is None")

        # Validate operator
        if operator not in ['>', '<', '=']:
            raise ValueError(f"Invalid operator: {operator}")

        # Validate the type of the context value
        if operator in ['>', '<'] and not isinstance(context[key], (int, float)):
            raise ValueError(f"Value for '{key}' must be a number for operator '{operator}'")
        elif operator == '=' and not isinstance(context[key], str):
            raise ValueError(f"Value for '{key}' must be a string for operator '{operator}'")

        # Perform the comparison
        if operator == '>':
            return context[key] > value
        elif operator == '<':
            return context[key] < value
        elif operator == '=':
            return context[key] == value

    def evaluate_operator(self, context):
        if self.value == 'AND':
            return self.left.evaluate(context) and self.right.evaluate(context)
        elif self.value == 'OR':
            return self.left.evaluate(context) or self.right.evaluate(context)
        else:
            raise ValueError(f"Unknown operator: {self.value}")
