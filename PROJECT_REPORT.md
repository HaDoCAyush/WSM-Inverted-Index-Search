# PROJECT REPORT
## Design and Implementation of a Modular Inverted Index Search Engine

**Subject:** Web Search and Mining (WSM)  
**Project Title:** IndexLab — Document Search using an Inverted Index  
**Submitted by:** Ayush Gupta  
**Student ID:** B124025  
**Branch:** CSEA  
**Technology Stack:** Python, Flask, HTML5, CSS3, JavaScript  
**Project Type:** Academic / Educational Web Application

---

## 1. Abstract

The project implements a small document retrieval system that demonstrates the fundamental architecture of a text search engine. A user enters a word, a multi-word expression, or a wildcard pattern in a browser-based interface. The backend processes the query and consults an in-memory inverted index to identify relevant documents. Results are returned through a JSON API and displayed in a read-only result panel.

The implementation is deliberately divided into independent modules: document loading, tokenization, text normalization and case folding, inverted-index construction, query processing, wildcard processing, and the frontend graphical user interface. This separation makes the program easier to understand, test, maintain, and extend.

The sample collection contains text documents covering information retrieval, data structures, computer networks, database systems, artificial intelligence, web development, and algorithms. The system supports case-insensitive retrieval, implicit AND queries, explicit AND and OR operators, and the `*` and `?` wildcard symbols.

## 2. Introduction

A search system helps users locate information in a collection without reading every document manually. A naïve implementation could scan every file for every query. This approach becomes inefficient as the number and size of documents grow.

Information retrieval systems commonly preprocess documents and build an index before users search. An **inverted index** stores a mapping from each term to the documents containing that term. When a query arrives, the search engine looks up the query terms in the index and combines their document lists. This avoids repeatedly scanning all document text.

This project presents the idea through a compact web application. Flask provides the backend HTTP routes, while HTML, CSS, and JavaScript provide the user interface.

## 3. Problem Statement

To design and implement a modular search application that:
1. Loads a collection of text documents from a folder.
2. Extracts tokens from document contents.
3. Normalizes tokens and performs case folding.
4. Builds an inverted index for efficient term lookup.
5. Processes user queries and retrieves matching documents.
6. Supports wildcard expansion for partial-term searching.
7. Provides a graphical interface containing a search input, Search button, and read-only result area.

## 4. Objectives

- Demonstrate the document preprocessing pipeline used in information retrieval.
- Implement an inverted index using a dictionary-based data structure.
- Make searches independent of uppercase/lowercase differences.
- Support multi-term Boolean retrieval using AND and OR.
- Add wildcard matching with `*` and `?`.
- Separate business logic from the web interface.
- Provide sample documents, automated tests, and deployment configuration.
- Create a project that can be version-controlled and shared through GitHub.

## 5. Scope and Assumptions

The current system is an educational prototype. It indexes UTF-8 plain-text `.txt` files located in `data/documents/`, including nested folders. The index is created when the Flask application starts and remains in memory while the process runs.

The query language supports one Boolean operator type per query. If no operator is supplied, multiple terms are combined using AND. Parentheses, quoted phrase queries, proximity operators, stemming, stop-word removal, PDF parsing, and user file uploads are not part of this version.

## 6. Technologies Used

| Technology | Purpose |
|---|---|
| Python 3.10+ | Backend language and search algorithms |
| Flask | HTTP routing and JSON API |
| HTML5 | Semantic page structure |
| CSS3 | Responsive visual design |
| JavaScript | Form interaction and asynchronous API requests |
| Regular expressions | Token extraction and wildcard matching |
| Python dictionaries and sets | Inverted index and Boolean set operations |
| unittest | Automated verification |
| Gunicorn | Production WSGI server |

Flask was selected because it is a lightweight Python web framework and can be organized with an application factory. Python's standard library supplies Unicode normalization, regular expressions, filesystem paths, and testing support.

## 7. System Architecture

### 7.1 High-level architecture

```text
             DOCUMENT COLLECTION
             data/documents/*.txt
                      |
                      v
              DOCUMENT LOADER
                      |
                      v
                 TOKENIZER
                      |
                      v
          NORMALIZATION / CASE FOLDING
                      |
                      v
              INVERTED INDEX
                      |
          +-----------+------------+
          |                        |
          v                        v
    WILDCARD PROCESSOR       QUERY PROCESSOR
          |                        |
          +-----------+------------+
                      |
                      v
                SEARCH RESULTS
                      |
                      v
             FLASK JSON API
                      |
                      v
              FRONTEND GUI
       Search input / Search button
             Read-only results
```

