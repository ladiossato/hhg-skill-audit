# UPDATE: UI/UX Redesign - Responsive Matrix with Observable Constraints

## Expert Persona

Before making any changes, embody these expert perspectives:

**Dr. Edward Tufte** - Information Design Pioneer
- "Above all else, show the data"
- Maximize data-ink ratio (remove non-essential elements)
- Small multiples for comparison
- Information at point of need

**Steve Krug** - Usability Expert ("Don't Make Me Think")
- Zero learning curve - meaning obvious at glance
- Eliminate cognitive overhead
- Convention over innovation for speed

**Luke Wroblewski** - Mobile-First Design
- Touch targets minimum 44px
- Progressive disclosure
- Content priority ruthlessly enforced

**Aarron Walter** - Emotional Design
- Color as information carrier
- Feedback loops build confidence
- Error states that guide, not blame

---

## Context

This is a **real-time video audit tool** for a kitchen manager. The auditor:
- Watches security camera footage (often on phone)
- Identifies constraint violations as they happen
- Needs to log violations in under 2 seconds
- Works in a fast-paced environment with interruptions
- May not remember abbreviations or abstract terms

**Critical Insight**: The auditor is watching a video feed while simultaneously logging. Every millisecond of eyes-off-camera is a missed violation.

---

## Constraint Renaming (Question-Based)

Update all constraint references throughout the codebase:

| Old Name | New Name | Station | Observable Signal | Description |
|----------|----------|---------|-------------------|-------------|
| Buffer | **Low Stock** | Cook | MidPack waiting for protein | Hot-hold below 80% |
| Staging | **Too Many** | Mid-pack | 5+ bowls visible on line | Overloaded assembly |
| Docking | **Split Order** | Mid-pack | Order items not grouped | Items scattered |
| Focus | **Mixed Orders** | Expo | 2+ orders being worked | Multiple bags open |

### Update CONSTRAINTS Array

```javascript
const CONSTRAINTS = [
    { 
        id: 'lowstock', 
        name: 'Low Stock', 
        station: 'Cook', 
        key: 'a',
        color: '#ef4444',  // Red
        signal: 'MidPack waiting',
        description: 'Hot-hold below 80%'
    },
    { 
        id: 'toomany', 
        name: 'Too Many', 
        station: 'Mid-pack', 
        key: 's',
        color: '#f97316',  // Orange
        signal: '5+ bowls visible',
        description: 'Overloaded assembly'
    },
    { 
        id: 'splitorder', 
        name: 'Split Order', 
        station: 'Mid-pack', 
        key: 'd',
        color: '#f97316',  // Orange
        signal: 'Items not grouped',
        description: 'Order scattered'
    },
    { 
        id: 'mixedorders', 
        name: 'Mixed Orders', 
        station: 'Expo', 
        key: 'f',
        color: '#22c55e',  // Green
        signal: '2+ orders open',
        description: 'Multiple bags'
    }
];
```

---

## Responsive Layout Design

### Breakpoints

```css
/* Mobile: < 768px - Card layout */
/* Desktop: >= 768px - Table layout */
```

---

## Desktop Layout (≥768px): Enhanced Table

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│  HHG AUDIT          Date: [12/10/24]    Shift: 3    Logged: 12    ⏱ 01:23       │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────┬───────────────┬─────────────────────────────┬────────────────┐ │
│  │             │   🔴 COOK     │        🟠 MID-PACK          │   🟢 EXPO      │ │
│  │             ├───────────────┼──────────────┬──────────────┼────────────────┤ │
│  │             │  Low Stock    │   Too Many   │  Split Order │  Mixed Orders  │ │
│  │             │  [A]          │   [S]        │  [D]         │  [F]           │ │
│  │             │  MidPack      │   5+ bowls   │  Items not   │  2+ orders     │ │
│  │             │  waiting      │   visible    │  grouped     │  open          │ │
│  ├─────────────┼───────────────┼──────────────┼──────────────┼────────────────┤ │
│  │ [1] Lydell  │      —        │      —       │      —       │       —        │ │
│  ├─────────────┼───────────────┼──────────────┼──────────────┼────────────────┤ │
│  │ [2] Ismael  │      —        │      2       │      1       │       —        │ │
│  ├─────────────┼───────────────┼──────────────┼──────────────┼────────────────┤ │
│  │ [3] Anthony │      —        │      —       │      —       │       1        │ │
│  └─────────────┴───────────────┴──────────────┴──────────────┴────────────────┘ │
│                                                                                 │
│  ┌─ Recent ─────────────────────────────────────────────────────────────────┐   │
│  │  Ismael → Too Many (2:34pm)  •  Ismael → Split Order (2:31pm)            │   │
│  └──────────────────────────────────────────────────────────────────────────┘   │
│                                                                                 │
│  [Clear Session]    [Export to Notion]    [Download JSON]    [⚙ Settings]       │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Desktop Design Details

1. **Station Header Row**
   - Colored backgrounds: Cook (red), Mid-pack (orange), Expo (green)
   - Station spans its constraints (Mid-pack spans 2 columns)

