from fastapi import HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from src.schemas import ResponseSchema, ValidationResponseSchema


class ErpProductAuthException:
    async def http_exception_handler(self, request: Request, exc):
        status_code = exc.status_code

        if isinstance(exc.detail, str):
            error_message = exc.detail
        elif isinstance(exc.detail, ResponseSchema):
            error_message = exc.detail.message
        else:
            error_message = "An error occurred."

        return JSONResponse(
            content={
                "message": ResponseSchema(
                    code=status_code, message=error_message, data=[]
                ).__dict__
            },
            status_code=status_code,
        )

    async def validation_exception_handler(self, request: Request, exc):
        error_messages = exc.errors()

        validation_errors = {}
        for error in error_messages:
            if error.get("ctx"):
                try:
                    validation_errors.update(error["ctx"]["error"].args[-1])
                except KeyError:
                    field_name = error["loc"][-1]
                    error_msg = error["msg"]
                    validation_errors[field_name] = [error_msg]
                except Exception:
                    validation_errors[error["loc"][-1]] = error["ctx"]["error"]
            else:
                field_name = error["loc"][-1]
                error_msg = error["msg"]
                validation_errors[field_name] = [error_msg]

        error_response = {
            "message": ValidationResponseSchema(
                code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                message=[validation_errors],
            ).__dict__
        }

        return JSONResponse(
            content=error_response,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    async def value_exception_handler(self, request: Request, exc):
        """
        THIS VALUE ERROR ONLY WORKS OUTSIDE SCHEMA
        """
        response = {}
        for error in exc.args:
            response.update(error)

        error_response = {
            "message": ValidationResponseSchema(
                code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                message=[response],
            ).__dict__
        }
        return JSONResponse(
            content=error_response,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    async def handle_integrity_error(self, request: Request, exc):
        detail = str(exc.orig.diag.message_detail)
        field_name = detail.split("Key (", 1)[1].split(")", 1)[0]
        return JSONResponse(
            content={
                "message": ResponseSchema(
                    code="400",
                    status="Bad Request",
                    message=f"Duplicate value already exists for field '{field_name}'.",  # noqa
                    data=[],
                ).__dict__
            },
            status_code=400,
        )

    async def internal_server_error_handler(self, request: Request, exc):
        return JSONResponse(
            content={
                "message": ResponseSchema(
                    code="500",
                    status="Internal Server Error",
                    message="error occurred on the server",
                    data=[],
                ).__dict__
            },
            status_code=500,
        )


class ExceptionHandlerRegistration:
    @staticmethod
    def register_all_exceptions(app):
        exceptions = ErpProductAuthException()
        exception_handlers: dict[type, callable] = {
            HTTPException: exceptions.http_exception_handler,
            RequestValidationError: exceptions.validation_exception_handler,  # noqa
            ValueError: exceptions.value_exception_handler,
            IntegrityError: exceptions.handle_integrity_error,
            Exception: exceptions.internal_server_error_handler,
        }

        for exception_type, exception_handler in exception_handlers.items():
            app.add_exception_handler(exception_type, exception_handler)
