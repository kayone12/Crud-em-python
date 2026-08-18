from flask import Flask, jsonify, request, render_template
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2

app = Flask(__name__)

def conectar():
    return psycopg2.connect(
        dbname="sistema_usuarios",
        user="postgres",
        password="K@yone123",
        host="localhost",
        port="5432"
    )

# Rotas de Páginas
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/registro')
def registro():
    return render_template('registro.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# Rotas da API (CRUD)

# Lista todos os usuários ativos (soft delete = exclusão lógica)
@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, nome, email, cpf, telefone, data_nascimento FROM usuarios WHERE ativo = TRUE")
    dados = cursor.fetchall()
    cursor.close()
    conexao.close()
    
    usuarios = []
    for u in dados:
        usuarios.append({
            "id": u[0], "nome": u[1], "email": u[2], 
            "cpf": u[3], "telefone": u[4], "data_nascimento": str(u[5])
        })
    return jsonify(usuarios)

# Consulta um único usuário pelo ID (usado, por exemplo, para pré-carregar o formulário de edição)
@app.route('/usuarios/<int:id_usuario>', methods=['GET'])
def buscar_usuario(id_usuario):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "SELECT id, nome, email, cpf, telefone, data_nascimento FROM usuarios WHERE id = %s AND ativo = TRUE",
        (id_usuario,)
    )
    u = cursor.fetchone()
    cursor.close()
    conexao.close()

    if not u:
        return jsonify({"erro": "Usuário não encontrado"}), 404

    usuario = {
        "id": u[0], "nome": u[1], "email": u[2],
        "cpf": u[3], "telefone": u[4], "data_nascimento": str(u[5])
    }
    return jsonify(usuario)

# Cadastra um novo usuário, validando campos obrigatórios e criptografando a senha
@app.route('/usuarios', methods=['POST'])
def criar_usuario():
    dados = request.json or {}

    # Validação das regras de negócio: campos obrigatórios não podem estar vazios
    campos_obrigatorios = ['nome', 'email', 'cpf', 'data_nascimento', 'senha']
    faltando = [campo for campo in campos_obrigatorios if not dados.get(campo)]
    if faltando:
        return jsonify({"erro": f"Campos obrigatórios não preenchidos: {', '.join(faltando)}"}), 400

    senha_criptografada = generate_password_hash(dados.get('senha'))

    conexao = conectar()
    cursor = conexao.cursor()
    sql = """
        INSERT INTO usuarios (nome, email, cpf, telefone, data_nascimento, senha) 
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    try:
        cursor.execute(sql, (
            dados.get('nome'), dados.get('email'), dados.get('cpf'), 
            dados.get('telefone'), dados.get('data_nascimento'), senha_criptografada
        ))
        conexao.commit()
    except psycopg2.errors.UniqueViolation:
        # E-mail ou CPF já cadastrado (restrição UNIQUE do banco)
        conexao.rollback()
        return jsonify({"erro": "E-mail ou CPF já cadastrado"}), 409
    except Exception as e:
        conexao.rollback()
        return jsonify({"erro": str(e)}), 400
    finally:
        cursor.close()
        conexao.close()
    return jsonify({"mensagem": "Usuário cadastrado com sucesso!"}), 201

# Atualiza os dados de um usuário existente
@app.route('/usuarios/<int:id_usuario>', methods=['PUT'])
def atualizar_usuario(id_usuario):
    dados = request.json or {}

    if not dados.get('nome') or not dados.get('email'):
        return jsonify({"erro": "Nome e e-mail são obrigatórios"}), 400

    conexao = conectar()
    cursor = conexao.cursor()
    sql = "UPDATE usuarios SET nome = %s, email = %s, telefone = %s WHERE id = %s AND ativo = TRUE"
    try:
        cursor.execute(sql, (dados.get('nome'), dados.get('email'), dados.get('telefone'), id_usuario))
        if cursor.rowcount == 0:
            # Nenhuma linha afetada = usuário não existe ou já está inativo
            conexao.rollback()
            return jsonify({"erro": "Usuário não encontrado"}), 404
        conexao.commit()
    except psycopg2.errors.UniqueViolation:
        conexao.rollback()
        return jsonify({"erro": "E-mail já cadastrado para outro usuário"}), 409
    except Exception as e:
        conexao.rollback()
        return jsonify({"erro": str(e)}), 400
    finally:
        cursor.close()
        conexao.close()
    return jsonify({"mensagem": f"Usuário {id_usuario} atualizado com sucesso!"})

# Exclusão lógica (soft delete): mantém o registro no banco, apenas marca como inativo
@app.route('/usuarios/<int:id_usuario>', methods=['DELETE'])
def deletar_usuario(id_usuario):
    conexao = conectar()
    cursor = conexao.cursor()
    sql = "UPDATE usuarios SET ativo = FALSE, data_exclusao = CURRENT_TIMESTAMP WHERE id = %s AND ativo = TRUE"
    cursor.execute(sql, (id_usuario,))
    if cursor.rowcount == 0:
        conexao.rollback()
        cursor.close()
        conexao.close()
        return jsonify({"erro": "Usuário não encontrado"}), 404
    conexao.commit()
    cursor.close()
    conexao.close()
    return jsonify({"mensagem": f"Usuário {id_usuario} excluído com sucesso!"})

# Autentica um usuário comparando a senha informada com o hash salvo no banco
@app.route('/login', methods=['POST'])
def login():
    dados = request.json or {}
    email = dados.get('email')
    senha = dados.get('senha')

    if not email or not senha:
        return jsonify({"erro": "E-mail e senha são obrigatórios"}), 400

    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, nome, senha FROM usuarios WHERE email = %s AND ativo = TRUE", (email,))
    u = cursor.fetchone()
    cursor.close()
    conexao.close()

    if u and u[2] and check_password_hash(u[2], senha):
        return jsonify({"mensagem": "Login realizado com sucesso!"}), 200
    else:
        return jsonify({"erro": "E-mail ou senha inválidos"}), 401

if __name__ == '__main__':
    app.run(debug=True)