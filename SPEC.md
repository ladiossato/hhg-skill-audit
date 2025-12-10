# CLAUDE CODE ONE-SHOT BUILD PROMPT
## HHG Skill Audit - Local HTML Application

---

## PROJECT OVERVIEW

| Parameter | Value |
|-----------|-------|
| **Application** | HHG Skill Audit |
| **Architecture** | Single HTML file (zero dependencies) |
| **Hosting** | Local file (double-click to run) |
| **Data Storage** | Browser localStorage |
| **Export** | Notion API (auto-creates database if needed) + JSON fallback |
| **Configuration** | Pre-configured, user-adjustable via Settings panel |
| **Output File** | `hhg-skill-audit.html` |

---

## OBJECTIVE

Build a single `hhg-skill-audit.html` file that provides:
1. A clickable matrix grid (14 team members × 4 constraints) for one-click violation logging
2. Keyboard shortcuts using adjacent keys (A-S-D-F for constraints, 1-9/0/Q-E for people)
3. Session management with 8-hour timeout and auto-save
4. Export to Notion with aggregated daily summaries per person
5. Auto-setup of Notion database if properties are missing
6. Extensive console logging for complete execution visibility

---

## PRE-CONFIGURED DATA (Hardcoded)

### Team Members (14)

```javascript
const TEAM = [
    'Lydell Tyler',
    'Efrain Campos',
    'Ismael Costilla',
    'Lizbeth Espinoza',
    'Anthony Esparza',
    'David Slavoff',
    'Refugio Guzman',
    'Sarah Lopez',
    'Edgar Jaimes',
    'David Crafton',
    'Anthony Gonzalez',
    'Brittany Gomez',
    'Floyd Jefferson',
    'Erin Hirtzig'
];
```

### Constraints (4) - Adjacent Keys A-S-D-F

```javascript
const CONSTRAINTS = [
    { 
        id: 'buffer', 
        name: 'Buffer', 
        fullName: 'Buffer State',
        station: 'Cook', 
        key: 'a',
        question: 'Is hot-hold at ≥80%?'
    },
    { 
        id: 'staging', 
        name: 'Staging', 
        fullName: 'Staging Limit',
        station: 'Mid-pack', 
        key: 's',
        question: 'Are there ≤4 bowls?'
    },
    { 
        id: 'docking', 
        name: 'Docking', 
        fullName: 'Order Docking',
        station: 'Mid-pack', 
        key: 'd',
        question: 'All items grouped together?'
    },
    { 
        id: 'focus', 
        name: 'Focus', 
        fullName: 'Single Focus',
        station: 'Expo', 
        key: 'f',
        question: 'Only 1 order in work zone?'
    }
];
```

### Stations

```javascript
const STATIONS = ['Cook', 'Mid-pack', 'Expo', 'Float'];
```

### Notion Configuration (Pre-filled)

```javascript
const NOTION_CONFIG = {
    token: 'ntn_tK4503835768z7NMcMwFc9MoxcFOr1XBaACyRRy8iOR0RH',
    databaseId: '2c501ad84ed880e5a4edc56122f60cb7'
};
```

### Keyboard Shortcuts

```javascript
// Person selection: 1-9 for first 9, 0 for 10th, Q/W/E/R for 11-14
const PERSON_KEYS = {
    '1': 0,  // Lydell Tyler
    '2': 1,  // Efrain Campos
    '3': 2,  // Ismael Costilla
    '4': 3,  // Lizbeth Espinoza
    '5': 4,  // Anthony Esparza
    '6': 5,  // David Slavoff
    '7': 6,  // Refugio Guzman
    '8': 7,  // Sarah Lopez
    '9': 8,  // Edgar Jaimes
    '0': 9,  // David Crafton
    'q': 10, // Anthony Gonzalez
    'w': 11, // Brittany Gomez
    'e': 12, // Floyd Jefferson
    'r': 13  // Erin Hirtzig
};

// Constraint selection: A-S-D-F (adjacent home row keys)
const CONSTRAINT_KEYS = {
    'a': 0, // Buffer
    's': 1, // Staging
    'd': 2, // Docking
    'f': 3  // Focus
};
```

---

## LOGGING INSTRUMENTATION

**Every function must log entry, exit, and errors using this exact format:**