### 7.2 Folder structure

```text
WSM_Inverted_Index_Search_Engine/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── modules/
│   │   ├── __init__.py
│   │   ├── document_loader.py
│   │   ├── tokenizer.py
│   │   ├── normalizer.py
│   │   ├── inverted_index.py
│   │   ├── query_processor.py
│   │   └── wildcard_processor.py
│   ├── templates/
│   │   └── index.html
│   └── static/
│       ├── css/style.css
│       └── js/app.js
├── data/documents/
├── tests/
├── PROJECT_REPORT.md
├── README.md
├── requirements.txt
├── run.py
├── wsgi.py
└── render.yaml
```

## 8. Module Description and Implementation

### 8.1 Document Loading Module — `document_loader.py`

**Purpose:** Read the source document collection and provide document identifiers with their text.

The `load_documents()` function:
- Accepts a directory path.
- Creates the directory if it does not exist.
- Recursively discovers `.txt` files.
- Reads files using UTF-8, tolerating a byte-order mark and replacing invalid byte sequences.
- Uses a relative path as the document identifier.
- Skips files that cannot be read.

**Input:** A directory containing text documents.  
**Output:** A dictionary in the form `{document_id: document_text}`.

Using relative paths keeps document identifiers stable and avoids exposing absolute server paths in search results.

### 8.2 Tokenization Module — `tokenizer.py`

**Purpose:** Divide text into searchable word tokens.

Tokenization converts a continuous character sequence into individual terms. The implementation uses a Unicode-aware regular expression. It accepts letters and numbers, and permits apostrophes inside a word. Punctuation and whitespace act as separators.

For example:

```text
Input:  "Search Engines, DATA structures!"
Tokens: ["search", "engines", "data", "structures"]
```

Each extracted token is passed through the normalization function so that document terms and query terms use the same representation.

### 8.3 Text Normalization and Case Folding — `normalizer.py`

**Purpose:** Ensure equivalent text forms are represented consistently.

The `normalize_text()` function applies Unicode NFKC normalization, converts typographic apostrophes to a standard apostrophe, and calls Python's Unicode-aware `casefold()` method.

Case folding is more comprehensive than ordinary lowercase conversion for some Unicode characters. For example, the German character `ß` case-folds to `ss`.

Example:

```text
"INFORMATION"  -> "information"
"Information"  -> "information"
"Straße"       -> "strasse"
```

Normalization is applied to both documents and query terms. This is essential: an index built with one normalization policy cannot reliably answer queries processed with a different policy.

### 8.4 Inverted Index Construction — `inverted_index.py`

**Purpose:** Build a term-to-document mapping for efficient retrieval.

The index uses a nested dictionary:

```python
postings[term][document_id] = [position_1, position_2, ...]
```

Example:

```text
Document: "data search data"
Posting:
  data   -> {document.txt: [0, 2]}
  search -> {document.txt: [1]}
```

The index stores:
- **Vocabulary:** the set of unique normalized terms.
- **Postings:** documents containing each term and the token positions.
- **Term frequency:** the number of times a term occurs in a document.
- **Document collection:** the original text used for previews.

The positional information is useful for future extensions such as phrase searching. In this version it is also used to calculate term frequency.

### 8.5 Query Processing — `query_processor.py`

**Purpose:** Interpret a query and combine matching document sets.

The query processor supports:
- A single term.
- Multiple terms with implicit AND.
- Explicit `AND`.
- Explicit `OR`.
- Wildcard terms as part of a query.

For AND, the result is the intersection of the posting document sets:

\[
R_{AND}=D_1 \cap D_2 \cap \dots \cap D_n
\]

For OR, the result is the union:

\[
R_{OR}=D_1 \cup D_2 \cup \dots \cup D_n
\]

The processor ranks the matching documents using a simple score: the sum of the frequencies of matched expanded terms in that document. Results are sorted by descending score and then by document name.

The query parser intentionally rejects mixed AND/OR expressions instead of silently applying an ambiguous precedence rule.

### 8.6 Wildcard Processing — `wildcard_processor.py`

**Purpose:** Expand partial search terms against the index vocabulary.

Two wildcard symbols are supported:

| Symbol | Meaning | Example |
|---|---|---|
| `*` | Zero or more characters | `comput*` |
| `?` | Exactly one character | `dat?` |

The wildcard processor first normalizes the pattern. It then converts wildcard symbols into regular-expression equivalents and escapes all other characters. Matching is anchored to the complete vocabulary term. Results are sorted and capped at 100 expansions to limit unexpectedly large matches.

