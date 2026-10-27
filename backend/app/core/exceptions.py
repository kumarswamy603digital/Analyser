"""Application exceptions and a consistent error-response envelope.

All API errors are returned as:
    {"error": {"code": <machine code>, "message": <safe human message>,
               "details": <optional, never contains stack traces in production>}}
"""
from __future__ import annotations

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


class AppError(HTTPException):
    """Base class for domain errors that map to a stable machine code."""

    code: str = "app_error"
    default_message: str = "Application error."

    def __init__(self, message: str | None = None, status_code: int | None = None,
                 details: dict | None = None) -> None:
        super().__init__(
            status_code=status_code or status.HTTP_400_BAD_REQUEST,
            detail=message or self.default_message,
        )
        self.details = details or {}


class EmptyInputError(AppError):
    code = "empty_input"
    default_message = "Input text must not be empty."


class InputTooLongError(AppError):
    code = "input_too_long"
    default_message = "Input text exceeds the maximum allowed length."


class UnsupportedPairError(AppError):
    code = "unsupported_language_pair"
    default_message = "The requested language pair is not supported."


class InvalidLanguageError(AppError):
    code = "invalid_language_code"
    default_message = "One or more language codes are invalid."


class ModelNotReadyError(AppError):
    code = "model_not_ready"
    default_message = "The required model is not ready."


class InferenceError(AppError):
    code = "inference_failed"
    default_message = "Model inference failed."


def _envelope(code: str, message: str, details: dict | None = None) -> dict:
    return {"error": {"code": code, "message": message, "details": details or {}}}


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def _app_error_handler(_: Request, exc: AppError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=_envelope(exc.code, str(exc.detail), exc.details),
        )

    @app.exception_handler(RequestValidationError)
    async def _validation_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
        # Echo which fields failed, but not their (potentially sensitive) values.
        fields = sorted({
            ".".join(str(p) for p in err.get("loc", [])[1:])
            for err in exc.errors()
        })
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=_envelope(
                "validation_error",
                "Request validation failed.",
                {"invalid_fields": fields},
            ),
        )

    @app.exception_handler(StarletteHTTPException)
    async def _http_handler(_: Request, exc: StarletteHTTPException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=_envelope("http_error", str(exc.detail)),
        )

    @app.exception_handler(Exception)
    async def _unhandled_handler(request: Request, exc: Exception) -> JSONResponse:
        # Never leak internal stack traces to clients. Logged server-side only.
        import logging
        logging.getLogger("app.error").exception(
            "Unhandled error on %s %s", request.method, request.url.path
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=_envelope("internal_error", "Internal server error."),
        )
