import re
from .parser import parse_tokens
from collections import Counter
from .node import Node
class RuleEnginee:

    def tokenize(self,rule_string):
        tokens = re.findall(r"\w+|[><=()]|AND|OR|'[^']+'", rule_string)
        for i, token in enumerate(tokens):
            if token.isdigit():
                tokens[i] = int(token)
            elif token.startswith("'") and token.endswith("'"):
                tokens[i] = token.strip("'")
        return tokens
    
    def create_rule(self,rule_string):
        tokens = self.tokenize(rule_string)
        ast = parse_tokens(tokens)
        return ast
    
    def combine_rules(self,rules):
        asts = []
        operator_count = Counter()

        # Tokenize and parse each rule to get its AST
        for rule in rules:
            # tokens = tokenize(rule)
            # ast = parse_tokens(tokens)
            ast = self.create_rule(rule)
            asts.append(ast)

            # Count the operators in the current rule's AST
            def count_operators(node):
                if node is None:
                    return
                if node.type == "operator":
                    operator_count[node.value] += 1
                count_operators(node.left)
                count_operators(node.right)

            count_operators(ast)

        # Determine the most frequent operator
        if operator_count:
            most_common_operator = operator_count.most_common(1)[0][0]  # Get the most common operator
        else:
            raise ValueError("No operators found in the provided rules.")

        # Combine the ASTs using the most common operator
        combined_ast = asts[0]
        for ast in asts[1:]:
            combined_ast = Node(node_type="operator", value=most_common_operator, left=combined_ast, right=ast)

        return combined_ast


    def print_ast(self,node,level=0):
        if node is None:
            return
        indent = "  " * level
        if node.type == "operand":
            print(f"{indent}Operand: {node.value}")
        elif node.type == "operator":
            print(f"{indent}Operator: {node.value}")
        
        # Recursively print the left and right children
        if node.left:
            print(f"{indent}Left:")
            self.print_ast(node.left, level + 1)
        if node.right:
            print(f"{indent}Right:")
            self.print_ast(node.right, level + 1)

    def evaluate_rule(self,ast,context):
        return ast.evaluate(context)
    


if __name__ == "__main__":
    engine = RuleEnginee()
    rule1 = "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)"

    ast = engine.create_rule(rule1)

    # Sample employee data
    employee_1 = {'age': 38, 'department': 'Sales', 'salary': 55000, 'experience': 4}
    employee_2 = {'age': 24, 'department': 'Marketing', 'salary': 40000, 'experience': 6}
    employee_3 = {'age': 28, 'department': 'HR', 'salary': 48000, 'experience': 3}  # Invalid case

    print("Employee 1 passes rule:", engine.evaluate_rule(ast, employee_1))  # True
    print("Employee 2 passes rule:", engine.evaluate_rule(ast, employee_2))  # True
    print("Employee 3 passes rule:", engine.evaluate_rule(ast, employee_3)) 