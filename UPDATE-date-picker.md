# UPDATE: Add Audit Date Selector

## Context

The `hhg-skill-audit.html` application is already built and working. This update adds a date picker so the user can select which date they're auditing for before exporting to Notion.

---

## Feature: Audit Date Selector

### What to Add

A date input field in the header area that:
1. Defaults to today's date
2. Allows user to select any date
3. Uses the selected date when exporting to Notion (not the current date)
4. Persists in session state (survives page refresh)

---

## UI Change

Add date picker to the header, next to session stats:

```
BEFORE:
┌─────────────────────────────────────────────────────────────────────────┐
│  HHG Skill Audit                    Logged: [47] | Session: [01:23:45]  │
└─────────────────────────────────────────────────────────────────────────┘

AFTER:
┌─────────────────────────────────────────────────────────────────────────┐
│  HHG Skill Audit        Audit Date: [12/10/2024]  | Logged: [47] | 01:23:45  │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Code Changes Required

### 1. Add to State Schema

```javascript
// Add to state object
state.auditDate = 'YYYY-MM-DD'  // ISO format, defaults to today
```

### 2. Add UI Element

```html
<label>
    Audit Date: 
    <input type="date" id="auditDate" value="2024-12-10" onchange="handleDateChange(event)">
</label>
```

Style to match existing dark theme.

### 3. Add Event Handler

```javascript
function handleDateChange(event) {
    LOG.enter('handleDateChange', { value: event.target.value });
    const oldDate = state.auditDate;
    state.auditDate = event.target.value;
    LOG.state('handleDateChange', 'auditDate', oldDate, state.auditDate);
    saveState();
    LOG.exit('handleDateChange');
}
```

### 4. Update loadState()

```javascript
// In loadState(), add:
if (!state.auditDate) {
    state.auditDate = new Date().toISOString().split('T')[0];  // Today
}
// Also update the date input element to show saved date
document.getElementById('auditDate').value = state.auditDate;
```

### 5. Update init()

```javascript
// In init(), after loadState():
document.getElementById('auditDate').value = state.auditDate;
```

### 6. Update exportToNotion()

Change how the date is set in the Notion API call:

```javascript
// BEFORE (probably using current date):
'Date': { date: { start: new Date().toISOString().split('T')[0] } }

// AFTER (use selected audit date):
'Date': { date: { start: state.auditDate } }
```

### 7. Update generateTitle()

If the title includes date, use `state.auditDate`:

```javascript
// BEFORE:
const dateStr = new Date().toLocaleDateString('en-US', {month: '2-digit', day: '2-digit', year: '2-digit'}).replace(/\//g, '');

// AFTER:
const [year, month, day] = state.auditDate.split('-');
const dateStr = `${month}${day}${year.slice(-2)}`;  // MMDDYY format
```

---

## Styling

Match existing dark theme:

```css
#auditDate {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 4px;
    color: #e2e8f0;
    padding: 4px 8px;
    font-size: 0.875rem;
}

#auditDate::-webkit-calendar-picker-indicator {
    filter: invert(1);  /* Make calendar icon visible on dark bg */
}
```

---

## Verification

After update, verify:
- [ ] Date picker appears in header
- [ ] Defaults to today's date on fresh session
- [ ] Selected date persists after page refresh
- [ ] Export to Notion uses selected date (not current date)
- [ ] Title generation uses selected date
- [ ] All new code has LOG.enter/LOG.exit/LOG.error
- [ ] Dark theme styling matches existing UI

---

## Execute

Update `hhg-skill-audit.html` with this feature. Do not rebuild from scratch—modify the existing file.
