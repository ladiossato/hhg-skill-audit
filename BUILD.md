# BUILD INSTRUCTIONS

## Step 0: Create Notion Database

Before building the HTML, create and run `setup-notion.py`:

**What the script does:**
- Creates a Notion database under the parent page
- Adds all 11 properties (see SPEC.md for schema)
- Pre-populates Team Member select with all 14 names
- Pre-populates Station select with Cook, Mid-pack, Expo, Float
- Creates formula properties for Total Misses and Miss Rate

**Execution:**
1. Create `setup-notion.py` following the schema in SPEC.md
2. Run: `python setup-notion.py`
3. Capture the database ID from output
4. Use this database ID in the HTML file

**Expected Output:**
```
SUCCESS! Database created.
Database ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

## Step 1: Read Specification
Read `SPEC.md` completely before writing any code.

## Step 2: Build
Create `hhg-skill-audit.html` following SPEC.md exactly.

## Step 3: Verify
After building, confirm:
- [ ] All 14 team members present
- [ ] All 4 constraints with correct keys (A-S-D-F)
- [ ] Notion credentials embedded
- [ ] Every function has LOG.enter/LOG.exit/LOG.error
- [ ] Keyboard shortcuts functional
- [ ] Undo (Z) works
- [ ] Export aggregates by person

## Step 4: Output
Save as `hhg-skill-audit.html`