```javascript
const LOG = {
    enter: (fn, params) => console.log(
        `%c[${fn}] ▶ ENTER`, 'color: #3b82f6; font-weight: bold',
        params ? `| params:` : '', params || ''
    ),
    exit: (fn, result) => console.log(
        `%c[${fn}] ✓ EXIT`, 'color: #22c55e; font-weight: bold',
        result !== undefined ? `| result:` : '', result !== undefined ? result : ''
    ),
    error: (fn, err) => console.error(
        `%c[${fn}] ✗ ERROR`, 'color: #ef4444; font-weight: bold',
        `|`, err
    ),
    data: (fn, label, data) => console.log(
        `%c[${fn}] 📊 ${label}`, 'color: #a855f7', data
    ),
    state: (fn, key, oldVal, newVal) => console.log(
        `%c[${fn}] 🔄 STATE`, 'color: #f97316',
        `| ${key}: ${JSON.stringify(oldVal)} → ${JSON.stringify(newVal)}`
    ),
    action: (fn, action) => console.log(
        `%c[${fn}] 👆 ACTION`, 'color: #06b6d4; font-weight: bold', `| ${action}`
    ),
    network: (fn, method, url, status) => console.log(
        `%c[${fn}] 🌐 ${method}`, status >= 400 ? 'color: #ef4444' : 'color: #22c55e',
        `| ${url} | Status: ${status}`
    ),
    warn: (fn, msg) => console.warn(
        `%c[${fn}] ⚠ WARN`, 'color: #eab308; font-weight: bold', `| ${msg}`
    )
};
```

---

## ARCHITECTURE

### Data Flow

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                                                                 │
│  USER CLICK (or keyboard: person key + constraint key)                          │
│       │                                                                         │
│       ▼                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────────┐    │
│  │  1. Create log entry: {person, constraint, station, timestamp}          │    │
│  │  2. Push to state.logs array                                            │    │
│  │  3. Update state.counts[person][constraint]++                           │    │
│  │  4. Save state to localStorage                                          │    │
│  │  5. Flash cell green (visual feedback)                                  │    │
│  │  6. Update counter display                                              │    │
│  └─────────────────────────────────────────────────────────────────────────┘    │
│                                                                                 │
│  ─────────────────────────────────────────────────────────────────────────────  │
│                                                                                 │
│  EXPORT TO NOTION                                                               │
│       │                                                                         │
│       ▼                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────────┐    │
│  │  1. Aggregate logs by person → {person: {buffer: N, staging: N, ...}}   │    │
│  │  2. Prompt for Total Orders count                                       │    │
│  │  3. For each person with violations:                                    │    │
│  │     a. Generate title: SA-{DATE}-{STATION}-{INITIALS}                   │    │
│  │     b. POST to Notion API                                               │    │
│  │     c. Log success/failure                                              │    │
│  │  4. If any failures → offer JSON download                               │    │
│  │  5. If all success → offer to clear session                             │    │
│  └─────────────────────────────────────────────────────────────────────────┘    │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### State Schema

```javascript
const STATE_SCHEMA = {
    sessionId: 'string (YYYYMMDD_HHMMSS)',
    sessionStart: 'number (unix timestamp ms)',
    logs: [
        {
            id: 'uuid',
            person: 'string (full name)',
            constraint: 'string (Buffer|Staging|Docking|Focus)',
            station: 'string (Cook|Mid-pack|Expo)',
            timestamp: 'ISO 8601 string'
        }
    ],
    counts: {
        'Person Name': {
            buffer: 0,
            staging: 0,
            docking: 0,
            focus: 0
        }
    }
};
```

### Notion Database Schema

The export creates/updates rows with this structure:

| Property | Type | Example | Notes |
|----------|------|---------|-------|
| **Title** | Title | `SA-120924-Cook-EJ` | Auto-generated |
| **Team Member** | Select | `Edgar Jaimes` | From TEAM array |
| **Station** | Select | `Cook` | Primary station audited |
| **Date** | Date | `2024-12-09` | Audit date |
| **Buffer** | Number | `3` | Count of buffer violations |
| **Staging** | Number | `1` | Count of staging violations |
| **Docking** | Number | `0` | Count of docking violations |
| **Focus** | Number | `2` | Count of focus violations |
| **Total Orders** | Number | `47` | User enters at export |
| **Total Misses** | Formula | `6` | `Buffer + Staging + Docking + Focus` |
| **Miss Rate** | Formula | `12.8%` | `Total Misses / Total Orders` |