Examples:
- `comput*` may match `computer` and `computing`.
- `retriev?l` may match `retrieval`.
- `dat?` may match `data` or `date`, if those terms exist.

### 8.7 Frontend GUI

**Purpose:** Provide a simple and usable interface to the search engine.

The interface includes:
- A search input box.
- A Search button.
- A read-only result region.
- Example query chips.
- Index statistics: number of documents, vocabulary size, and total term occurrences.
- Result cards with document name, relevance score, matched terms, and a short preview.

JavaScript sends an asynchronous request to `/api/search`. The response is rendered into the result region. The user cannot edit the result area; it is populated by the application.

The layout uses responsive CSS so the interface adapts to mobile and desktop screens.

## 9. Search API

### `GET /api/search?q=<query>`

Example request:

```text
/api/search?q=information%20retrieval
```

Example response:

```json
{
  "query": "information retrieval",
  "count": 1,
  "message": "Results found.",
  "results": [
    {
      "document": "information_retrieval.txt",
      "score": 2,
      "matched_terms": ["information", "retrieval"],
      "preview": "Information retrieval is the process..."
    }
  ]
}
```

### `GET /api/stats`

Returns the document count, vocabulary size, and total number of indexed token occurrences.

### `GET /health`

Returns a simple health status for deployment monitoring.

## 10. Algorithm

### 10.1 Index construction

1. Read every supported text file.
2. For each document, tokenize its contents.
3. Normalize every token.
4. Enumerate tokens to obtain their positions.
5. Add each position to the term's posting list for that document.
6. Add the term to the vocabulary.
7. Repeat until all documents have been processed.

### 10.2 Query execution

1. Normalize the query.
2. Split the query into terms and identify the Boolean operator.
3. Expand wildcard terms using the vocabulary.
4. Look up the posting document set for each expanded term.
5. Combine sets using intersection for AND or union for OR.
6. Calculate a frequency-based score for each result.
7. Sort and return the results.

### 10.3 Pseudocode

```text
BUILD_INDEX(documents):
    FOR each document:
        tokens = TOKENIZE(document.text)
        FOR each token at position:
            term = NORMALIZE(token)
            INDEX[term][document.id].append(position)

SEARCH(query):
    terms, operator = PARSE(query)
    FOR each term:
        alternatives = EXPAND_WILDCARD(term, vocabulary)
        term_documents = UNION(postings for alternatives)
    IF operator is AND:
        matches = INTERSECTION(all term_documents)
    ELSE:
        matches = UNION(all term_documents)
    SCORE and SORT matches
    RETURN matches
```

## 11. Complexity Analysis

Let:
- \(T\) be the total number of tokens in the corpus.
- \(V\) be the number of unique terms in the vocabulary.
- \(P(t)\) be the number of postings for term \(t\).
- \(D\) be the number of documents.

| Operation | Approximate cost | Explanation |
|---|---:|---|
| Document loading | \(O(B)\) | B is the total number of input bytes |
| Tokenization and indexing | \(O(T)\) | Each token is processed once |
| Exact term lookup | Expected \(O(1)\) | Dictionary lookup before reading postings |
| AND / OR combination | Depends on posting sizes | Set intersection or union |
| Wildcard expansion | \(O(V)\) | Current implementation checks vocabulary terms |
| Result sorting | \(O(R \log R)\) | R is the number of matched documents |

The index requires memory proportional to the number of token occurrences because positions are retained. This is acceptable for a small educational corpus. Large-scale search systems use compressed postings, persistent indexes, distributed storage, and more advanced ranking.

## 12. Installation and Execution

### Windows

```powershell
py -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python run.py
```

