const API_URL = 'http://localhost:8000';

const noteInput = document.getElementById('noteInput');
const addBtn = document.getElementById('addBtn');
const notesList = document.getElementById('notesList');
const errorMsg = document.getElementById('error');

// Fetch notes on load
document.addEventListener('DOMContentLoaded', fetchNotes);

// Handle enter key
noteInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        addNote();
    }
});

addBtn.addEventListener('click', addNote);

async function fetchNotes() {
    try {
        const response = await fetch(`${API_URL}/notes`);
        if (!response.ok) throw new Error('Failed to fetch notes');
        
        const data = await response.json();
        renderNotes(data.notes);
    } catch (err) {
        showError('Could not connect to the backend. Is it running on port 8000?');
        console.error(err);
    }
}

async function addNote() {
    const text = noteInput.value.trim();
    if (!text) return;

    // Optimistic UI update or simple disable while loading
    addBtn.disabled = true;
    errorMsg.classList.add('hidden');

    try {
        const response = await fetch(`${API_URL}/notes`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ content: text })
        });

        if (!response.ok) throw new Error('Failed to add note');

        // Add note to list
        createNoteElement(text);
        noteInput.value = '';
        
        // Scroll to bottom
        notesList.scrollTop = notesList.scrollHeight;
    } catch (err) {
        showError('Failed to save note.');
        console.error(err);
    } finally {
        addBtn.disabled = false;
        noteInput.focus();
    }
}

function renderNotes(notes) {
    notesList.innerHTML = '';
    if (notes.length === 0) {
        notesList.innerHTML = '<li class="note-item" style="text-align: center; color: var(--text-secondary); background: transparent; border: none; box-shadow: none;">No notes yet. Add one above!</li>';
        return;
    }
    notes.forEach(note => createNoteElement(note));
}

function createNoteElement(text) {
    // Remove "No notes yet" message if it exists
    if (notesList.firstChild && notesList.firstChild.innerText && notesList.firstChild.innerText.includes('No notes yet')) {
        notesList.innerHTML = '';
    }
    
    const li = document.createElement('li');
    li.className = 'note-item';
    li.textContent = text;
    notesList.appendChild(li);
}

function showError(msg) {
    errorMsg.textContent = msg;
    errorMsg.classList.remove('hidden');
}