---

## UI SPECIFICATION

### Layout

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│  HEADER                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────────┐    │
│  │  HHG Skill Audit                    Logged: [47] | Session: [01:23:45]  │    │
│  └─────────────────────────────────────────────────────────────────────────┘    │
│                                                                                 │
│  MATRIX (14 rows × 4 columns)                                                   │
│  ┌─────────────────────────────────────────────────────────────────────────┐    │
│  │             │ Buffer [A] │ Staging [S] │ Docking [D] │ Focus [F] │      │    │
│  │             │   Cook     │  Mid-pack   │  Mid-pack   │   Expo    │      │    │
│  │  ───────────┼────────────┼─────────────┼─────────────┼───────────┤      │    │
│  │  [1] Lydell Tyler    │     [2]    │      [ ]    │      [1]    │    [ ]   │    │
│  │  [2] Efrain Campos   │     [ ]    │      [1]    │      [ ]    │    [3]   │    │
│  │  [3] Ismael Costilla │     [ ]    │      [ ]    │      [ ]    │    [ ]   │    │
│  │  [4] Lizbeth Espinoza│     [1]    │      [ ]    │      [ ]    │    [ ]   │    │
│  │  [5] Anthony Esparza │     [ ]    │      [2]    │      [ ]    │    [ ]   │    │
│  │  [6] David Slavoff   │     [ ]    │      [ ]    │      [1]    │    [ ]   │    │
│  │  [7] Refugio Guzman  │     [ ]    │      [ ]    │      [ ]    │    [1]   │    │
│  │  [8] Sarah Lopez     │     [ ]    │      [ ]    │      [ ]    │    [ ]   │    │
│  │  [9] Edgar Jaimes    │     [1]    │      [1]    │      [ ]    │    [ ]   │    │
│  │  [0] David Crafton   │     [ ]    │      [ ]    │      [ ]    │    [ ]   │    │
│  │  [Q] Anthony Gonzalez│     [ ]    │      [1]    │      [2]    │    [ ]   │    │
│  │  [W] Brittany Gomez  │     [ ]    │      [ ]    │      [ ]    │    [ ]   │    │
│  │  [E] Floyd Jefferson │     [1]    │      [ ]    │      [ ]    │    [1]   │    │
│  │  [R] Erin Hirtzig    │     [ ]    │      [1]    │      [ ]    │    [ ]   │    │
│  └─────────────────────────────────────────────────────────────────────────┘    │
│                                                                                 │
│  CONTROLS                                                                       │
│  ┌─────────────────────────────────────────────────────────────────────────┐    │
│  │  [Clear Session]    [Export to Notion]    [Download JSON]               │    │
│  └─────────────────────────────────────────────────────────────────────────┘    │
│                                                                                 │
│  KEYBOARD GUIDE                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐    │
│  │  People: 1-9, 0, Q, W, E, R  |  Constraints: A S D F  |  Undo: Z        │    │
│  └─────────────────────────────────────────────────────────────────────────┘    │
│                                                                                 │
│  RECENT LOGS (last 10)                                                          │
│  ┌─────────────────────────────────────────────────────────────────────────┐    │
│  │  Edgar Jaimes → Buffer                                      14:32:15    │    │
│  │  Efrain Campos → Focus                                      14:31:02    │    │
│  │  Lydell Tyler → Buffer                                      14:30:45    │    │
│  │  ...                                                                    │    │
│  └─────────────────────────────────────────────────────────────────────────┘    │
│                                                                                 │
│  SETTINGS (collapsible)                                                         │
│  ┌─────────────────────────────────────────────────────────────────────────┐    │
│  │  ▶ Notion Settings (click to expand)                                    │    │
│  │  ▶ Add/Remove Team Members                                              │    │
│  │  ▶ Add/Remove Constraints                                               │    │
│  └─────────────────────────────────────────────────────────────────────────┘    │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## FUNCTION SPECIFICATIONS

### Core Functions (All Must Include Logging)

