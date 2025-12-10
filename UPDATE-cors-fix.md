# UPDATE: Fix CORS + Reduce Console Noise

## Context

Two issues to fix:
1. **CORS Error**: Notion API blocks browser requests. Route through Cloudflare Worker proxy.
2. **Console Noise**: Session timer logs every second, cluttering console.

---

## Fix 1: Use Cloudflare Worker Proxy

### Proxy URL (Hardcoded)

```javascript
const NOTION_PROXY = 'https://muddy-credit-47c7.ladiossato.workers.dev';
```

### Update `createNotionRow` function

Find the fetch call to Notion API and change the URL:

```javascript
// BEFORE
const response = await fetch('https://api.notion.com/v1/pages', {
    method: 'POST',
    headers: {
        'Authorization': `Bearer ${NOTION_TOKEN}`,
        'Notion-Version': '2022-06-28',
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(requestBody)
});

// AFTER
const NOTION_PROXY = 'https://muddy-credit-47c7.ladiossato.workers.dev';

const response = await fetch(NOTION_PROXY, {
    method: 'POST',
    headers: {
        'Authorization': `Bearer ${NOTION_TOKEN}`,
        'Notion-Version': '2022-06-28',
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(requestBody)
});
```

**That's it.** No settings UI needed—proxy URL is hardcoded.

---

## Fix 2: Remove Session Timer Logging

### Find `updateSessionTimer` function

Remove LOG.enter and LOG.exit calls:

```javascript
// BEFORE
function updateSessionTimer() {
    LOG.enter('updateSessionTimer');
    const elapsed = Date.now() - state.sessionStart;
    const result = formatTime(elapsed);
    document.getElementById('sessionTime').textContent = result;
    LOG.exit('updateSessionTimer');
}

// AFTER
function updateSessionTimer() {
    // No logging - runs every second, creates noise
    const elapsed = Date.now() - state.sessionStart;
    document.getElementById('sessionTime').textContent = formatTime(elapsed, true);
}
```

### Update `formatTime` to support silent mode

```javascript
// BEFORE
function formatTime(ms) {
    LOG.enter('formatTime', { ms });
    const hours = Math.floor(ms / 3600000);
    const mins = Math.floor((ms % 3600000) / 60000);
    const secs = Math.floor((ms % 60000) / 1000);
    const result = `${hours.toString().padStart(2, '0')}:${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    LOG.exit('formatTime', result);
    return result;
}

// AFTER
function formatTime(ms, silent = false) {
    if (!silent) LOG.enter('formatTime', { ms });
    const hours = Math.floor(ms / 3600000);
    const mins = Math.floor((ms % 3600000) / 60000);
    const secs = Math.floor((ms % 60000) / 1000);
    const result = `${hours.toString().padStart(2, '0')}:${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    if (!silent) LOG.exit('formatTime', result);
    return result;
}
```

---

## Summary of Changes

| Location | Change |
|----------|--------|
| `createNotionRow()` | Change URL from `https://api.notion.com/v1/pages` to `https://muddy-credit-47c7.ladiossato.workers.dev` |
| `updateSessionTimer()` | Remove LOG.enter and LOG.exit |
| `formatTime()` | Add `silent` parameter, call with `true` from timer |

---

## Verification

After update:
- [ ] Export to Notion works (no CORS error)
- [ ] Console no longer logs every second
- [ ] Network tab shows requests going to `muddy-credit-47c7.ladiossato.workers.dev`

---

## Execute

Update `hhg-skill-audit.html` with these two fixes. Modify existing file—do not rebuild.
