# WSM — Inverted Index Search Engine

**Student:** Ayush Gupta  
**Student ID:** B124025  
**Branch:** CSEA

A modular, browser-based document search engine built with Python and Flask. It loads `.txt` documents, tokenizes and normalizes text, builds an inverted index, and supports ordinary and wildcard searches.

## Features

- Seven clearly separated modules matching the assignment requirements.
- Responsive, polished search interface with a search field, Search button, and read-only results.
- Case-insensitive search using Unicode-aware `casefold()`.
- Inverted index with document frequency and term frequency information.
- Multi-term AND search by default; `OR` can be used between terms.
- Wildcard support: `*` matches zero or more characters; `?` matches exactly one character.
- Search results show document name, matched terms, and a short text preview.
- Example corpus included in `data/documents/`.
- JSON API at `/api/search` and `/api/stats`.
- Unit tests and a production WSGI entry point.
- Ready for GitHub and deployment to Render.

## Quick start (Windows)

1. Install Python 3.10 or newer.
2. Extract this ZIP.
3. Open Command Prompt or PowerShell in the project folder.
4. Create and activate a virtual environment:

   ```powershell
   py -m venv .venv
   .venv\Scripts\activate
   ```

5. Install dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

6. Start the app:

   ```powershell
   python run.py
   ```

7. Open **http://127.0.0.1:5000** in your browser.

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python run.py
```

## Search examples

| Query | Meaning |
|---|---|
| `information` | Documents containing “information” |
| `information retrieval` | Both terms must occur (AND) |
| `index OR database` | Documents containing either term |
| `comput*` | Terms beginning with “comput” |
| `retriev?l` | One-character wildcard, e.g. “retrieval” |
| `data AND search` | Explicit AND |
| `data OR search` | Explicit OR |

Wildcard characters can be used inside a term. Wildcard matching is case-insensitive. A query cannot mix AND and OR without parentheses; parentheses are intentionally outside this project's supported query grammar.

## Add your own documents

Place UTF-8 `.txt` files in `data/documents/`. Restart the app to rebuild the index. Nested folders are also scanned. Other file types are ignored.

## Run tests

```bash
python -m unittest discover -s tests -v
```

## Deploy online (Render)

1. Create a GitHub repository and upload the contents of this project folder (not the ZIP itself).
2. On Render, choose **New → Web Service** and connect the repository.
3. Set:
   - **Runtime:** Python
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn wsgi:app`
4. Deploy. Render will provide a public URL.

The included `render.yaml` provides the same build and start commands for Blueprint-based setup. The service reads the `PORT` environment variable through Gunicorn/Render.

> GitHub stores your source code; it does not run the Flask server by itself. Use Render or another Python-capable host to publish the live application.

## Project structure

```text
WSM_Inverted_Index_Search_Engine/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── modules/
│   │   ├── document_loader.py
│   │   ├── tokenizer.py
│   │   ├── normalizer.py
│   │   ├── inverted_index.py
│   │   ├── query_processor.py
│   │   └── wildcard_processor.py
│   ├── templates/index.html
│   └── static/css/style.css, js/app.js
├── data/documents/       # sample text corpus
├── tests/
├── PROJECT_REPORT.md
├── requirements.txt
├── run.py
├── wsgi.py
└── render.yaml
```

## Architecture and request flow

1. **Document loader** reads UTF-8 text files from the corpus directory.
2. **Tokenizer** extracts word-like tokens while retaining apostrophes inside words.
3. **Normalizer** applies Unicode case folding and normalizes curly apostrophes.
4. **Inverted index** maps each normalized term to the documents and positions in which it occurs.
5. **Wildcard processor** expands `*` and `?` patterns against the vocabulary.
6. **Query processor** evaluates AND/OR groups and returns ranked document matches.
7. **Flask routes + GUI** connect the search engine to the browser and display results.

The index is built once when the application starts. The current implementation is an in-memory educational search engine; restarting the application reloads documents and rebuilds the index.

## Limitations / future improvements

- Plain-text `.txt` files only; PDF/DOCX extraction is not included.
- The complete index is held in memory and is intended for a classroom-sized corpus.
- Ranking is simple term-frequency scoring, not a full TF-IDF/BM25 implementation.
- Boolean expressions with parentheses, phrase search, stemming, stop-word removal, and live file upload are possible extensions.

## Academic note

This repository is a working educational implementation of the concepts described in the accompanying **PROJECT_REPORT.md**. Review the report, run the application, and be prepared to explain each module and the sample queries during evaluation.
