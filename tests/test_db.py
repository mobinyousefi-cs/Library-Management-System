#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================== 
Project: Library Management System 
File: test_db.py 
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi-cs) 
Created: 2025-10-22 
Updated: 2025-10-22 
License: MIT License (see LICENSE file for details)
=================================================================== 

Description: 
Smoke tests for database migration and connectivity.

Usage: 
pytest -q

Notes: 
- Uses an in-temp db file by monkeypatching the DB filename env.

===================================================================
"""
from __future__ import annotations

from pathlib import Path
from library_ms import db


def test_migrate_creates_db(tmp_path: Path):
    path = tmp_path / "test.db"
    db.migrate(str(path))
    assert path.exists()
    with db.get_connection(str(path)) as conn:
        cur = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='books';")
        assert cur.fetchone() is not None
