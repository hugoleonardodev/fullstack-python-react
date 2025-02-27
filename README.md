# Fullstack project

É necessário ter aws, aws-sam-cli, docker, docker-compose, node.js, python 3 instalados no seu computador para executar a aplicação.


## Como executar a aplicação

A aplicação inteira está separada em containers do Docker.

Para executar todos os containeres:

    ```bash
        docker-compose up --build
    ```

- Frontend está em [http://0.0.0.0:3000/](http://0.0.0.0:3000/)

- Backend está em `http://0.0.0.0:8000/api` e [http://0.0.0.0:8000/docs](http://0.0.0.0:8000/docs)

- Localstack [http://0.0.0.0:4566/](http://0.0.0.0:4566/)

- MongoDB [http://0.0.0.0:27017/](http://0.0.0.0:27017/)

- Lambda será executado separadamente, será demonstrado a seguir com as outras features

## Requisitos

Desafio Full Stack
Objetivo Geral​
Desenvolver uma aplicação full stack que integre FastAPI, MongoDB, ReactJS e AWS (com
LocalStack para S3). Use Python no backend, Serverless Framework (para funções Lambda)
e Docker para containerização.

1. Backend (FastAPI + MongoDB)
1.1. Entidades
[X] - As entidades permanecem as mesmas, mas use modelos Pydantic para validação:
[X] 1.1.1. Product - id (string ou ObjectId) - name (string) - description (string) - price (number) - category_ids (lista de IDs) (relação many-to-many com Category) - image_url (string) – URL da imagem no S3
[X] 1.1.2. Category - id (string ou ObjectId) - name (string)
[X] 1.1.3. Order- id (string ou ObjectId) - date (Date) - product_ids (lista de IDs de Product) - total (number)

Observação: O relacionamento entre Product e Category é many-to-many, permitindo que cada Product pertença a várias Categories e vice-versa.

1.2. Endpoints
1.2.1. CRUD para cada entidade:
[ ] - ​Product: criar, listar, atualizar, deletar.
[ ] - ​Category: criar, listar, atualizar, deletar.
[ ] - ​Order: criar, listar, atualizar, deletar.
  
[ ] 1.2.2. Dashboard: Exibir dados agregados de vendas com filtros por categoria, produto e período (implemente queries agregadas no MongoDB para métricas como total de pedidos, valor médio, etc.).

1.2.3. Relacionamentos: 
[ ] - Associar Products a Categories (many-to-many).

[ ] - Associar Products a Orders.
  
1.2.4. Validações:
[ ] - ​Utilize Pydantic para garantir a integridade dos dados.
[ ] - ​Trate deleções com cuidado (ex.: ao deletar uma Category, evite deixar Products com IDs inexistentes).
[ ] - Garanta um tratamento de erros adequado com status HTTP e respostas em JSON.

1.3. Script de Massa de Dados
1.3.1. Crie um script em Python (por exemplo, utilizando Typer ou argparse) para popular o MongoDB com dados fictícios:
[ ] - ​Products: Variações de preço e categorias.
[ ] - ​Categories: Diferentes tipos.
[ ] - ​Orders: Combinações variadas de products, datas e totais.
  
2. Tarefa Assíncrona (Serverless Framework)
2.1. Função Lambda
2.1.1. Desenvolva uma função Lambda usando o Serverless Framework em Python para tarefas em segundo plano, como:
[ ] - ​Processar relatórios de vendas (baseado nos Orders);
[ ] - Enviar notificações quando um novo Order for criado;
[ ] - Ou qualquer outra funcionalidade relevante.

2.2. Integração
[ ] 2.2.1. Explique como a Lambda pode ser acionada (ex.: via evento, cron ou chamada HTTP).
[ ] 2.2.2. Demonstre, se aplicável, a integração com o backend FastAPI ou a leitura de dados do MongoDB.

3. Front-end (React + Material UI + Storybook)
3.1. Páginas Principais
[ ] - Products: Listagem, criação, edição e deleção. Incluir upload de imagem (armazenada no S3).
[ ] - ​Categories: Listagem, criação, edição e deleção.
[ ] - ​Orders: Listagem, criação, edição e deleção.
3.2. Dashboard de KPIs
Exiba métricas dos Orders, como:
[ ] - ​Quantidade total de pedidos
[ ] - ​Valor médio por pedido
[ ] - Receita total
[ ] - ​Pedidos por período (diário, semanal, mensal, etc.)
3.3. Documentação de Componentes
3.3.1. Utilize o Storybook para documentar pelo menos 2 componentes principais, como:
[ ] - ​Uma tabela para listagem.
[ ] - ​Um formulário para criação/edição.

4. Integração com AWS (LocalStack para S3)
4.1. Configuração Local
[ ] - ​Use LocalStack para simular o S3 em ambiente local.
[ ] - ​Garanta o upload de imagens dos Products para um bucket S3 simulado.
[ ] - ​Configure o Docker (via docker-compose ou similar) para subir o LocalStack, o backend FastAPI e o front-end React.
4.2. Acesso ao S3
[ ] - Certifique-se de que a aplicação consiga enviar arquivos para o bucket e recuperar a URL da imagem, exibindo-a no front-end.

5. Entrega
5.1. Repositório
[ ] - ​Disponibilize um repositório GitHub com todo o código-fonte.
[ ] - ​Inclua um README.md com instruções de setup e execução.
[ ] - Envie o link do repositório em resposta a esse e-mail.
5.2. Scripts e Configurações
[ ] - Docker/docker-compose: Para facilitar o setup de todos os serviços.
[ ] - ​Script de Massa de Dados: Implementado em Python.
[ ] - ​Arquivo serverless.yml: Para configurar a Lambda.
[ ] - ​Storybook: Configurado e funcional.
5.3. Demonstração
[ ] - (Opcional) Inclua screenshots ou breves instruções que validem