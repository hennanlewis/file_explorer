# 🔒 Segurança

## Funcionalidades de Segurança Implementadas

### Autenticação
- Hash SHA-256 para senhas
- Rate limiting de tentativas de login
- Timeout automático de sessão
- Proteção contra brute force

### Rede
- Detecção automática de IPs locais
- Diferenciamento entre acesso local e remoto
- Logs detalhados de acesso

### Sessão
- Chaves secretas geradas automaticamente
- Renovação de sessão a cada requisição
- Limpeza automática de sessões expiradas

## Configuração
- `SESSION_TIMEOUT`: 3600 segundos
- `MAX_LOGIN_ATTEMPTS`: 5 tentativas
- `SECRET_KEY`: Gerada via `secrets.token_hex(32)`