from fastapi import FastAPI
from app.database.connection import engine
from app.database.models import Base
from app.services import insights_service

# Initialize FastAPI app
app = FastAPI(title="SpendMind")

# Create all database tables
Base.metadata.create_all(bind=engine)


@app.get("/")
def health_check():
    """
    Health check endpoint.
    Used to verify that the API is running.
    
    Returns:
        dict: Status of the API.
    """
    return {"status": "ok"}


# Include routers for various endpoints
from app.routes.expenses import router as expenses_router
app.include_router(expenses_router)

from app.routes.categories import router as categories_router
app.include_router(categories_router)

from app.routes.reports import router as reports_router
app.include_router(reports_router)

from app.routers import insights
app.include_router(insights.router)

from app.routers import charts
app.include_router(charts.router)
