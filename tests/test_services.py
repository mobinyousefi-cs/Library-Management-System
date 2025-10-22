#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================== 
Project: Library Management System 
File: test_services.py 
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi) 
Created: 2025-10-22 
Updated: 2025-10-22 
License: MIT License (see LICENSE file for details)
=================================================================== 

Description: 
Basic unit tests for LibraryService borrow/return logic using a temp db.

Usage: 
pytest -q

Notes: 
- Not exhaustive; meant as a sanity check.

===================================================================
"""
from __future__ import annotations

from pathlib import Path
from library_ms.db import migrate, get_connection
from library_ms.repository import LibraryRepository
from library_ms.services import LibraryService
from library_ms.models import Book, Member


def _bind_temp_db(path: Path):
    # Monkeypatch db.get_db_path used inside repo connections via environment
    import importlib
    from library_ms import db as _db

    def _fake_get_db_path(custom_path=None):
        return path

    _db.get_db_path = _fake_get_db_path  # type: ignore
    importlib.reload(_db)


def test_borrow_and_return(tmp_path: Path):
    path = tmp_path / "test.db"
    _bind_temp_db(path)
    migrate(str(path))

    svc = LibraryService(LibraryRepository())

    # seed
    b_id = svc.add_book("123456789X", "Test Book", "Author", copies=2)
    m_id = svc.add_member("Alice")

    loan_id = svc.borrow_book(b_id, m_id, days=1)
    # After borrow, available should be 1
    b = next(b for b in svc.list_books() if b.id == b_id)
    assert b.available_copies == 1

    svc.return_book(loan_id)
    b = next(b for b in svc.list_books() if b.id == b_id)
    assert b.available_copies == 2
