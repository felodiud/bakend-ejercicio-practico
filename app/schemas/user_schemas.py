from pydantic import BaseModel

class CreatrUser(BaseModel):
    username: str
    full_name: str
    email: str
    password: str
        


