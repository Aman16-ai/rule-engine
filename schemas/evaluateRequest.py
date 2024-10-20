from pydantic import BaseModel


class EvaluateRequest(BaseModel):
    rule_id : str
    data : dict