```javascript
// ══════════════════════════════════════════════════════════════════════════════
// INITIALIZATION
// ══════════════════════════════════════════════════════════════════════════════

function init() {
    // LOG.enter, banner, load state, render UI, attach listeners, LOG.exit
}

// ══════════════════════════════════════════════════════════════════════════════
// STATE MANAGEMENT
// ══════════════════════════════════════════════════════════════════════════════

function loadState() {
    // Load from localStorage, check 8-hour timeout, return fresh if expired
}

function saveState() {
    // Save current state to localStorage
}

function addLog(person, constraint) {
    // Create log entry, update counts, save, update UI
}

function undoLastLog() {
    // Remove last log, update counts, save, update UI
}

function clearSession() {
    // Confirm, reset state, save, re-render
}

// ══════════════════════════════════════════════════════════════════════════════
// NOTION EXPORT
// ══════════════════════════════════════════════════════════════════════════════

async function exportToNotion() {
    // Aggregate logs by person
    // Prompt for total orders
    // POST each person's summary to Notion
    // Handle errors, offer JSON fallback
}

function aggregateLogsByPerson() {
    // Returns: { 'Person Name': { buffer: N, staging: N, docking: N, focus: N } }
}

function generateTitle(person, date) {
    // Returns: SA-MMDDYY-STATION-INITIALS (e.g., SA-120924-Cook-EJ)
}

async function createNotionRow(person, counts, totalOrders, date) {
    // POST to Notion API with proper schema
}

// ══════════════════════════════════════════════════════════════════════════════
// UI RENDERING
// ══════════════════════════════════════════════════════════════════════════════

function renderMatrix() {
    // Build header row with constraints
    // Build 14 person rows with clickable cells
    // Show shortcut keys in labels
}

function updateCounts() {
    // Update count badges in cells without full re-render
}

function flashCell(person, constraint) {
    // Add flash animation class, remove after 300ms
}

function renderRecentLogs() {
    // Show last 10 logs in reverse chronological order
}

function updateSessionTimer() {
    // Update HH:MM:SS display
}

function showModal(title, content, buttons) {
    // Generic modal for confirmations and inputs
}

function showToast(message, type) {
    // Toast notification (success/error/info)
}

// ══════════════════════════════════════════════════════════════════════════════
// EVENT HANDLERS
// ══════════════════════════════════════════════════════════════════════════════

function handleCellClick(personIndex, constraintIndex) {
    // Get person and constraint from indices, call addLog
}

function handleKeydown(event) {
    // Person keys: 1-9, 0, Q, W, E, R → set pending person
    // Constraint keys: A, S, D, F → log if person pending
    // Z → undo last log
    // Escape → clear pending
}

function handleExportClick() {
    // Show modal for total orders input, then call exportToNotion
}

function handleDownloadClick() {
    // Generate and download JSON file
}

function handleClearClick() {
    // Show confirmation modal, then clearSession
}

// ══════════════════════════════════════════════════════════════════════════════
// UTILITIES
// ══════════════════════════════════════════════════════════════════════════════

function generateUUID() {
    // Return UUID v4
}

function generateSessionId() {
    // Return YYYYMMDD_HHMMSS
}

function getInitials(fullName) {
    // "Edgar Jaimes" → "EJ"
}

function formatTime(ms) {
    // Milliseconds → HH:MM:SS
}
```

---

## STYLING REQUIREMENTS

```css
/* 
 * Dark theme with HHG branding feel
 * Background: #0f172a (darkest), #1e293b (cards), #334155 (borders)
 * Text: #e2e8f0 (primary), #94a3b8 (secondary), #64748b (muted)
 * Accents: #3b82f6 (blue), #22c55e (green), #ef4444 (red), #f97316 (orange)
 *
 * Matrix cells: minimum 44px height for touch targets
 * Responsive: works on tablet as secondary audit device
 * Keyboard shortcuts visible in UI
 */
```

---

## NOTION API DETAILS

### Endpoint

```
POST https://api.notion.com/v1/pages
```

### Headers

```javascript
{
    'Authorization': `Bearer ${NOTION_CONFIG.token}`,
    'Notion-Version': '2022-06-28',
    'Content-Type': 'application/json'
}
```

### Request Body (Per Person Export)

