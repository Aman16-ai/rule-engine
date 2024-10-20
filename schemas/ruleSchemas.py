from models.rule_info import RuleInfo

def serliaze(ruleInfo):
    return {
        "id" : str(ruleInfo['_id']),
        "title":ruleInfo['title'],
        "rules":ruleInfo['rules']
    }

def ruleSerializer(data,many=False) -> dict|list[dict]:
    if(not many):
        return serliaze(data)

    return [serliaze(d) for d in data] 


