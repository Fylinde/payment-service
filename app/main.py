from fastapi import FastAPI
from app.routes import payment
from fastapi.middleware.cors import CORSMiddleware
import logging
from fastapi.staticfiles import StaticFiles
import os


logger = logging.getLogger(__name__)

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn.error")

app = FastAPI(
    title="Payment Service API",
    version="1.0.0",
    description="A dedicated service for handling payment processing, tokenization, and transaction management.",
    openapi_tags=[
        {"name": "payment", "description": "Operations related to payment processing and tokenization"},
        {"name": "transactions", "description": "Operations for managing payment transactions"},
        {"name": "billing", "description": "Operations for handling billing and billing addresses"},
    ],
)



# Include payment router
app.include_router(payment.router, prefix="/api", tags=["payment"])

static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")
#@app.on_event("startup")
#async def startup():
    ##create_tables()
    
origins = [
    "http://localhost:3000",  # Your frontend application
]


# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow these origins
    allow_credentials=True,  # Allow cookies and credentials
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

@app.on_event("startup")
async def startup_event():


    # Ensure the scheduler is running when the app starts

    for route in app.router.routes:
        print(route.path, route.name)
       # Ensure the scheduler is running when the app starts

@app.get("/")
def read_root():
    return {"message": "Welcome to the User Service!"}