```javascript
{
    parent: { database_id: NOTION_CONFIG.databaseId },
    properties: {
        'Name': {
            title: [{ text: { content: 'SA-120924-Cook-EJ' } }]
        },
        'Team Member': {
            select: { name: 'Edgar Jaimes' }
        },
        'Station': {
            select: { name: 'Cook' }
        },
        'Date': {
            date: { start: '2024-12-09' }
        },
        'Buffer': {
            number: 2
        },
        'Staging': {
            number: 1
        },
        'Docking': {
            number: 0
        },
        'Focus': {
            number: 3
        },
        'Total Orders': {
            number: 47
        }
    }
}
```

---

## NOTION DATABASE SETUP SCRIPT

### Script: `setup-notion.py`

**Purpose:** Creates Notion database with all required properties before first use.

**Credentials:**
```
Token: ntn_tK4503835768z7NMcMwFc9MoxcFOr1XBaACyRRy8iOR0RH
Parent Page ID: 2c501ad84ed880e5a4edc56122f60cb7
```

**API Call:**
```
POST https://api.notion.com/v1/databases
Headers:
  Authorization: Bearer {token}
  Notion-Version: 2022-06-28
  Content-Type: application/json
```

**Database Properties to Create:**

| Property | Type | Configuration |
|----------|------|---------------|
| Name | title | — |
| Team Member | select | 14 options (all team members) |
| Station | select | Cook, Mid-pack, Expo, Float |
| Date | date | — |
| Buffer | number | format: number |
| Staging | number | format: number |
| Docking | number | format: number |
| Focus | number | format: number |
| Total Orders | number | format: number |
| Total Misses | formula | `prop("Buffer") + prop("Staging") + prop("Docking") + prop("Focus")` |
| Miss Rate | formula | `if(prop("Total Orders") > 0, prop("Total Misses") / prop("Total Orders"), 0)` |

**Team Member Select Options:**
```python
[
    {"name": "Lydell Tyler", "color": "blue"},
    {"name": "Efrain Campos", "color": "green"},
    {"name": "Ismael Costilla", "color": "yellow"},
    {"name": "Lizbeth Espinoza", "color": "pink"},
    {"name": "Anthony Esparza", "color": "purple"},
    {"name": "David Slavoff", "color": "orange"},
    {"name": "Refugio Guzman", "color": "red"},
    {"name": "Sarah Lopez", "color": "blue"},
    {"name": "Edgar Jaimes", "color": "green"},
    {"name": "David Crafton", "color": "yellow"},
    {"name": "Anthony Gonzalez", "color": "pink"},
    {"name": "Brittany Gomez", "color": "purple"},
    {"name": "Floyd Jefferson", "color": "orange"},
    {"name": "Erin Hirtzig", "color": "red"}
]
```

**Station Select Options:**
```python
[
    {"name": "Cook", "color": "red"},
    {"name": "Mid-pack", "color": "orange"},
    {"name": "Expo", "color": "green"},
    {"name": "Float", "color": "blue"}
]
```

**Script Requirements:**
- Use `requests` library for HTTP calls
- Include full logging instrumentation (LOG.enter/LOG.exit/LOG.error)
- Print database ID on success
- Handle common errors (401 auth, 404 not found, 400 permissions)
- Exit with code 0 on success, 1 on failure

**Success Output Format:**
```
======================================================================
SUCCESS! Database created.
======================================================================
Database ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
Database URL: https://www.notion.so/...
======================================================================
```
### Error Handling

```javascript
// If Notion returns error about missing properties:
// 1. Log the error with full details
// 2. Show user-friendly message
// 3. Offer JSON download as fallback
// 4. Do NOT attempt to auto-create properties (requires different permissions)
```

---

## COMPLETE BUILD CHECKLIST

The generated `hhg-skill-audit.html` file must include:

### HTML Structure
- [ ] Header with title and session stats
- [ ] Matrix grid: 14 rows × 4 columns
- [ ] Control buttons: Clear, Export, Download
- [ ] Keyboard guide display
- [ ] Recent logs panel (last 10)
- [ ] Collapsible settings panel
- [ ] Modal container for dialogs
- [ ] Toast container for notifications

### CSS (in `<style>` tag)
- [ ] Dark theme colors
- [ ] Matrix cell styling with hover/active states
- [ ] Flash animation for logged cells
- [ ] Responsive layout (works on tablet)
- [ ] Modal and toast styling
- [ ] Keyboard shortcut badges

