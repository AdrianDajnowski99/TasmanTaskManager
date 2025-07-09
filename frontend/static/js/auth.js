const loginBtn = document.getElementById("Login");
const registerBtn = document.getElementById("Register");

if (loginBtn) {
    loginBtn.addEventListener("click", () => {
        const loginUrl = loginBtn.getAttribute("data-url");
        window.location.href = loginUrl;
    });
}

if (registerBtn) {
    registerBtn.addEventListener("click", () => {
        const registerUrl = registerBtn.getAttribute("data-url");
        window.location.href = registerUrl;
    });
}

const logoutBtn = document.getElementById('logout');
if (logoutBtn) {
    logoutBtn.addEventListener('click', () => {
        console.log('Logout clicked');
        window.location.href = '/logout';
    });
}