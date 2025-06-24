import sqlite3
from pathlib import Path
from typing import Generator

def get_db() -> Generator[sqlite3.Connection, None, None]:
    # Use the main atm.db in ATM_Machine directory
    db_path = Path(__file__).parent.parent / "atm.db"
    print(f"[DEBUG] FastAPI using database at: {db_path.resolve()}")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()
