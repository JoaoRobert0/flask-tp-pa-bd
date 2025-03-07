from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    # Relacionamento com Post e Comentario
    posts = db.relationship('Post', backref='autor', lazy=True, cascade="all, delete-orphan")  # Um usuário pode ter vários posts
    comentarios = db.relationship('Comentario', backref='autor', lazy=True, cascade="all, delete-orphan")  # Um usuário pode ter vários comentários

    def __str__(self):
        return f"{self.id} - {self.nome}"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    conteudo = db.Column(db.Text, nullable=False)

    # Relacionamento com Usuario e Comentario
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)  # Um post pertence a um usuário
    comentarios = db.relationship('Comentario', backref='post', lazy=True, cascade="all, delete-orphan")  # Um post pode ter vários comentários

    def __str__(self):
        return f"{self.id} - {self.titulo}"


class Comentario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conteudo = db.Column(db.Text, nullable=False)

    # Relacionamento com Usuario e Post
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)  # Um comentário pertence a um usuário
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)  # Um comentário pertence a um post

    def __str__(self):
        return f"Comentario {self.id} - {self.conteudo[:30]}..."

