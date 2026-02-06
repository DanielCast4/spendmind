from pydantic import BaseModel

class InsightsResponse(BaseModel):
    """
    Response model for returning insights from the API.
    
    Attributes:
        insights (list[str]): A list of insight messages or statements.
    """
    insights: list[str]
