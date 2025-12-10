# UPDATE: Remove Notion Token from HTML (Security Fix)

## Context

The Notion token was exposed in the public GitHub repo. Token has been moved to the Cloudflare Worker. HTML no longer needs to send the Authorization header.

---

## Changes Required

### 1. Remove NOTION_TOKEN constant

Find and DELETE any line like:
```javascript
const NOTION_TOKEN = 'ntn_...';
```

Or replace with a comment:
```javascript
// Token removed - now stored securely in Cloudflare Worker
```

### 2. Update `createNotionRow` function

Remove the Authorization header from the fetch call:

```javascript
// BEFORE
const response = await fetch(NOTION_PROXY, {
    method: 'POST',
    headers: {
        'Authorization': `Bearer ${NOTION_TOKEN}`,  // ← REMOVE THIS LINE
        'Notion-Version': '2022-06-28',
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(requestBody)
});

// AFTER
const response = await fetch(NOTION_PROXY, {
    method: 'POST',
    headers: {
        'Notion-Version': '2022-06-28',
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(requestBody)
});
```

### 3. Remove token from Settings panel (if present)

If there's a Notion Token input field in Settings, remove it. Token is now managed in the Cloudflare Worker, not the app.

---

## Summary

| Item | Action |
|------|--------|
| `NOTION_TOKEN` constant | DELETE |
| `Authorization` header in fetch | DELETE |
| Token input in Settings | DELETE (if exists) |

---

## Verification

After update:
- [ ] No `ntn_` string anywhere in the HTML file
- [ ] Search for "secret" or "token" returns nothing sensitive
- [ ] Export still works (worker handles auth)

---

## Execute

Update `hhg-skill-audit.html` to remove all traces of the Notion token.
