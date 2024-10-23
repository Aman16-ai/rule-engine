from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.database import db 
from models.rule_info import RuleInfo
from schemas.ruleSchemas import ruleSerializer
from schemas.evaluateRequest import EvaluateRequest
from bson import ObjectId
from rule_enginee.engine import RuleEnginee
from dotenv import load_dotenv
load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, you can restrict it to specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)






#create an api to store the rules
@app.post("/create_rule")
async def create_rule(ruleInfo:RuleInfo):
    try:
        rule = db['rules'].insert_one(dict(ruleInfo))
        return {"Success":True,"Response":"Rule created successfully"}        
    except Exception as e:
        print(e)
        return {"Error":"Something went wrong"}
    

@app.get("/get_rules")
async def get_rules():
    try:
        rules = db['rules'].find()
        data = ruleSerializer(rules,many=True)
        return {"Success":True,"Response":data}
    except Exception as e:
        print(e)
        return {"Error":"Something went wrong"}
    

@app.post("/evaluate_against_rule")
async def evaluate_against_rule(evaluateRequest:EvaluateRequest):
    # payload will contain the rule_id and data
    try:
        rule_id = evaluateRequest.rule_id
        data = evaluateRequest.data
        rule = db['rules'].find_one({"_id":ObjectId(rule_id)})
        ruleObj = ruleSerializer(rule)
        createCombinedRule = False

        if len(ruleObj['rules'])>1:
            createCombinedRule = True
        

        engine = RuleEnginee()
        ast = None
        if createCombinedRule:
            ast = engine.combine_rules(ruleObj['rules'])
        else:
            ast = engine.create_rule(ruleObj['rules'][0])
        
        evalutation = engine.evaluate_rule(ast,data)


        return {"Success":True,"Response":evalutation}
    except Exception as e:
        print(e)
        return {"Error":"Something went wrong"}


#create an api to build ast from the rules and evalute the rule
#payload contents -> type of ast(single or combined_rule), selected rules and test data