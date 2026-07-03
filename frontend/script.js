const API_URL = 'http://localhost:8000';

const noteTitle = document.getElementById('noteTitle');
const noteInput = document.getElementById('noteInput');
const searchInput = document.getElementById('searchInput');
const addBtn = document.getElementById('addBtn');
const notesList = document.getElementById('notesList');
const errorMsg = document.getElementById('error');

// Tabs
const tabAdd = document.getElementById('tabAdd');
const tabSearch = document.getElementById('tabSearch');
const addSection = document.getElementById('addSection');
const searchSection = document.getElementById('searchSection');

let editingNoteId = null;

// Tab logic
tabAdd.addEventListener('click', () => {
    tabAdd.classList.add('active');
    tabSearch.classList.remove('active');
    addSection.classList.add('active');
    searchSection.classList.remove('active');
    searchSection.classList.add('hidden');
    
    searchInput.value = '';
    fetchNotes();
});

tabSearch.addEventListener('click', () => {
    tabSearch.classList.add('active');
    tabAdd.classList.remove('active');
    searchSection.classList.add('active');
    searchSection.classList.remove('hidden');
    addSection.classList.remove('active');
    searchInput.focus();
});

document.addEventListener('DOMContentLoaded', () => fetchNotes());

noteInput.addEventListener('keydown', (e) => {
    if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') {
        addNote();
    }
});
noteTitle.addEventListener('keydown', (e) => {
    if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') {
        addNote();
    }
});

let searchTimeout;
searchInput.addEventListener('input', () => {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
        fetchNotes(searchInput.value.trim());
    }, 300);
});

addBtn.addEventListener('click', addNote);

async function fetchNotes(searchQuery = '') {
    try {
        let url = `${API_URL}/notes`;
        if (searchQuery) {
            url += `?search=${encodeURIComponent(searchQuery)}`;
        }
        
        const response = await fetch(url);
        if (!response.ok) throw new Error('Failed to fetch notes');
        
        const data = await response.json();
        renderNotes(data.notes);
    } catch (err) {
        showError('Could not connect to the backend. Is it running on port 8000?');
        console.error(err);
    }
}

async function addNote() {
    const titleText = noteTitle.value.trim();
    const contentText = noteInput.value.trim();
    if (!contentText) return;

    addBtn.disabled = true;
    errorMsg.classList.add('hidden');

    try {
        if (editingNoteId) {
            const response = await fetch(`${API_URL}/notes/${editingNoteId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ title: titleText, content: contentText })
            });
            if (!response.ok) throw new Error('Failed to update note');
            
            editingNoteId = null;
            addBtn.innerHTML = '<span class="btn-text">Add Note</span>';
        } else {
            const response = await fetch(`${API_URL}/notes`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ title: titleText, content: contentText })
            });
            if (!response.ok) throw new Error('Failed to add note');
        }

        noteTitle.value = '';
        noteInput.value = '';
        searchInput.value = ''; 
        await fetchNotes();
        
    } catch (err) {
        showError('Failed to save note.');
        console.error(err);
    } finally {
        addBtn.disabled = false;
        noteInput.focus();
    }
}

async function deleteNote(id) {
    if (!confirm('Are you sure you want to delete this note?')) return;
    
    try {
        const response = await fetch(`${API_URL}/notes/${id}`, { method: 'DELETE' });
        if (!response.ok) throw new Error('Failed to delete note');
        await fetchNotes(searchInput.value.trim());
    } catch (err) {
        showError('Failed to delete note.');
        console.error(err);
    }
}

function startEditNote(id, currentTitle, currentContent) {
    tabAdd.click();
    editingNoteId = id;
    noteTitle.value = currentTitle === 'Untitled' ? '' : currentTitle;
    noteInput.value = currentContent;
    noteInput.focus();
    addBtn.innerHTML = '<span class="btn-text">Save Edit</span>';
}

function renderNotes(notes) {
    notesList.innerHTML = '';
    if (notes.length === 0) {
        notesList.innerHTML = '<li class="note-item" style="text-align: center; color: var(--text-secondary); background: transparent; border: none; box-shadow: none;">No notes yet. Add one above!</li>';
        return;
    }
    notes.forEach(note => createNoteElement(note.id, note.title, note.content));
}

function createNoteElement(id, title, content) {
    const li = document.createElement('li');
    li.className = 'note-item';
    
    const titleDiv = document.createElement('div');
    titleDiv.className = 'note-title';
    titleDiv.textContent = title; 

    const contentDiv = document.createElement('div');
    contentDiv.className = 'note-content';
    contentDiv.textContent = content; 
    
    const actionsDiv = document.createElement('div');
    actionsDiv.className = 'note-actions';
    
    const editBtn = document.createElement('button');
    editBtn.className = 'btn-edit';
    editBtn.textContent = 'Edit';
    editBtn.onclick = () => startEditNote(id, title, content);
    
    const deleteBtn = document.createElement('button');
    deleteBtn.className = 'btn-delete';
    deleteBtn.textContent = 'Delete';
    deleteBtn.onclick = () => deleteNote(id);
    
    actionsDiv.appendChild(editBtn);
    actionsDiv.appendChild(deleteBtn);
    
    li.appendChild(titleDiv);
    li.appendChild(contentDiv);
    li.appendChild(actionsDiv);
    
    notesList.appendChild(li);
}

function showError(msg) {
    errorMsg.textContent = msg;
    errorMsg.classList.remove('hidden');
}
