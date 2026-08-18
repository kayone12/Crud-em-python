async function fazerLogin() {
    const email = document.getElementById('email').value;
    const senha = document.getElementById('senha').value;

    const response = await fetch('/login', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({email, senha})
    });

    const resultado = await response.json();

    if (response.ok) {
        window.location.href = "/dashboard";
    } else {
        alert("Erro no login: " + resultado.erro);
    }
}