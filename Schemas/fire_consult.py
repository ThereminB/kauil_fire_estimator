from pydantic import BaseModel

class FireData(BaseModel):
    latitude            : str
    longitude           : str
    fire_start_date     : str