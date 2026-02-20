import bcrypt
from database import get_connection


# ================= REGISTER =================


def register(username, password):

    username = username.strip()
    password = password.strip()

    # ---------- BACKEND VALIDATION ----------
    if not username or not password:
        return False, "Bitte alle Felder ausfüllen."

    if len(username) < 3:
        return False, "Username muss mindestens 3 Zeichen haben."

    if len(password) < 6:
        return False, "Passwort muss mindestens 6 Zeichen haben."

    conn = get_connection()
    c = conn.cursor()

    # Check if username already exists
    c.execute("SELECT id FROM users WHERE username=?", (username,))
    if c.fetchone():
        conn.close()
        return False, "Username existiert bereits."

    # Hash password
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    try:
        c.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hashed),
        )
        conn.commit()
        return True, "Erfolgreich registriert."
    except Exception as e:
        return False, "Registrierung fehlgeschlagen."
    finally:
        conn.close()


# ================= LOGIN =================


def login(username, password):

    username = username.strip()
    password = password.strip()

    if not username or not password:
        return None

    conn = get_connection()
    c = conn.cursor()

    c.execute("SELECT id, password FROM users WHERE username=?", (username,))
    user = c.fetchone()

    conn.close()

    if user:
        user_id, hashed_pw = user
        if bcrypt.checkpw(password.encode("utf-8"), hashed_pw):
            return user_id

    return None
