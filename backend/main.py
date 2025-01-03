from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware

from backend.core.config import RedisConfig
from backend.core.dependencies.dependencies import get_current_user_dependency
from backend.core.redis_cache import RedisCache
from backend.database.connection.connection import DatabaseConnection
from backend.routers.auth import router as auth_router


async def lifespan(app: FastAPI):
    app.state.redis_cache = await RedisCache()()
    app.state.db_connection = await DatabaseConnection()()
    yield


app = FastAPI(lifespan=lifespan)
PROTECTED = Depends(get_current_user_dependency)


origins = ["http://localhost:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    try:
        errors = []

        for error in exc.errors():
            field = error["loc"]
            input = error["input"]
            message = error["msg"]

            if isinstance(input, dict):
                input = input.get(field[-1])

            errors.append(
                {
                    "location": " -> ".join(field),
                    "detail": message,
                    "input": input,
                }
            )

        return JSONResponse(content=errors, status_code=422)
    except TypeError:
        return JSONResponse(
            status_code=422, content={"detail": "invalid json"}
        )
