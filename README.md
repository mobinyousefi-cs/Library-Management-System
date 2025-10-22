# Library Management System (Tkinter + SQLite)

A clean, modular **Library Management System** built with **Tkinter** for the GUI and **SQLite** for storage. Designed with a modern Python project layout (\`src/\` package, tests, CI-ready) to drop straight onto GitHub.

## Features
- Manage **Books** (add, edit, delete, search)
- Manage **Members** (add, edit, delete, search)
- **Loans** lifecycle (borrow, return, due dates, simple availability rules)
- Persistent **SQLite** database with safe migrations
- **Services/Repository** layers for testability and clean separation of concerns
- Tkinter UI with reusable widgets and lightweight theming

## Tech Stack
- Python 3.10+
- Tkinter (standard library)
- SQLite (standard library via \`sqlite3\`)
- PyTest for tests

## Project Structure
```
library-ms/
├─ README.md
├─ LICENSE
├─ .gitignore
├─ .editorconfig
├─ pyproject.toml
├─ requirements.txt
├─ src/
│  └─ library_ms/
│     ├─ __init__.py
│     ├─ main.py
│     ├─ db.py
│     ├─ models.py
│     ├─ repository.py
│     ├─ services.py
│     ├─ utils/
│     │  └─ validators.py
│     └─ ui/
│        ├─ __init__.py
│        ├─ theme.py
│        ├─ widgets.py
│        ├─ views_books.py
│        ├─ views_members.py
│        └─ views_loans.py
└─ tests/
   ├─ test_db.py
   └─ test_services.py
```

## Quick Start
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m library_ms
```
On first run, the SQLite database file (\`library.db\`) will be created in the working directory with all required tables.

## Packaging
This project uses **PEP 621** metadata via \`pyproject.toml\`.

## Running Tests
```bash
pytest -q
```

## Notes
- The UI focuses on clarity over flash; you can theme it further in \`ui/theme.py\`.
- Business rules live in \`services.py\` (e.g., preventing borrowing of an already-loaned book).

## License
This project is under the **MIT License**. See [LICENSE](LICENSE).

