const translations = {
    en: {
        "task-manager": "TASMAN Task Manager",
        "sort-by": "Sort by:",
        "id": "ID",
        "title": "Task Title",
        "status": "Task Status",
        "order": "Order:",
        "ascending": "Ascending",
        "descending": "Descending",
        "sort": "Sort",
        "help": "Help",
        "operation": "Operation",
        "choose-operation": "Choose the operation",
        "add": "Add new task",
        "edit-task": "Edit task",  
        "task-id": "Task ID",  
        "edit": "Edit",    
        "update": "Update task status",
        "delete": "Delete task",
        "show-help": "Show help",
        "select-operation": "Select operation",
        "add-task": "Add Task",
        "task-name": "Task Name:",
        "description": "Description:",
        "status": "Status:",
        "to-do": "To Do",
        "in-progress": "In Progress",
        "done": "Done",
        "ND": "ND",
        "update-task": "Update Task Status",
        "new-status": "New Status:",
        "delete-task": "Delete Task",
        "help-title": "HELP",
        "help-description": "Welcome to the Task Manager application. To add a new task, select the 'Add new task' operation and fill out the form. To edit a existing task, select the 'Edit task' operation. To update a task, select the 'Update task' operation and fill out the form. To delete a task, select the 'Delete task' operation and fill out the form. To sort tasks, select the appropriate options from the dropdown lists. Good luck!",
        "error-title": "POSSIBLE ERROR CODES:",
        "error-301": "Error 301 - Value Error",
        "error-302": "Error 302 - File Not Found Error",
        "error-303": "Error 303 - Operational Error",
        "error-304": "Error 304 - Database Error",
        "error-305": "Error 305 - Integrity Error",
        "error-306": "Error 306 - Syntax or Invalid Operation Error",
        "error-307": "Error 307 - Data Error",
        "error-308": "Error 308 - Undefined non-fatal issue",
        "error-309": "Error 309 - Database Connection Error",
        "error-399": "Error 399 - Not Supported Error",
        "all-rights-reserved": "TASMAN Task Manager. All rights reserved."
    },
    pl: {
        "task-manager": "TASMAN Task Manager",
        "sort-by": "Sortuj według:",
        "id": "ID",
        "title": "Tytuł zadania",
        "status": "Status zadania",
        "order": "Kolejność:",
        "ascending": "Rosnąco",
        "descending": "Malejąco",
        "sort": "Sortuj",
        "help": "Pomoc",
        "operation": "Operacja",
        "choose-operation": "Wybierz operację",
        "add": "Dodaj nowe zadanie",
        "update": "Zaktualizuj status zadania",
        "delete": "Usuń zadanie",
        "show-help": "Pokaż pomoc",
        "select-operation": "Wybierz operację",
        "add-task": "Dodaj zadanie",
        "edit-task": "Edytuj zadanie",     
        "task-id": "ID zadania",  
        "edit": "Edytuj",    
        "task-name": "Nazwa zadania:",
        "description": "Opis:",
        "status": "Status:",
        "to-do": "Do zrobienia",
        "in-progress": "W trakcie",
        "done": "Zrobione",
        "ND": "BD",
        "update-task": "Zaktualizuj status zadania",
        "new-status": "Nowy status:",
        "delete-task": "Usuń zadanie",
        "help-title": "POMOC",
        "help-description": "Witaj w aplikacji Task Manager. Aby dodać nowe zadanie, wybierz operację 'Dodaj nowe zadanie' i wypełnij formularz. Aby edytować istniejące zadanie wybierz 'Edytuj zadanie'. Aby zaktualizować zadanie, wybierz operację 'Zaktualizuj zadanie' i wypełnij formularz. Aby usunąć zadanie, wybierz operację 'Usuń zadanie' i wypełnij formularz. Aby posortować zadania, wybierz odpowiednie opcje z list rozwijanych. Powodzenia!",
        "error-title": "MOŻLIWE KODY BŁĘDÓW:",
        "error-301": "Błąd 301 - Błąd wartości",
        "error-302": "Błąd 302 - Plik nie znaleziony",
        "error-303": "Błąd 303 - Błąd operacyjny",
        "error-304": "Błąd 304 - Błąd bazy danych",
        "error-305": "Błąd 305 - Błąd integralności",
        "error-306": "Błąd 306 - Błąd składni lub nieprawidłowa operacja",
        "error-307": "Błąd 307 - Błąd danych",
        "error-308": "Błąd 308 - Niezdefiniowany problem niekrytyczny",
        "error-309": "Błąd połączenia z bazą danych",
        "error-399": "Błąd 399 - Błąd nieobsługiwany",
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
        element.textContent = translations[currentLanguage][key];
    });

    // Update overlay content
    document.getElementById('overlay-title').textContent = translations[currentLanguage]['help-title'];
    document.getElementById('overlay-description').textContent = translations[currentLanguage]['help-description'];
}

// Initial translation application
applyTranslations();