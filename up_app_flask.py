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

# Rota para atualizar imagem
@app.route('/update/<int:image_id>', methods=['PUT'])
def update_image(image_id):
    # Verifica se a imagem foi enviada
    if 'image' not in request.files:
        return jsonify({'error': 'No image part'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Conectando ao banco de dados
    conn = get_db_connection()
    cursor = conn.cursor()

    # Ler a nova imagem
    image_data = file.read()
    image_name = file.filename

    # Atualizar a imagem no banco de dados
    cursor.execute(
        "UPDATE image_upload SET image_name = ?, image_data = ? WHERE id = ?",
        (image_name, image_data, image_id)
    )
    conn.commit()

    # Verificar se a imagem foi encontrada e atualizada
    if cursor.rowcount == 0:
        cursor.close()
        conn.close()
        return jsonify({'error': 'Image not found'}), 404

    # Fechar a conexão
    cursor.close()
    conn.close()

    return jsonify({'message': 'File updated successfully', 'image_name': image_name}), 200

# Página inicial para testar
@app.route('/')
def home():
    return "Welcome to the Flask Image Update API!"

if __name__ == '__main__':
    app.run(debug=True)