Open `http://127.0.0.1:5000`.

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python run.py
```

## 13. Test Cases

The repository includes automated tests in `tests/test_search_engine.py`.

| Test ID | Test input / action | Expected result |
|---|---|---|
| TC-01 | Normalize `INFORMATION` | `information` |
| TC-02 | Tokenize `Hello, WORLD!` | `hello`, `world` |
| TC-03 | Read posting positions for `information` | Correct token positions |
| TC-04 | Search `information data` | Only documents containing both terms |
| TC-05 | Search `retrieval OR database` | Documents containing either term |
| TC-06 | Search `infor*` | Documents containing matching vocabulary terms |
| TC-07 | Expand `dat?` | Four-character matching terms |
| TC-08 | Mix AND and OR | Validation error |
| TC-09 | Open `/` | Search interface loads |
| TC-10 | Request `/api/stats` | Valid index statistics |
| TC-11 | Request `/api/search?q=information` | JSON search results |
| TC-12 | Submit an empty query | HTTP 400 validation response |

Run all tests:

```bash
python -m unittest discover -s tests -v
```

## 14. Sample Search Demonstration

Try these queries in the browser:

1. `information` — finds documents containing the term.
2. `information retrieval` — finds documents containing both terms.
3. `database OR index` — finds documents containing either term.
4. `comput*` — demonstrates prefix wildcard expansion.
5. `dat?` — demonstrates a single-character wildcard.
6. `web development` — finds documents containing both terms.

The sample corpus is intentionally varied so that different searches produce different result sets.

## 15. Deployment and GitHub Submission

### GitHub

1. Sign in to GitHub and create a new repository, for example `wsm-inverted-index-search`.
2. Extract this ZIP.
3. Upload the contents of the extracted project folder to the repository root.
4. Commit the files.
5. Copy the repository URL into the project report or submission form.

**GitHub repository URL:** `[PASTE_YOUR_GITHUB_REPOSITORY_URL_HERE](https://github.com/HaDoCAyush/WSM-Inverted-Index-Search)`

The repository URL cannot be generated until the student creates the repository under their own GitHub account.

### Hosting with Render

The included `render.yaml` defines a Python web service. Connect the GitHub repository to Render and deploy with:

- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn wsgi:app`
- Health-check path: `/health`

A production WSGI server is used instead of Flask's development server. The Flask development server is intended for local development, not public production hosting.

**Live deployment URL:** `ADD_RENDER_URL_AFTER_DEPLOYMENT`

## 16. Results and Discussion

The application demonstrates a complete small-scale retrieval workflow. The corpus is loaded and indexed at application startup. Exact terms are resolved through dictionary-based postings rather than by scanning every document for every query. Boolean set operations combine the postings, and wildcard patterns are expanded against the vocabulary.

The frontend and backend are independent layers connected through HTTP endpoints. This means the search logic can be tested without a browser, and the interface can be redesigned without rewriting the index implementation.

## 17. Limitations

- Only `.txt` files are loaded.
- The index is rebuilt at process startup and is not persisted to disk.
- Wildcard expansion scans the vocabulary and is therefore linear in vocabulary size.
- Ranking uses raw term frequency and does not account for document length or inverse document frequency.
- The query grammar does not support parentheses or mixed Boolean operators.
- Search previews show the beginning of a document rather than a dynamically selected matching sentence.
- There is no authentication or document-upload interface.

## 18. Future Enhancements

1. Add PDF and DOCX document extraction.
2. Persist the index to disk or a database.
3. Implement TF-IDF or BM25 ranking.
4. Add phrase and proximity search using stored token positions.
5. Add stemming and stop-word configuration.
6. Support parentheses and a full Boolean query parser.
7. Use a trie or finite-state structure for faster wildcard expansion.
8. Add pagination, snippets around matching terms, and highlighting.
9. Add an upload interface with file validation.
10. Add performance benchmarks for larger corpora.

## 19. Conclusion

The project successfully demonstrates the major components of a modular text search engine. The document loader, tokenizer, normalizer, inverted index, query processor, wildcard processor, and frontend GUI each have a separate responsibility. The system supports case-insensitive exact search, Boolean AND/OR retrieval, and wildcard matching.

The project is structured for maintainability and includes sample documents, tests, setup instructions, and deployment configuration. It provides a practical foundation for understanding how an information retrieval system transforms a collection of documents into an index and uses that index to answer user queries.

## 20. References

1. Flask Documentation — Application Factories: https://flask.palletsprojects.com/en/stable/patterns/appfactories/
2. Flask Documentation — Application Lifecycle: https://flask.palletsprojects.com/en/stable/lifecycle/
3. Flask Documentation — Deploying to Production: https://flask.palletsprojects.com/en/stable/deploying/
4. Python Documentation — `re` Regular Expression Operations: https://docs.python.org/3/library/re.html
5. Python Documentation — `pathlib`: https://docs.python.org/3/library/pathlib.html
6. Python Documentation — `unittest`: https://docs.python.org/3/library/unittest.html
7. Manning, Raghavan and Schütze, *Introduction to Information Retrieval*, Cambridge University Press, 2008. Online text: https://nlp.stanford.edu/IR-book/

---

**Submitted by:** Ayush Gupta  
**Student ID:** B124025  
**Branch:** CSEA
