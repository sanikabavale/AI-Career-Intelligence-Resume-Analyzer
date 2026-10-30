import sqlite3, hashlib, secrets, hmac, json
from pathlib import Path
DB_PATH=Path(__file__).resolve().parents[1]/"runtime"/"career_intelligence.db"
DB_PATH.parent.mkdir(parents=True,exist_ok=True)

def connect():
    con=sqlite3.connect(DB_PATH,check_same_thread=False)
    con.row_factory=sqlite3.Row
    return con

def init_db():
    with connect() as con:
        con.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE NOT NULL, salt TEXT NOT NULL, password_hash TEXT NOT NULL, created_at TEXT DEFAULT CURRENT_TIMESTAMP)")
        con.execute("CREATE TABLE IF NOT EXISTS analyses (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, filename TEXT NOT NULL, skills_json TEXT NOT NULL, results_json TEXT NOT NULL, created_at TEXT DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY(user_id) REFERENCES users(id))")

def _hash_password(password,salt):
    return hashlib.pbkdf2_hmac("sha256",password.encode(),bytes.fromhex(salt),240000).hex()

def create_user(username,password):
    username=username.strip()
    if len(username)<3: return False,"Username किमान 3 characters असावा."
    if len(password)<8: return False,"Password किमान 8 characters असावा."
    salt=secrets.token_hex(16)
    try:
        with connect() as con: con.execute("INSERT INTO users(username,salt,password_hash) VALUES(?,?,?)",(username,salt,_hash_password(password,salt)))
        return True,"Account तयार झाला. आता login करा."
    except sqlite3.IntegrityError: return False,"हा username आधीच वापरात आहे."

def verify_user(username,password):
    with connect() as con: row=con.execute("SELECT id,salt,password_hash FROM users WHERE username=?",(username.strip(),)).fetchone()
    if not row: return None
    candidate=_hash_password(password,row["salt"])
    return row["id"] if hmac.compare_digest(candidate,row["password_hash"]) else None

def save_analysis(user_id,filename,skills,results):
    with connect() as con:
        con.execute("INSERT INTO analyses(user_id,filename,skills_json,results_json) VALUES(?,?,?,?)",(user_id,filename,json.dumps(skills),json.dumps(results)))

def get_history(user_id,limit=20):
    with connect() as con: return con.execute("SELECT id,filename,created_at,skills_json,results_json FROM analyses WHERE user_id=? ORDER BY id DESC LIMIT ?",(user_id,limit)).fetchall()

def delete_history(history_id, user_id):
    with connect() as con:
        con.execute(
            "DELETE FROM analyses WHERE id = ? AND user_id = ?",
            (history_id, user_id)
        )
