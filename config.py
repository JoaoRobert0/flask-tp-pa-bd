swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/api/docs/apispec_1.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/api/docs"  # Rota para documentação do Swagger
}

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "API de Usuários, Posts e Comentários",
        "description": "API para gerenciar usuários, posts e comentários com documentação Swagger",
        "version": "1.0.0"
    },
    "host": "localhost:8080",
    "basePath": "/",
    "schemes": [
        "http"
    ],
    "definitions": {
        "Usuario": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "nome": {"type": "string"},
                "email": {"type": "string"}
            }
        },
        "Post": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "titulo": {"type": "string"},
                "conteudo": {"type": "string"},
                "usuario_id": {"type": "integer"}
            }
        },
        "Comentario": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "conteudo": {"type": "string"},
                "usuario_id": {"type": "integer"},
                "post_id": {"type": "integer"}
            }
        }
    }
}
