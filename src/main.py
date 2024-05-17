import sentry_sdk
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.redis import RedisIntegration
from src.config import settings
from src.eureka import EurekaAuth
from src.exceptions import ExceptionHandlerRegistration
from src.user_management.api.v1 import router as user_router

sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
    integrations=[RedisIntegration(), FastApiIntegration()],
)

app = FastAPI()
app.title = "User-Management-Service"
app.include_router(user_router.router)

# register all exceptions
ExceptionHandlerRegistration.register_all_exceptions(app)
origins = settings.ORIGINS.split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    # register auth-service in eureka
    await EurekaAuth.register_with_eureka()
    


@app.on_event("shutdown")
async def shutdown_event():
    # unregister auth-service in eureka
    await EurekaAuth.unregister_from_eureka()
