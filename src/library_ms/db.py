#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================== 
Project: Library Management System 
File: db.py 
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi) 
Created: 2025-10-22 
Updated: 2025-10-22 
License: MIT License (see LICENSE file for details)
=================================================================== 

Description: 
SQLite database utilities: connection factory, schema migrations, and helpers.

Usage: 
python -c "from library_ms.db import get_connection, migrate; migrate()"

Notes: 
- The database file is created in the working directory (library.db).
- Migrations are idempotent.

===================================================================
"""
from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, Optional

DB_FILENAME = "library.db"


def get_db_path(custom_path: Optional[str] = None) -> Path:
    """Return the resolved path for the SQLite database file.

    Args:
        custom_path: Optional explicit file path. If None, uses CWD/library.db
    """
    return Path(custom_path or DB_FILENAME).resolve()


@contextmanager
def get_connection(db_path: Optional[str] = None) -> Iterator[sqlite3.Connection]:
    """Context-managed connection with pragmas for reliability.

    Yields:
        sqlite3.Connection
    """
    path = get_db_path(db_path)
    conn = sqlite3.connect(path)
    try:
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.execute("PRAGMA journal_mode = WAL;")
        conn.execute("PRAGMA synchronous = NORMAL;")
        yield conn
        conn.commit()
    finally:
        conn.close()


def migrate(db_path: Optional[str] = None) -> None:
    """Create tables if they do not exist (idempotent)."""
    with get_connection(db_path) as conn:
        cur = conn.cursor()

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                isbn TEXT UNIQUE NOT NULL,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                year INTEGER,
                total_copies INTEGER NOT NULL DEFAULT 1,
                available_copies INTEGER NOT NULL DEFAULT 1,
                created_at TEXT NOT NULL DEFAULT (datetime('now')),
                updated_at TEXT
            );
            """
        )

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE,
                phone TEXT,
                created_at TEXT NOT NULL DEFAULT (datetime('now')),
                updated_at TEXT
            );
            """
        )

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS loans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER NOT NULL,
                member_id INTEGER NOT NULL,
                loaned_at TEXT NOT NULL DEFAULT (datetime('now')),
                due_at TEXT NOT NULL,
                returned_at TEXT,
                FOREIGN KEY(book_id) REFERENCES books(id) ON DELETE CASCADE,
                FOREIGN KEY(member_id) REFERENCES members(id) ON DELETE CASCADE
            );
            """
        )

        conn.commit()
