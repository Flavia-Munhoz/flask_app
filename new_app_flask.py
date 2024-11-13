from flask import Flask, request, jsonify
import os
import mariadb

app = Flask(__name__)

# Configurações do banco de dados MariaDB
db_config = {
    'host': 'localhost',
    'user': 'root',         # Usuário do banco de dados
    'password': '',         # Senha do banco de dados
    'database': 'image_upload'
}

# Conectar ao banco de dados MariaDB
def get_db_connection():
    conn = mariadb.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database']
    )
    return conn

# Rota para upload de imagem
@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image part'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Conectando ao banco de dados
    conn = get_db_connection()
    cursor = conn.cursor()

    # Ler a imagem e salvar no banco de dados
    image_data = file.read()
    image_name = file.filename

    # Inserir a imagem no banco de dados
    cursor.execute(
        "INSERT INTO images (image_name, image_data) VALUES (?, ?)",
        (image_name, image_data)
    )
    conn.commit()

    # Fechar a conexão
    cursor.close()
    conn.close()

    return jsonify({'message': 'File uploaded successfully', 'image_name': image_name}), 200

# Página inicial para testar
@app.route('/')
def home():
    return "Welcome to the Flask Image Upload API!"

if __name__ == '__main__':
    app.run(debug=True)
