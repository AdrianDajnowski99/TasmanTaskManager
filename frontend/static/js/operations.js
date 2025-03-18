const operationSelect = document.getElementById('Operation');
const selectButton = document.getElementById('Select_Operation');
const addSection = document.getElementById('AddTask');
const editSection = document.getElementById('EditTask');
const updateSection = document.getElementById('UpdateTask');
const deleteSection = document.getElementById('DeleteTask');
const helpButton = document.getElementById('Select_Help'); // Help button
const overlay = document.getElementById('overlay');
const closeBtn = document.getElementById('close-btn');

// Show the appropriate section based on selected operation
selectButton.addEventListener('click', () => {
    addSection.classList.remove('active');
    editSection.classList.remove('active');
    updateSection.classList.remove('active');
    deleteSection.classList.remove('active');

    const selectedOperation = operationSelect.value;

    if (selectedOperation === 'add') {
        addSection.classList.add('active');
    } else if (selectedOperation === 'edit') {
        editSection.classList.add('active');
    } else if (selectedOperation === 'update') {
        updateSection.classList.add('active');
    } else if (selectedOperation === 'delete') {
        deleteSection.classList.add('active');
    } else {
        alert('Please select a valid operation!');
    }
});

// Open the overlay when the "Help" button is clicked
helpButton.addEventListener('click', () => {
    overlay.classList.add('active'); // Add the 'active' class to show the overlay
});

// Close the overlay
function closeOverlay() {
    overlay.classList.remove('active'); // Remove the 'active' class to hide the overlay
}

// Handle closing the overlay via the close button
closeBtn.addEventListener('click', closeOverlay);

// Handle closing the overlay via the Escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && overlay.classList.contains('active')) {
        closeOverlay();
    }
});
