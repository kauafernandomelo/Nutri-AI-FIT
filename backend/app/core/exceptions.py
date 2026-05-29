"""
Exceções de domínio.

POR QUE: os serviços levantam estas exceções (que NÃO conhecem o FastAPI). A
camada de API traduz cada uma para um status HTTP (handler em main.py). Assim a
regra de negócio fica desacoplada do framework web.
"""


class AppError(Exception):
    status_code: int = 400

    def __init__(self, detail: str) -> None:
        self.detail = detail
        super().__init__(detail)


class BadRequestError(AppError):
    status_code = 400


class UnauthorizedError(AppError):
    status_code = 401


class ForbiddenError(AppError):
    status_code = 403


class NotFoundError(AppError):
    status_code = 404


class ConflictError(AppError):
    status_code = 409


class ServiceUnavailableError(AppError):
    status_code = 503
