from pydantic import BaseModel

class Usercreateshcema(BaseModel):
    username:str
    password:str
    class Config:
        extra="forbid"

class Userdeletescheme(BaseModel):
    username:str
    class Config:
        extra="forbid"
        
class GetUserschema(BaseModel):
    username:str
    class Config:
        extra="forbid"
        
class UpdateUserschema(BaseModel):
    password:str
    class config:
        extra="forbid"
        
