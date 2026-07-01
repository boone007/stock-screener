from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import time
import logging

from app.core.config import get_settings
from app.api.routes import score, fundamentals, technicals, sentiment, risk

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "Zen Rating-style multi-factor stock scoring API. "
        "Provides data-driven analysis and probability estimates. "
        "NOT financial advice."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url=f"{settings.api_v1_prefix}/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    response.headers["X-Process-Time"] = f"{(time.time() - start) * 1000:.2f}ms"
    response.headers["X-API-Version"] = settings.app_version
    return response


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "path": str(request.url)},
    )


prefix = settings.api_v1_prefix
app.include_router(score.router, prefix=f"{prefix}/score", tags=["Scoring"])
app.include_router(fundamentals.router, prefix=f"{prefix}/fundamentals", tags=["Fundamentals"])
app.include_router(technicals.router, prefix=f"{prefix}/technicals", tags=["Technicals"])
app.include_router(sentiment.router, prefix=f"{prefix}/sentiment", tags=["Sentiment"])
app.include_router(risk.router, prefix=f"{prefix}/risk", tags=["Risk"])


@app.get("/", tags=["Health"])
async def root():
    return {
        "service": settings.app_name,
        "version": settings.app_version,
        "status": "operational",
        "docs": "/docs",
        "disclaimer": "For informational purposes only. Not financial advice.",
    }


@app.get("/health", tags=["Health"])
async def health():
    return {"status": "healthy", "version": settings.app_version}
