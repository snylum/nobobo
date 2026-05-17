# NOBOBO Politician Data

This folder contains the politician data used by the NOBOBO chatbot.

## Folder Structure

```
data/
└── ELEKSYON 2028/
    ├── Presidential Candidates/
    │   ├── DUTERTE.txt
    │   ├── MARCOS.txt
    │   └── (add more .txt files here)
    ├── Vice Presidential Candidates/
    │   ├── SARA.txt
    │   └── (add more .txt files here)
    └── (add more categories as folders)
```

## How to Add a New Candidate

1. Go to the correct election folder (e.g. `ELEKSYON 2028`)
2. Go to the correct category folder (e.g. `Presidential Candidates`)
3. Click **Add file → Create new file**
4. Name it `LASTNAME.txt` or `FULLNAME.txt` (all caps recommended)
5. Paste the candidate's information using the template below
6. Click **Commit changes**

The chatbot will automatically load the new file on next startup.

## Suggested Template for Each .txt File

```
Full Name:
Position Running For:
Current/Previous Position:
Party:

--- BACKGROUND ---
Born:
Education:
Profession:

--- TRACK RECORD ---
-
-

--- BILLS / LEGISLATION ---
-
-

--- CAMPAIGN DONORS ---
(from COMELEC records)

--- SALN ---
(latest filing)

--- CONTROVERSIES / PUBLIC RECORD ---
-

--- SOURCES ---
-
```

## Notes
- Keep information factual and sourced
- Do not editorialize or express opinions
- Always cite your source at the bottom
- You can add more category folders anytime (e.g. "Senatorial Candidates", "Local Candidates")
