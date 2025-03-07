from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, Usuario, Post, Comentario
from flasgger import Swagger  # type: ignore
from config import swagger_config, swagger_template  # Importando configurações do Swagger

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

swagger = Swagger(app, config=swagger_config, template=swagger_template)

# --------------------------------------
#  ROTAS DE USUÁRIOS
# --------------------------------------
@app.route('/usuarios', methods=['POST'])
def create_usuario():
    """
    Criar um novo usuário
    ---
    tags:
      - Usuários
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            nome:
              type: string
              example: João Roberto
            email:
              type: string
              example: joao@email.com
    responses:
      201:
        description: Usuário criado com sucesso
      400:
        description: Nome e email são obrigatórios ou email já cadastrado
    """
    data = request.get_json()
    nome = data.get('nome')
    email = data.get('email')

    if not nome or not email:
        return jsonify({'message': 'Nome e email são obrigatórios'}), 400

    # Verifica se o email já existe no banco de dados
    if Usuario.query.filter_by(email=email).first():
        return jsonify({'message': 'Este email já está cadastrado'}), 400

    usuario = Usuario(nome=nome, email=email)
    db.session.add(usuario)
    db.session.commit()
    
    return jsonify({'message': 'Usuário criado', 'id': usuario.id}), 201



@app.route('/usuarios', methods=['GET'])
def get_usuarios():
    """
    Listar todos os usuários
    ---
    tags:
      - Usuários
    responses:
      200:
        description: Retorna uma lista de usuários
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              nome:
                type: string
              email:
                type: string
    """
    usuarios = Usuario.query.all()
    return jsonify([{'id': usuario.id, 'nome': usuario.nome, 'email': usuario.email} for usuario in usuarios])


@app.route('/usuarios/<int:id>', methods=['GET'])
def get_usuario(id):
    """
    Obter detalhes de um usuário pelo ID
    ---
    tags:
      - Usuários
    parameters:
      - name: id
        in: path
        required: true
        type: integer
        example: 1
    responses:
      200:
        description: Retorna os detalhes do usuário
      404:
        description: Usuário não encontrado
    """
    usuario = Usuario.query.get_or_404(id)
    return jsonify({'id': usuario.id, 'nome': usuario.nome, 'email': usuario.email})


@app.route('/usuarios/<int:id>', methods=['PUT'])
def update_usuario(id):
    """
    Atualizar um usuário
    ---
    tags:
      - Usuários
    parameters:
      - name: id
        in: path
        required: true
        type: integer
        example: 1
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            nome:
              type: string
              example: João Roberto
            email:
              type: string
              example: joao@email.com
    responses:
      200:
        description: Usuário atualizado com sucesso
      404:
        description: Usuário não encontrado
    """
    usuario = Usuario.query.get_or_404(id)
    data = request.get_json()

    usuario.nome = data.get('nome', usuario.nome)
    usuario.email = data.get('email', usuario.email)

    db.session.commit()
    return jsonify({'message': 'Usuário atualizado'})


@app.route('/usuarios/<int:id>', methods=['DELETE'])
def delete_usuarios(id):
    """
    Deletar um usuário
    ---
    tags:
      - Usuários
    parameters:
      - name: id
        in: path
        required: true
        type: integer
        example: 1
    responses:
      200:
        description: Usuário deletado com sucesso
      404:
        description: Usuário não encontrado
    """
    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()

    return jsonify({'message': 'Usuário deletado'})



# --------------------------------------
#  ROTAS DE POSTS
# --------------------------------------
@app.route('/posts', methods=['POST'])
def create_post():
    """
    Criar um novo post
    ---
    tags:
      - Posts
    parameters:
      - in: body
        name: body
        description: Dados do post para criação
        required: true
        schema:
          type: object
          properties:
            titulo:
              type: string
              example: 'Título do post'
            conteudo:
              type: string
              example: 'Conteúdo do post'
            usuario_id:
              type: integer
              example: 1
    responses:
      201:
        description: Post criado com sucesso
        schema:
          type: object
          properties:
            message:
              type: string
              example: 'Post criado'
            id:
              type: integer
              example: 1
      400:
        description: Requisição inválida, dados obrigatórios não fornecidos
        schema:
          type: object
          properties:
            message:
              type: string
              example: 'Título, conteúdo e usuário_id são obrigatórios'
    """
    data = request.get_json()
    titulo = data.get('titulo')
    conteudo = data.get('conteudo')
    usuario_id = data.get('usuario_id')

    if not titulo or not conteudo or not usuario_id:
        return jsonify({'message': 'Título, conteúdo e usuário_id são obrigatórios'}), 400
    
    # Verifica se o usuário existe
    usuario = Usuario.query.get(usuario_id)
    if not usuario:
        return jsonify({'message': 'Usuário não encontrado'}), 404

    post = Post(titulo=titulo, conteudo=conteudo, usuario_id=usuario_id)
    db.session.add(post)
    db.session.commit()

    return jsonify({'message': 'Post criado', 'id': post.id}), 201


