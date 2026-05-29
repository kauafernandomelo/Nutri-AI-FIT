"""
Rate limiting com slowapi.

POR QUE: limitar requisições por IP protege contra abuso e força bruta —
especialmente importante nas rotas de autenticação (/auth/login, /auth/register).
A chave de limite é o IP de origem (get_remote_address).
"""
from slowapi import Limiter
from slowapi.util import get_remote_address

# Limite padrão generoso para a API; rotas sensíveis aplicam limites mais rígidos
# via o decorator @limiter.limit("...") nos próprios endpoints.
limiter = Limiter(key_func=get_remote_address, default_limits=["200/minute"])
