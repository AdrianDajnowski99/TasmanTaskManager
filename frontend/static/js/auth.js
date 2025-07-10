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
const usernameInput = document.getElementById('username');
if (usernameInput) {
    usernameInput.addEventListener('input', function() {
        this.value = this.value.replace(/\s/g, '');
    });
}
document.getElementById('username').addEventListener('input', function() {
    const username = this.value;
    const checkSpan = document.getElementById('username-check');
    if (username.length < 3) {
        checkSpan.textContent = '';
        return;
    }
    fetch(`/api/check_username?username=${encodeURIComponent(username)}`)
        .then(res => res.json())
        .then(data => {
            if (data.exists) {
                checkSpan.textContent = 'Username already exists!';
            } else {
                checkSpan.textContent = '';
            }
        });
});