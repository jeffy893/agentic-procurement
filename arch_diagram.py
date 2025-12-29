from diagrams import Diagram, Edge
from diagrams.aws.compute import Lambda
from diagrams.aws.database import Dynamodb
from diagrams.aws.ml import Bedrock
from diagrams.aws.integration import Eventbridge

with Diagram("Autonomous Procurement System", show=False, direction="LR"):
    scheduler = Eventbridge("EventBridge\nScheduler")
    lambda_func = Lambda("Procurement\nLambda")
    dynamodb = Dynamodb("Raw Materials\nInventory")
    bedrock = Bedrock("Claude AI\nBedrock")
    
    scheduler >> Edge(label="Daily Trigger") >> lambda_func
    lambda_func >> Edge(label="Read Inventory") >> dynamodb
    lambda_func >> Edge(label="Generate Email") >> bedrock