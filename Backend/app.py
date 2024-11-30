from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Modelo de usuário
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

# Criação do banco de dados
with app.app_context():
    db.create_all()

# Rota para cadastro de usuários
@app.route('/register', methods=['POST'])
def register():
    # Obter os dados enviados pelo cliente
    data = request.get_json()

    # Validar campos obrigatórios
    if not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Todos os campos (username, email, password) são obrigatórios.'}), 400

    # Verificar se o usuário já existe
    existing_user = User.query.filter((User.username == data['username']) | (User.email == data['email'])).first()
    if existing_user:
        return jsonify({'error': 'Usuário ou e-mail já estão registrados.'}), 400

    # Hash da senha
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    # Criar um novo usuário
    new_user = User(username=data['username'], email=data['email'], password=hashed_password)

    # Salvar no banco de dados
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Usuário registrado com sucesso!'}), 201

if __name__ == '__main__':
    app.run(debug=True)