2. **Constraint Header Row**
   - Name (bold)
   - Keyboard shortcut in brackets
   - Observable signal (smaller, muted text)

3. **Data Cells**
   - Empty = dash (—) not zero (reduces visual noise)
   - Number when count > 0
   - Cell background tints on hover
   - Green flash animation on log

4. **Person Column**
   - Keyboard shortcut in brackets
   - First name only (saves space, more scannable)

---

## Mobile Layout (<768px): Card Stack

```
┌─────────────────────────────────────────┐
│  HHG AUDIT                    ⏱ 01:23   │
│  Dec 10  •  3 people  •  12 logged      │
├─────────────────────────────────────────┤
│                                         │
│  ┌─────────────────────────────────────┐│
│  │  LYDELL                         [1] ││
│  │  ┌────────┬────────┬────────┬─────┐ ││
│  │  │🔴 Low  │🟠 Too  │🟠 Split│🟢Mix│ ││
│  │  │ Stock  │ Many   │ Order  │Ordrs│ ││
│  │  │   —    │   —    │   —    │  —  │ ││
│  │  └────────┴────────┴────────┴─────┘ ││
│  └─────────────────────────────────────┘│
│                                         │
│  ┌─────────────────────────────────────┐│
│  │  ISMAEL                         [2] ││
│  │  ┌────────┬────────┬────────┬─────┐ ││
│  │  │🔴 Low  │🟠 Too  │🟠 Split│🟢Mix│ ││
│  │  │ Stock  │ Many   │ Order  │Ordrs│ ││
│  │  │   —    │   2    │   1    │  —  │ ││
│  │  └────────┴────────┴────────┴─────┘ ││
│  └─────────────────────────────────────┘│
│                                         │
│  ┌─────────────────────────────────────┐│
│  │  ANTHONY                        [3] ││
│  │  ┌────────┬────────┬────────┬─────┐ ││
│  │  │🔴 Low  │🟠 Too  │🟠 Split│🟢Mix│ ││
│  │  │ Stock  │ Many   │ Order  │Ordrs│ ││
│  │  │   —    │   —    │   —    │  1  │ ││
│  │  └────────┴────────┴────────┴─────┘ ││
│  └─────────────────────────────────────┘│
│                                         │
│  ┌─────────────────────────────────────┐│
│  │  Recent: Ismael → Too Many (2:34p)  ││
│  └─────────────────────────────────────┘│
│                                         │
│  [Export]              [Settings]       │
│                                         │
└─────────────────────────────────────────┘
```

### Mobile Design Details

1. **Cards Per Person**
   - Name prominent, keyboard shortcut right-aligned
   - 4 constraint cells in a row within each card
   - Each cell shows colored dot + abbreviated name + count
   - Minimum 44px touch targets

2. **Abbreviated Names (Mobile Only)**
   - Low Stock → "Low Stock" (fits)
   - Too Many → "Too Many" (fits)
   - Split Order → "Split" 
   - Mixed Orders → "Mixed"

3. **Header**
   - Compact single line
   - Date, shift count, log count, timer

4. **Controls**
   - Bottom-anchored for thumb reach
   - Two primary buttons only

---

## CSS Implementation

```css
/* Station Colors */
:root {
    --station-cook: #ef4444;
    --station-cook-bg: rgba(239, 68, 68, 0.1);
    --station-midpack: #f97316;
    --station-midpack-bg: rgba(249, 115, 22, 0.1);
    --station-expo: #22c55e;
    --station-expo-bg: rgba(34, 197, 94, 0.1);
}

/* Responsive Breakpoint */
@media (max-width: 767px) {
    .desktop-table { display: none; }
    .mobile-cards { display: block; }
}

@media (min-width: 768px) {
    .desktop-table { display: block; }
    .mobile-cards { display: none; }
}

/* Touch Targets */
.cell, .card-cell {
    min-height: 44px;
    min-width: 44px;
}

/* Empty State */
.cell-empty {
    color: var(--text-muted);
}

/* Active Count */
.cell-active {
    font-weight: bold;
    color: var(--text-primary);
}

/* Station Header */
.station-header-cook { 
    background: var(--station-cook-bg);
    border-top: 3px solid var(--station-cook);
}
.station-header-midpack { 
    background: var(--station-midpack-bg);
    border-top: 3px solid var(--station-midpack);
}
.station-header-expo { 
    background: var(--station-expo-bg);
    border-top: 3px solid var(--station-expo);
}
```

---

## JavaScript Changes

### Update renderMatrix() 

Create two render functions:

```javascript
function renderMatrix() {
    LOG.enter('renderMatrix');
    
    if (window.innerWidth >= 768) {
        renderDesktopTable();
    } else {
        renderMobileCards();
    }
    
    LOG.exit('renderMatrix');
}

// Re-render on resize
window.addEventListener('resize', debounce(renderMatrix, 250));
```

### renderDesktopTable()

