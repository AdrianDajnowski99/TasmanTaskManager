//
const loginBtn = document.getElementById("Login");
const registerBtn = document.getElementById("Register");

//
loginBtn.addEventListener("click", () => {
    const loginUrl = loginBtn.getAttribute("data-url");
    window.location.href = loginUrl;
});

registerBtn.addEventListener("click", () => {
    const registerUrl = registerBtn.getAttribute("data-url");
    window.location.href = registerUrl;
});