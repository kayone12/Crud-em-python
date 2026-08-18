async function cadastrar() {
    const nome = document.getElementById('nome').value.trim();
    const email = document.getElementById('email').value.trim();
    const cpf = document.getElementById('cpf').value.trim();
    const telefone = document.getElementById('telefone').value.trim();
    const data_nascimento = document.getElementById('data_nascimento').value;
    const senha = document.getElementById('senha').value;

    if (!nome || !email || !cpf || !data_nascimento || !senha) {
        alert("Preencha todos os campos obrigatórios.");
        return;
    }

    const dados = { nome, email, cpf, telefone, data_nascimento, senha };

    const res = await fetch('/usuarios', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(dados)
    });

    if (res.ok) {
        alert("Conta criada com sucesso! Faça login para continuar.");
        window.location.href = "/";
    } else {
        const erro = await res.json();
        alert("Erro ao cadastrar: " + erro.erro);
    }
}
