# Sistema de Cadastro de Usuários (CRUD)

Aplicação web para gerenciamento de usuários (Cadastrar, Consultar, Atualizar e Excluir), desenvolvida como atividade prática integrando Front-end, Back-end e Banco de Dados.

## 📋 Sobre o projeto

O sistema permite realizar login e gerenciar usuários através de um painel com formulário de cadastro/edição e uma tabela de listagem, com exclusão lógica (soft delete) dos registros.

## 🛠️ Tecnologias utilizadas

**Front-end**
- HTML5
- CSS3
- JavaScript puro (Fetch API para consumo da API REST)

**Back-end**
- Python 3
- Flask (framework web e criação da API REST)
- Werkzeug Security (hash de senhas)

**Banco de Dados**
- PostgreSQL

## 📁 Estrutura da aplicação

O Flask exige uma organização específica de pastas para servir HTML (`templates/`) e arquivos estáticos como CSS/JS (`static/`). Organize o projeto assim:

```
projeto-crud/
│
├── main.py                # Back-end: rotas de página + API REST + conexão com o banco
├── banco.sql               # Script de criação do banco de dados e da tabela
├── requirements.txt         # Dependências Python do projeto
├── README.md
│
├── static/
│   ├── style.css            # Estilos da aplicação
│   ├── login.js             # Lógica da tela de login
│   ├── registro.js          # Lógica da tela pública de cadastro
│   └── dashboard.js         # Lógica do CRUD (listar, salvar, editar, excluir)
│
└── templates/
    ├── index.html            # Tela de login
    ├── registro.html         # Tela pública de criação de conta
    └── dashboard.html         # Tela de listagem e cadastro/edição de usuários (requer login)
```

> ⚠️ Se os arquivos `index.html` e `dashboard.html` não estiverem dentro de `templates/`, e `style.css`, `login.js`, `dashboard.js` não estiverem dentro de `static/`, o Flask não vai encontrá-los e a aplicação vai quebrar (erro 404 ou `TemplateNotFound`).

## ✅ Pré-requisitos

Antes de começar, instale na máquina:

