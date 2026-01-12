from api.groq_router_API import router as groq_router
from api.groq_router_full_API import router as groq_router_full
from fastapi import FastAPI

app = FastAPI(
    title="MarketingIA API",
    description="API para marketing digital",
    version="1.0.0"
)
app.include_router(groq_router, tags=["MarketingIA"])
app.include_router(groq_router_full, tags=["MarketingIA Full"])
