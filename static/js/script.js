function mostrarSenha() {
    const senha = document.getElementById("senha");
    const img = document.getElementById("toggleSenha");

    if (senha.type === "password") {
        senha.type = "text";
        img.src = "/static/img/olho-aberto.png";
    } else {
        senha.type = "password";
        img.src = "/static/img/olho-fechado.png";
    }
}