1. **Python 3.10+** → [python.org/downloads](https://www.python.org/downloads/)
   - No Windows, marque a opção **"Add Python to PATH"** durante a instalação.
2. **PostgreSQL** → [postgresql.org/download](https://www.postgresql.org/download/)
   - Anote o usuário e a senha configurados durante a instalação (por padrão, o usuário é `postgres`).
3. **Git** (opcional, para clonar o repositório) → [git-scm.com](https://git-scm.com/)

Para verificar se estão instalados, abra o terminal e rode:

```bash
python --version
psql --version
git --version
```

## 🚀 Como executar o projeto

### 1. Clonar (ou baixar) o repositório

```bash
git clone <URL_DO_REPOSITORIO>
cd projeto-crud
```

### 2. Criar e ativar um ambiente virtual (recomendado)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

Quando o ambiente virtual estiver ativo, você verá `(venv)` no início da linha do terminal.

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Criar o banco de dados

Abra o terminal do PostgreSQL (`psql`) ou uma ferramenta como o **pgAdmin** e execute o script `banco.sql`.

**Opção A — via terminal (psql):**
```bash
psql -U postgres
```
Dentro do console do psql, execute:
```sql
\i caminho/completo/para/banco.sql
```

**Opção B — via pgAdmin:**
Abra o pgAdmin, conecte-se ao servidor, abra o Query Tool e cole/execute o conteúdo do arquivo `banco.sql`.

Isso vai criar o banco `sistema_usuarios` e a tabela `usuarios`.

### 5. Configurar a conexão com o banco

No arquivo `main.py`, ajuste os dados de conexão para os da sua máquina, na função `conectar()`:

```python
def conectar():
    return psycopg2.connect(
        dbname="sistema_usuarios",
        user="postgres",
        password="SUA_SENHA_AQUI",
        host="localhost",
        port="5432"
    )
```

> 🔒 **Recomendação de boas práticas:** evite deixar a senha do banco escrita diretamente no código-fonte (hardcoded). O ideal é usar variáveis de ambiente (biblioteca `python-dotenv`) para manter esses dados fora do repositório Git.

### 6. Rodar a aplicação

Com o ambiente virtual ativado e o banco configurado, execute:

```bash
python main.py
```

Se tudo estiver certo, o terminal vai mostrar algo como:

```
* Running on http://127.0.0.1:5000
```

### 7. Acessar no navegador

Abra o navegador e acesse:

```
http://127.0.0.1:5000
```

Você verá a tela de login. Como ainda não existe nenhum usuário cadastrado, clique em **"Não tem conta? Cadastre-se"** para acessar a tela pública de registro (`/registro`) e criar o primeiro usuário. A senha já é salva no banco com hash (criptografada) automaticamente, então não é necessário (nem recomendado) inserir usuários diretamente pelo banco de dados.

## 🔌 Endpoints da API

| Método | Rota                | Descrição                          |
|--------|----------------------|--------------------------------------|
| GET    | `/usuarios`           | Lista todos os usuários ativos       |
| GET    | `/usuarios/<id>`        | Consulta um usuário específico pelo ID |
| POST   | `/usuarios`            | Cadastra um novo usuário (senha já salva com hash) |
| PUT    | `/usuarios/<id>`        | Atualiza os dados de um usuário      |
| DELETE | `/usuarios/<id>`        | Exclui (logicamente) um usuário      |
| POST   | `/login`               | Autentica um usuário                |

**Páginas:** `/` (login), `/registro` (criar conta), `/dashboard` (gerenciar usuários, requer estar logado apenas por navegação — não há sessão/token implementados).

## 🗃️ Modelo de dados

Tabela `usuarios`:

| Campo             | Tipo         | Restrições                    |
|-------------------|--------------|--------------------------------|
| id                 | SERIAL        | Chave primária                 |
| nome               | VARCHAR(100)   | NOT NULL                       |
| email              | VARCHAR(100)   | UNIQUE, NOT NULL                |
| cpf                | VARCHAR(11)    | UNIQUE, NOT NULL                |
| telefone           | VARCHAR(20)    | -                               |
| data_nascimento    | DATE           | NOT NULL                       |
| senha              | VARCHAR(255)    | Armazenada com hash (Werkzeug)  |
| ativo              | BOOLEAN         | Default TRUE (controla exclusão lógica) |
| data_exclusao      | TIMESTAMP        | Preenchido ao excluir o usuário |
| data_cadastro      | TIMESTAMP        | Default CURRENT_TIMESTAMP        |

## ⚠️ Limitações conhecidas

- O login apenas **valida** e-mail/senha, mas não cria sessão nem token: qualquer pessoa que digite `/dashboard` na URL consegue acessar a tela sem estar logada. Para um projeto de produção, seria necessário implementar sessões (Flask `session`) ou autenticação via JWT.
- Não há validação de formato de CPF/e-mail no back-end além das restrições do banco (`UNIQUE`, `NOT NULL`).

## 🧯 Problemas comuns

- **`ModuleNotFoundError: No module named 'flask'`** → o ambiente virtual não está ativado, ou as dependências não foram instaladas. Rode novamente `pip install -r requirements.txt`.
- **`psycopg2.OperationalError: could not connect to server`** → verifique se o serviço do PostgreSQL está rodando e se usuário/senha/porta no `main.py` estão corretos.
- **`TemplateNotFound`** → confira se os `.html` estão dentro da pasta `templates/`.
- **Página carrega sem estilo/sem funcionar os botões** → confira se `style.css`, `login.js` e `dashboard.js` estão dentro da pasta `static/`.

## 👤 Autor
Kayone Silva do Nasicento

Atividade prática individual — Desenvolvimento de um CRUD de Usuários (Front-end, Back-end e Banco de Dados).