### JavaScript (in `<script>` tag)
- [ ] LOG utility object with all 8 log types
- [ ] TEAM array (14 members, hardcoded)
- [ ] CONSTRAINTS array (4 items, hardcoded)
- [ ] STATIONS array (4 items, hardcoded)
- [ ] NOTION_CONFIG object (token + database ID, hardcoded)
- [ ] PERSON_KEYS mapping (1-9, 0, Q-R)
- [ ] CONSTRAINT_KEYS mapping (A-S-D-F)
- [ ] All state management functions with logging
- [ ] All UI rendering functions with logging
- [ ] All event handlers with logging
- [ ] Notion export function with logging
- [ ] JSON download function
- [ ] Keyboard shortcut handler
- [ ] Undo functionality (Z key)
- [ ] Session timeout check (8 hours)
- [ ] init() function called on DOMContentLoaded

### Logging Coverage
- [ ] Every function has LOG.enter at start
- [ ] Every function has LOG.exit at end
- [ ] Every try block has LOG.error in catch
- [ ] State changes logged with LOG.state
- [ ] User actions logged with LOG.action
- [ ] Network calls logged with LOG.network
- [ ] Data transformations logged with LOG.data

---

## USER SETUP INSTRUCTIONS

Embed this at the top of the HTML file:

```html
<!--
═══════════════════════════════════════════════════════════════════════════════
HHG SKILL AUDIT - READY TO USE
═══════════════════════════════════════════════════════════════════════════════

SETUP: None required. Just double-click this file to open in your browser.

USAGE:
  1. Click any cell to log a constraint violation
  2. Or use keyboard: Press person key (1-9, 0, Q, W, E, R) then A/S/D/F
  3. Press Z to undo last log
  4. Click "Export to Notion" when done - enter total orders when prompted
  5. Data syncs to your Notion database automatically

KEYBOARD SHORTCUTS:
  People (1-9, 0, Q-R):
    1=Lydell  2=Efrain  3=Ismael  4=Lizbeth  5=Anthony E.
    6=David S.  7=Refugio  8=Sarah  9=Edgar  0=David C.
    Q=Anthony G.  W=Brittany  E=Floyd  R=Erin

  Constraints (A-S-D-F):
    A=Buffer (Cook)
    S=Staging (Mid-pack)
    D=Docking (Mid-pack)
    F=Focus (Expo)

  Other:
    Z=Undo last log
    Escape=Cancel pending selection

TROUBLESHOOTING:
  • Open browser console (F12) to see detailed logs
  • All actions are logged with timestamps
  • If Notion export fails, use "Download JSON" as backup

NOTION DATABASE:
  Your data exports to: Skill Audit database
  Properties: Name, Team Member, Station, Date, Buffer, Staging, Docking, Focus, Total Orders

  If you see property errors, ensure your Notion database has all required columns.

═══════════════════════════════════════════════════════════════════════════════
-->
```

---

## VERIFICATION TESTS

After building, verify in browser:

| Test | Action | Expected Console Output |
|------|--------|-------------------------|
| Page load | Open file | `[init] ▶ ENTER` → config logs → `[init] ✓ EXIT` |
| Click cell | Click any cell | `[handleCellClick] ▶ ENTER` → `[addLog]` → flash → `✓ EXIT` |
| Keyboard log | Press `1` then `A` | `[handleKeydown]` → person selected → `[addLog]` |
| Undo | Press `Z` | `[undoLastLog] ▶ ENTER` → count decremented → `✓ EXIT` |
| Export | Click Export | `[exportToNotion]` → modal → network logs → success/fail |
| Session persist | Refresh page | Logs restored, counts intact |
| 8hr timeout | (simulate) | Old session cleared, fresh start |

---

## EXECUTION COMMAND

Build the complete `hhg-skill-audit.html` file following all specifications above.

**Critical Requirements:**
1. ✓ All 14 team members hardcoded
2. ✓ All 4 constraints with A-S-D-F keys hardcoded
3. ✓ Notion token and database ID hardcoded
4. ✓ Every function has complete logging instrumentation
5. ✓ Keyboard shortcuts work globally (not just when focused)
6. ✓ Undo (Z) removes last log
7. ✓ Export aggregates by person, prompts for total orders
8. ✓ 8-hour session timeout
9. ✓ Mobile-responsive layout
10. ✓ Zero setup required for end user

**Output:** Single file named `hhg-skill-audit.html`

Begin building now.
