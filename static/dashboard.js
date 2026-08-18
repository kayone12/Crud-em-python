const API_URL = 'http://127.0.0.1:5000';

// Desenha as linhas da tabela a partir de uma lista de usuários
function renderizarUsuarios(usuarios) {
    const tbody = document.getElementById('tabela-usuarios');
    tbody.innerHTML = '';

    if (usuarios.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" style="text-align:center;">Nenhum usuário encontrado.</td></tr>';
        return;
    }

    usuarios.forEach(u => {
        tbody.innerHTML += `
            <tr>
                <td>${u.id}</td>
                <td>${u.nome}</td>
                <td>${u.email}</td>
                <td>${u.cpf}</td>
                <td>${u.telefone || '-'}</td>
                <td>${u.data_nascimento}</td>
                <td>
                    <button class="btn-editar" onclick="prepararEdicao(${u.id}, '${u.nome}', '${u.email}', '${u.telefone}')">Editar</button>
                    <button class="btn-excluir" onclick="deletarUsuario(${u.id})">Excluir</button>
                </td>
            </tr>
        `;
    });
}

async function carregarUsuarios() {
    const res = await fetch(`${API_URL}/usuarios`);
    const usuarios = await res.json();
    renderizarUsuarios(usuarios);
}

// Busca um único usuário pelo ID (usa a rota GET /usuarios/<id>) e mostra só ele na tabela
async function buscarPorId() {
    const id = document.getElementById('busca-id').value;

    if (!id) {
        alert("Digite um ID para buscar.");
        return;
    }

    const res = await fetch(`${API_URL}/usuarios/${id}`);

    if (res.ok) {
        const usuario = await res.json();
        renderizarUsuarios([usuario]);
    } else {
        const erro = await res.json();
        renderizarUsuarios([]);
        alert(erro.erro || "Usuário não encontrado.");
    }
}

// Limpa o campo de busca e volta a listar todos os usuários
function limparBusca() {
    document.getElementById('busca-id').value = '';
    carregarUsuarios();
}

async function salvarUsuario() {
    const id = document.getElementById('usuario-id').value;
    const dados = {
        nome: document.getElementById('nome').value,
        email: document.getElementById('email').value,
        cpf: document.getElementById('cpf').value,
        telefone: document.getElementById('telefone').value,
        data_nascimento: document.getElementById('data_nascimento').value,
        senha: document.getElementById('senha').value
    };

    if (id) {
        const res = await fetch(`${API_URL}/usuarios/${id}`, {
            method: 'PUT',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(dados)
        });
        if (res.ok) {
            alert("Atualizado com sucesso!");
            limparFormulario();
            carregarUsuarios();
        }
    } else {
        const res = await fetch(`${API_URL}/usuarios`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(dados)
        });
        if (res.ok) {
            alert("Cadastrado com sucesso!");
            limparFormulario();
            carregarUsuarios();
        } else {
            const erro = await res.json();
            alert("Erro: " + erro.erro);
        }
    }
}

function prepararEdicao(id, nome, email, telefone) {
    document.getElementById('usuario-id').value = id;
    document.getElementById('nome').value = nome;
    document.getElementById('email').value = email;
    document.getElementById('telefone').value = telefone;
    document.getElementById('titulo-form').innerText = "Editar Usuário (ID: " + id + ")";
    document.getElementById('btn-salvar-texto').innerText = "Atualizar Usuário";
}

function limparFormulario() {
    document.getElementById('usuario-id').value = '';
    document.getElementById('nome').value = '';
    document.getElementById('email').value = '';
    document.getElementById('cpf').value = '';
    document.getElementById('telefone').value = '';
    document.getElementById('data_nascimento').value = '';
    document.getElementById('senha').value = '';
    document.getElementById('titulo-form').innerText = "Cadastrar Novo Usuário";
    document.getElementById('btn-salvar-texto').innerText = "Salvar Usuário";
}

async function deletarUsuario(id) {
    if (confirm("Tem certeza que deseja excluir?")) {
        const res = await fetch(`${API_URL}/usuarios/${id}`, { method: 'DELETE' });
        if (res.ok) {
            alert("Excluído com sucesso!");
            carregarUsuarios();
        }
    }
}

carregarUsuarios();