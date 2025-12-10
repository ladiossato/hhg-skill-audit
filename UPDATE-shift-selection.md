# UPDATE: Shift Selection - Show Only Working Employees

## Context

The `hhg-skill-audit.html` currently displays all 14 employees in the matrix. This update adds shift selection so only employees working that shift appear in the matrix, reducing cognitive load during auditing.

---

## Feature: Shift Selection

### Behavior

1. **Fresh session**: Modal appears asking "Who's working this shift?"
2. **User selects**: Checkboxes for all 14 employees, select those on shift
3. **Matrix updates**: Only shows selected employees (3-8 typically)
4. **Keyboard shortcuts**: Dynamically assigned 1-N based on selection count
5. **Persists**: Shift selection saved in session state
6. **Editable**: "Edit Shift" button in Settings to modify mid-session

---

## UI Components

### 1. Shift Selection Modal (appears on fresh session)

```html
<div id="shiftModal" class="modal">
    <div class="modal-content">
        <h2>Who's working this shift?</h2>
        <div class="shift-grid">
            <!-- Checkbox for each of 14 employees -->
            <label class="shift-checkbox">
                <input type="checkbox" data-index="0" checked>
                <span>Lydell Tyler</span>
            </label>
            <!-- ... repeat for all 14 -->
        </div>
        <button onclick="confirmShiftSelection()" id="startAuditBtn">
            Start Audit (0 selected)
        </button>
    </div>
</div>
```

### 2. Updated Header

Add shift count indicator:

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│  HHG Skill Audit    Date: [12/10/24]  │  Shift: 4 people  │  Logged: 12  │ 01:23  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 3. Settings Panel Addition

```html
<div class="settings-section">
    <h3>Current Shift</h3>
    <p>Auditing: Lydell, Efrain, Sarah, Edgar</p>
    <button onclick="openShiftModal()">Edit Shift</button>
</div>
```

---

## State Changes

### Add to State Schema

```javascript
state.shiftEmployees = []  // Array of indices into TEAM array
// Example: [0, 1, 7, 8] means Lydell, Efrain, Sarah, Edgar selected
```

### Default Behavior

```javascript
// On fresh session:
if (!state.shiftEmployees || state.shiftEmployees.length === 0) {
    showShiftModal();  // Force selection before auditing
}
```

---

## Code Changes Required

### 1. Add Shift Modal HTML

Insert modal HTML at end of body, before closing `</body>` tag.

Style to match existing dark theme:

```css
.shift-modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.8);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
}

.shift-modal-content {
    background: #1e293b;
    border-radius: 8px;
    padding: 24px;
    max-width: 500px;
    width: 90%;
}

.shift-modal h2 {
    margin-bottom: 16px;
    color: #e2e8f0;
}

.shift-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 8px;
    margin-bottom: 20px;
}

.shift-checkbox {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px;
    background: #334155;
    border-radius: 4px;
    cursor: pointer;
}

.shift-checkbox:hover {
    background: #475569;
}

.shift-checkbox input {
    width: 18px;
    height: 18px;
    accent-color: #3b82f6;
}

.shift-checkbox span {
    color: #e2e8f0;
    font-size: 0.9rem;
}
```

### 2. Add Shift Functions

```javascript
function showShiftModal() {
    LOG.enter('showShiftModal');
    const modal = document.getElementById('shiftModal');
    modal.style.display = 'flex';
    
    // Pre-check previously selected employees
    state.shiftEmployees.forEach(idx => {
        const checkbox = document.querySelector(`#shiftModal input[data-index="${idx}"]`);
        if (checkbox) checkbox.checked = true;
    });
    
    updateShiftButtonCount();
    LOG.exit('showShiftModal');
}

function hideShiftModal() {
    LOG.enter('hideShiftModal');
    document.getElementById('shiftModal').style.display = 'none';
    LOG.exit('hideShiftModal');
}

function updateShiftButtonCount() {
    LOG.enter('updateShiftButtonCount');
    const checkboxes = document.querySelectorAll('#shiftModal input[type="checkbox"]:checked');
    const count = checkboxes.length;
    const btn = document.getElementById('startAuditBtn');
    btn.textContent = `Start Audit (${count} selected)`;
    btn.disabled = count === 0;
    LOG.exit('updateShiftButtonCount', count);
}

function confirmShiftSelection() {
    LOG.enter('confirmShiftSelection');
    
    const checkboxes = document.querySelectorAll('#shiftModal input[type="checkbox"]:checked');
    const oldShift = [...state.shiftEmployees];
    
    state.shiftEmployees = Array.from(checkboxes).map(cb => parseInt(cb.dataset.index));
    
    LOG.state('confirmShiftSelection', 'shiftEmployees', oldShift, state.shiftEmployees);
    
    if (state.shiftEmployees.length === 0) {
        showToast('Select at least one employee', 'error');
        LOG.warn('confirmShiftSelection', 'No employees selected');
        return;
    }
    
    saveState();
    hideShiftModal();
    renderMatrix();  // Re-render with only selected employees
    updateKeyboardHints();
    
    LOG.exit('confirmShiftSelection', state.shiftEmployees.length);
}