```javascript
function renderDesktopTable() {
    LOG.enter('renderDesktopTable');
    
    const container = document.getElementById('matrixContainer');
    const shiftTeam = getShiftTeam();
    
    let html = `
        <table class="audit-table desktop-table">
            <thead>
                <!-- Station Header Row -->
                <tr class="station-row">
                    <th></th>
                    <th class="station-header-cook">🔴 COOK</th>
                    <th colspan="2" class="station-header-midpack">🟠 MID-PACK</th>
                    <th class="station-header-expo">🟢 EXPO</th>
                </tr>
                <!-- Constraint Header Row -->
                <tr class="constraint-row">
                    <th></th>
                    ${CONSTRAINTS.map(c => `
                        <th class="constraint-header">
                            <div class="constraint-name">${c.name}</div>
                            <div class="constraint-key">[${c.key.toUpperCase()}]</div>
                            <div class="constraint-signal">${c.signal}</div>
                        </th>
                    `).join('')}
                </tr>
            </thead>
            <tbody>
                ${shiftTeam.map((person, displayIndex) => {
                    const actualIndex = state.shiftEmployees[displayIndex];
                    const keyHint = getPersonKeyHint(displayIndex);
                    return `
                        <tr>
                            <td class="person-cell">
                                <span class="key-hint">[${keyHint}]</span>
                                <span class="person-name">${person.split(' ')[0]}</span>
                            </td>
                            ${CONSTRAINTS.map((c, cIdx) => {
                                const count = getCount(person, c.id);
                                return `
                                    <td class="cell ${count > 0 ? 'cell-active' : 'cell-empty'}"
                                        id="cell-${actualIndex}-${c.id}"
                                        onclick="handleCellClick(${actualIndex}, ${cIdx})">
                                        ${count > 0 ? count : '—'}
                                    </td>
                                `;
                            }).join('')}
                        </tr>
                    `;
                }).join('')}
            </tbody>
        </table>
    `;
    
    container.innerHTML = html;
    LOG.exit('renderDesktopTable');
}
```

### renderMobileCards()

```javascript
function renderMobileCards() {
    LOG.enter('renderMobileCards');
    
    const container = document.getElementById('matrixContainer');
    const shiftTeam = getShiftTeam();
    
    let html = `<div class="mobile-cards">`;
    
    shiftTeam.forEach((person, displayIndex) => {
        const actualIndex = state.shiftEmployees[displayIndex];
        const keyHint = getPersonKeyHint(displayIndex);
        const firstName = person.split(' ')[0].toUpperCase();
        
        html += `
            <div class="person-card">
                <div class="card-header">
                    <span class="card-name">${firstName}</span>
                    <span class="card-key">[${keyHint}]</span>
                </div>
                <div class="card-cells">
                    ${CONSTRAINTS.map((c, cIdx) => {
                        const count = getCount(person, c.id);
                        const shortName = getShortName(c.name);
                        return `
                            <div class="card-cell" 
                                 style="border-top-color: ${c.color}"
                                 id="cell-${actualIndex}-${c.id}"
                                 onclick="handleCellClick(${actualIndex}, ${cIdx})">
                                <div class="card-cell-dot" style="background: ${c.color}"></div>
                                <div class="card-cell-name">${shortName}</div>
                                <div class="card-cell-count ${count > 0 ? 'active' : ''}">${count > 0 ? count : '—'}</div>
                            </div>
                        `;
                    }).join('')}
                </div>
            </div>
        `;
    });
    
    html += `</div>`;
    container.innerHTML = html;
    LOG.exit('renderMobileCards');
}

function getShortName(name) {
    const shorts = {
        'Low Stock': 'Low Stock',
        'Too Many': 'Too Many',
        'Split Order': 'Split',
        'Mixed Orders': 'Mixed'
    };
    return shorts[name] || name;
}
```

---

## HTML Structure Update

Replace current matrix container with:

```html
<div id="matrixContainer">
    <!-- Rendered by JS: desktop-table or mobile-cards -->
</div>
```

---

## Notion Property Updates

Update property names in Notion export:

| Old Property | New Property |
|--------------|--------------|
| Buffer | Low Stock |
| Staging | Too Many |
| Docking | Split Order |
| Focus | Mixed Orders |

Update `createNotionRow()` to use new property names.

**Note:** If Notion database already exists with old names, either:
1. Manually rename properties in Notion, OR
2. Create new database with setup-notion.py (update property names in script first)

---

## Verification Checklist

After update:
- [ ] Desktop (≥768px) shows table layout with station headers
- [ ] Mobile (<768px) shows card layout
- [ ] Resize browser switches between layouts
- [ ] Station colors visible (Cook=red, Mid-pack=orange, Expo=green)
- [ ] Constraint names updated (Low Stock, Too Many, Split Order, Mixed Orders)
- [ ] Observable signals shown under constraint names (desktop)
- [ ] All cells clickable with 44px minimum touch target
- [ ] Empty cells show "—" not "0"
- [ ] Keyboard shortcuts still work
- [ ] Export to Notion uses new property names
- [ ] All new functions have LOG.enter/LOG.exit/LOG.error

---

## Execute

Update `hhg-skill-audit.html` with this responsive redesign. This is a significant refactor—replace the matrix rendering entirely with the new dual-layout system.
