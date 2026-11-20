from fastapi import FastAPI

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

