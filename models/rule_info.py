from pydantic import BaseModel

class RuleInfo(BaseModel):
    title:str
    rules : list[str]



