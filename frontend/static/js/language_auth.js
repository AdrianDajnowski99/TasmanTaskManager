const translations = {
    en: {
        "task-manager": "TASMAN Task Manager",
        "login": "Login",
        "register": "Register",
        "logout": "Log Out",
        "username": "Username",
        "password": "Password",
        "confirm-password": "Confirm password",
        "login-title": "Login",
        "login-header": "Login to existing account to start using TASMAN Task Manager",
        "register-title": "Register",
        "register-header": "Register new account to start using TASMAN Task Manager",
        "username-exists": "Username already exists!",
        "username-available": "Username available",
        "username-no-spaces": "Username (cannot contain spaces):",
        "password-min": "Password (8 characters minimum):",
        "confirm-password-label": "Confirm password:",
        "already-have-account": "Already have an account? Login!",
        "dont-have-account": "Don't have an account? Create one!",
        "sign-in": "SIGN IN",
        "log-in": "LOG IN",
        "welcome": "Welcome!",
        "home-header": "Register to create new account or login to existing account to start using TASMAN Task Manager",
        "access_denied": "Access Denied!",
        "no_permission": "We're sorry, but you do not have permission to use the application.",
        "denied_info": "Please create an account, log in to an existing account, or contact the administrator!",
        "all-rights-reserved": "TASMAN Task Manager. All rights reserved."
    },
    pl: {
        "task-manager": "TASMAN Task Manager",
        "login": "Zaloguj się",
        "register": "Zarejestruj się",
        "logout": "Wyloguj się",
        "username": "Nazwa użytkownika",
        "password": "Hasło",
        "confirm-password": "Potwierdź hasło",
        "login-title": "Logowanie",
        "login-header": "Zaloguj się, aby korzystać z TASMAN Task Manager",
        "register-title": "Rejestracja",
        "register-header": "Zarejestruj nowe konto, aby korzystać z TASMAN Task Manager",
        "username-exists": "Nazwa użytkownika już istnieje!",
        "username-available": "Nazwa użytkownika dostępna",
        "username-no-spaces": "Nazwa użytkownika (bez spacji):",
        "password-min": "Hasło (minimum 8 znaków):",
        "confirm-password-label": "Potwierdź hasło:",
        "already-have-account": "Masz już konto? Zaloguj się!",
        "dont-have-account": "Nie masz konta? Utwórz je!",
        "sign-in": "ZAREJESTRUJ",
        "log-in": "ZALOGUJ",
        "welcome": "Witaj!",
        "home-header": "Zarejestruj się lub zaloguj, aby korzystać z TASMAN Task Manager",
        "access_denied": "Brak dostępu!",
        "no_permission": "Przepraszamy, nie masz uprawnień do korzystania z aplikacji.",
        "denied_info": "Załóż konto, zaloguj się lub skontaktuj się z administratorem!",
        "all-rights-reserved": "TASMAN Task Manager. Wszystkie prawa zastrzeżone."
    }
};

let currentLanguage = 'pl';

function switchLanguage() {
    currentLanguage = currentLanguage === 'pl' ? 'en' : 'pl';
    applyTranslations();
}

function applyTranslations() {
    document.querySelectorAll('[data-lang]').forEach(element => {
        const key = element.getAttribute('data-lang');
        if (translations[currentLanguage][key]) {
            element.textContent = translations[currentLanguage][key];
        }
    });

    // Update overlay content
    document.getElementById('overlay-title').textContent = translations[currentLanguage]['help-title'];
    document.getElementById('overlay-description').textContent = translations[currentLanguage]['help-description'];
}

// Initial translation application
applyTranslations();