from pydantic import BaseModel, HttpUrl

class ScrapeSettings(BaseModel):
    limit: int = None
    proxy: HttpUrl = None