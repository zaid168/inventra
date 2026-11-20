from fastapi import FastAPI
from app.routers import items, inventory, transactions
from app.routers import categories

app = FastAPI(
    title="INVENTRA API",
    description="Intelligent Inventory Management and Blockchain-Based Supply Chain Traceability System",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to INVENTRA API",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }

app.include_router(items.router, prefix="/api")
app.include_router(inventory.router, prefix="/api")
app.include_router(transactions.router, prefix="/api")
app.include_router(categories.router, prefix="/api")
