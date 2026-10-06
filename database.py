import sqlite3
from pathlib import Path

DB_DIR = Path("data")
DB_PATH = DB_DIR / "stylemind.db"


def get_connection():
    DB_DIR.mkdir(exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_db():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            preferred_colors TEXT,
            favorite_styles TEXT,
            disliked_styles TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS wardrobe (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name TEXT NOT NULL,
            clothing_type TEXT,
            color TEXT,
            pattern TEXT,
            material TEXT,
            style TEXT,
            season TEXT,
            formality TEXT,
            image_path TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS outfits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            occasion TEXT,
            outfit TEXT,
            reason TEXT,
            feedback TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    
    """)
        # Add Stage 4 AI analysis columns
    cursor.execute("PRAGMA table_info(wardrobe)")
    existing_columns = [column[1] for column in cursor.fetchall()]

    if "matching_colors" not in existing_columns:
        cursor.execute(
            "ALTER TABLE wardrobe ADD COLUMN matching_colors TEXT"
        )

    if "analysis_confidence" not in existing_columns:
        cursor.execute(
            "ALTER TABLE wardrobe ADD COLUMN analysis_confidence TEXT"
        )

    if "analysis_notes" not in existing_columns:
        cursor.execute(
            "ALTER TABLE wardrobe ADD COLUMN analysis_notes TEXT"
        )

    connection.commit()
    connection.close()


def create_user(name, preferred_colors, favorite_styles, disliked_styles):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO users (
            name,
            preferred_colors,
            favorite_styles,
            disliked_styles
        )
        VALUES (?, ?, ?, ?)
    """, (
        name,
        ", ".join(preferred_colors),
        ", ".join(favorite_styles),
        ", ".join(disliked_styles)
    ))

    user_id = cursor.lastrowid
    connection.commit()
    connection.close()

    return user_id


def get_user():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, preferred_colors, favorite_styles, disliked_styles
        FROM users
        ORDER BY id DESC
        LIMIT 1
    """)

    user = cursor.fetchone()
    connection.close()
    return user


def add_wardrobe_item(
    user_id,
    name,
    clothing_type,
    color,
    pattern,
    material,
    style,
    season,
    formality,
    image_path,
    matching_colors="",
    analysis_confidence="",
    analysis_notes=""
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO wardrobe (
            user_id,
            name,
            clothing_type,
            color,
            pattern,
            material,
            style,
            season,
            formality,
            image_path,
            matching_colors,
            analysis_confidence,
            analysis_notes
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?,?,?)
    """, (
        user_id,
        name,
        clothing_type,
        color,
        pattern,
        material,
        style,
        season,
        formality,
        image_path,
        matching_colors,
        analysis_confidence,
        analysis_notes
    ))

    item_id = cursor.lastrowid
    connection.commit()
    connection.close()

    return item_id


def get_wardrobe_items(user_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            name,
            clothing_type,
            color,
            pattern,
            material,
            style,
            season,
            formality,
            image_path,
            created_at
        FROM wardrobe
        WHERE user_id = ?
        ORDER BY id DESC
    """, (user_id,))

    items = cursor.fetchall()
    connection.close()

    return items


def delete_wardrobe_item(item_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM wardrobe WHERE id = ?",
        (item_id,)
    )

    connection.commit()
    connection.close()


init_db()