function getShiftTeam() {
    LOG.enter('getShiftTeam');
    // Returns array of employee names for current shift
    const team = state.shiftEmployees.map(idx => TEAM[idx]);
    LOG.exit('getShiftTeam', team);
    return team;
}
```

### 3. Update renderMatrix()

Change to only render employees in `state.shiftEmployees`:

```javascript
function renderMatrix() {
    LOG.enter('renderMatrix');
    
    const shiftTeam = getShiftTeam();
    LOG.data('renderMatrix', 'Rendering employees', shiftTeam.length);
    
    // Build header row (unchanged)
    // ...
    
    // Build person rows - ONLY for shift employees
    shiftTeam.forEach((person, displayIndex) => {
        const actualIndex = state.shiftEmployees[displayIndex];
        
        // Person label with dynamic keyboard shortcut
        const keyHint = getPersonKeyHint(displayIndex);
        const label = document.createElement('div');
        label.className = 'person-label';
        label.innerHTML = `<span class="key-hint">[${keyHint}]</span> ${person}`;
        matrix.appendChild(label);
        
        // Constraint cells
        CONSTRAINTS.forEach((constraint, cIdx) => {
            const cell = document.createElement('div');
            cell.className = 'cell';
            cell.id = `cell-${actualIndex}-${constraint.id}`;
            cell.onclick = () => handleCellClick(actualIndex, cIdx);
            
            const count = getCount(person, constraint.id);
            cell.innerHTML = `<span class="count ${count > 0 ? 'active' : ''}">${count || ''}</span>`;
            
            matrix.appendChild(cell);
        });
    });
    
    LOG.exit('renderMatrix');
}
```

### 4. Update Keyboard Handling

Dynamic shortcuts based on shift size:

```javascript
function getPersonKeyHint(displayIndex) {
    // 1-9 for first 9, then 0, Q, W, E, R
    if (displayIndex < 9) return (displayIndex + 1).toString();
    if (displayIndex === 9) return '0';
    const extras = ['Q', 'W', 'E', 'R'];
    return extras[displayIndex - 10] || '?';
}

function handleKeydown(event) {
    LOG.enter('handleKeydown', { key: event.key });
    
    const key = event.key.toLowerCase();
    const shiftTeam = getShiftTeam();
    
    // Dynamic person keys based on shift size
    let personDisplayIndex = null;
    
    if (key >= '1' && key <= '9') {
        personDisplayIndex = parseInt(key) - 1;
    } else if (key === '0') {
        personDisplayIndex = 9;
    } else if (key === 'q') {
        personDisplayIndex = 10;
    } else if (key === 'w') {
        personDisplayIndex = 11;
    } else if (key === 'e') {
        personDisplayIndex = 12;
    } else if (key === 'r') {
        personDisplayIndex = 13;
    }
    
    // Check if valid for current shift size
    if (personDisplayIndex !== null && personDisplayIndex < shiftTeam.length) {
        pendingPerson = state.shiftEmployees[personDisplayIndex];
        LOG.action('handleKeydown', `Person selected: ${TEAM[pendingPerson]}`);
    }
    
    // Constraint keys (unchanged: A, S, D, F)
    // ...
    
    LOG.exit('handleKeydown');
}
```

### 5. Update init()

```javascript
function init() {
    LOG.enter('init');
    // ... existing init code ...
    
    loadState();
    
    // Show shift modal if no shift selected
    if (!state.shiftEmployees || state.shiftEmployees.length === 0) {
        showShiftModal();
    } else {
        renderMatrix();
    }
    
    // ... rest of init ...
    LOG.exit('init');
}
```

### 6. Update loadState()

```javascript
function loadState() {
    LOG.enter('loadState');
    // ... existing code ...
    
    // Ensure shiftEmployees exists
    if (!state.shiftEmployees) {
        state.shiftEmployees = [];
    }
    
    LOG.exit('loadState');
}
```

### 7. Update Keyboard Hints Display

Make it dynamic based on shift size:

```javascript
function updateKeyboardHints() {
    LOG.enter('updateKeyboardHints');
    
    const shiftTeam = getShiftTeam();
    const maxKey = shiftTeam.length <= 9 
        ? shiftTeam.length.toString() 
        : shiftTeam.length === 10 
            ? '0' 
            : ['Q','W','E','R'][shiftTeam.length - 11];
    
    const hintsEl = document.getElementById('keyboardHints');
    hintsEl.textContent = `People: 1-${maxKey}  |  Constraints: A S D F  |  Undo: Z`;
    
    LOG.exit('updateKeyboardHints');
}
```

### 8. Add Edit Shift Button to Settings

```html
<div class="settings-section">
    <h3>Current Shift</h3>
    <p id="currentShiftDisplay">Loading...</p>
    <button onclick="showShiftModal()" class="btn-secondary">Edit Shift</button>
</div>
```

```javascript
function updateShiftDisplay() {
    const shiftTeam = getShiftTeam();
    const display = document.getElementById('currentShiftDisplay');
    display.textContent = shiftTeam.length > 0 
        ? `Auditing: ${shiftTeam.join(', ')}`
        : 'No shift selected';
}
```

---

## Verification Checklist

After update, verify:

- [ ] Fresh session shows shift selection modal
- [ ] Can select/deselect employees with checkboxes
- [ ] "Start Audit" button shows count and is disabled when 0 selected
- [ ] Matrix only shows selected employees after confirmation
- [ ] Keyboard shortcuts 1-N match displayed employees
- [ ] Shift selection persists after page refresh
- [ ] "Edit Shift" in Settings opens modal with current selection
- [ ] Changing shift mid-session updates matrix immediately
- [ ] Existing logs preserved when changing shift
- [ ] Export still works correctly (uses full employee names)
- [ ] All new functions have LOG.enter/LOG.exit/LOG.error

---

## Execute

Update `hhg-skill-audit.html` with this feature. Modify the existing file—do not rebuild from scratch.
