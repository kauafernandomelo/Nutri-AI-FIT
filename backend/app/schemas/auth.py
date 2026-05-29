"""Schemas de autenticação (entrada das rotas /auth)."""
from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    # 8..72: mínimo razoável + limite de 72 bytes do bcrypt (validado aqui,
    # então nunca truncamos silenciosamente uma senha no hash).
    password: str = Field(min_length=8, max_length=72)

# O LOGIN usa o formulário OAuth2 padrão (username=email, password) — isso faz o
# botão "Authorize" do Swagger /docs funcionar sem código extra. Ver api/v1/auth.py.