@app.route('/posts', methods=['GET'])
def get_posts():
    """
    Listar todos os posts
    ---
    tags:
      - Posts
    responses:
      200:
        description: Lista de posts
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 1
              titulo:
                type: string
                example: 'Título do post'
              conteudo:
                type: string
                example: 'Conteúdo do post'
              usuario_id:
                type: integer
                example: 1
      500:
        description: Erro interno do servidor
        schema:
          type: object
          properties:
            message:
              type: string
              example: 'Erro ao listar os posts'
    """
    try:
        posts = Post.query.all()
        return jsonify([{'id': post.id, 'titulo': post.titulo, 'conteudo': post.conteudo, 'usuario_id': post.usuario_id} for post in posts])
    except Exception as e:
        return jsonify({'message': 'Erro ao listar os posts', 'error': str(e)}), 500
    


# --------------------------------------
#  ROTAS DE COMENTÁRIOS
# --------------------------------------
@app.route('/comentarios', methods=['POST'])
def create_comentario():
    """
    Criar um novo comentário
    ---
    tags:
      - Comentários
    parameters:
      - in: body
        name: body
        description: Dados do comentário para criação
        required: true
        schema:
          type: object
          properties:
            conteudo:
              type: string
              example: 'Este é o conteúdo do comentário'
            usuario_id:
              type: integer
              example: 1
            post_id:
              type: integer
              example: 1
    responses:
      201:
        description: Comentário criado com sucesso
        schema:
          type: object
          properties:
            message:
              type: string
              example: 'Comentário criado'
            id:
              type: integer
              example: 1
      400:
        description: Requisição inválida, dados obrigatórios não fornecidos
        schema:
          type: object
          properties:
            message:
              type: string
              example: 'Conteúdo, usuário_id e post_id são obrigatórios'
    """
    data = request.get_json()
    conteudo = data.get('conteudo')
    usuario_id = data.get('usuario_id')
    post_id = data.get('post_id')

    if not conteudo or not usuario_id or not post_id:
        return jsonify({'message': 'Conteúdo, usuário_id e post_id são obrigatórios'}), 400

    # Verifica se o usuário existe
    usuario = Usuario.query.get(usuario_id)
    if not usuario:
        return jsonify({'message': 'Usuário não encontrado'}), 404

    # Verifica se o post existe
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'message': 'Post não encontrado'}), 404
    
    comentario = Comentario(conteudo=conteudo, usuario_id=usuario_id, post_id=post_id)
    db.session.add(comentario)
    db.session.commit()

    return jsonify({'message': 'Comentário criado', 'id': comentario.id}), 201


@app.route('/comentarios', methods=['GET'])
def get_comentarios():
    """
    Listar todos os comentários
    ---
    tags:
      - Comentários
    responses:
      200:
        description: Lista de comentários
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 1
              conteudo:
                type: string
                example: 'Este é o conteúdo do comentário'
              usuario_id:
                type: integer
                example: 1
              post_id:
                type: integer
                example: 1
      500:
        description: Erro interno do servidor
        schema:
          type: object
          properties:
            message:
              type: string
              example: 'Erro ao listar os comentários'
    """
    try:
        comentarios = Comentario.query.all()
        return jsonify([{'id': c.id, 'conteudo': c.conteudo, 'usuario_id': c.usuario_id, 'post_id': c.post_id} for c in comentarios])
    except Exception as e:
        return jsonify({'message': 'Erro ao listar os comentários', 'error': str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=8080, host='0.0.0.0')
