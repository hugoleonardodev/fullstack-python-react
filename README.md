# Fullstack project

É necessário ter docker-compose, node.js, python para executar a aplicação.


## Como executar a aplicação

A aplicação inteira está separada em containers do Docker.

Para executar todos os containeres:

    ```bash
        docker-compose up --build
    ```
Backend está em `0.0.0.0:8000`

- Backend:
    DEVELOPMENT
    ```bash
        cd backend/app
        fastapi dev main.js
    ```
- Frontend: