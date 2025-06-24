def get_user(conn, account_number):
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE account_number = ?", (account_number,))
    row = cur.fetchone()
    return dict(row) if row else None

def create_user(conn, user):
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (account_number, pin, balance, full_name, address, blood_group) VALUES (?, ?, ?, ?, ?, ?)",
        (user.account_number, user.pin, user.balance, user.full_name, user.address, user.blood_group)
    )
    conn.commit()
    return user

def get_all_users(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    return [dict(row) for row in cur.fetchall()]

def get_transactions(conn, account_number):
    cur = conn.cursor()
    cur.execute("SELECT * FROM transactions WHERE account_number = ? ORDER BY timestamp DESC", (account_number,))
    return [dict(row) for row in cur.fetchall()]



# cruds means Create, Read, Update, Delete