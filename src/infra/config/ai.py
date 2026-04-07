from pydantic import BaseModel


class AiConfig(BaseModel):
    token: str
    base_url: str
    model_name: str
