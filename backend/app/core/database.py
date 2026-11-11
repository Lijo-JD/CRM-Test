import pymysql

from app.core.config import settings


def get_connection():
    return pymysql.connect(
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        database=settings.DB_NAME,
        charset="utf8mb4",
        autocommit=True,
        cursorclass=pymysql.cursors.DictCursor,
    )


def fetch_all(query: str, params=None):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params or ())
            return cursor.fetchall()


def fetch_one(query: str, params=None):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params or ())
            return cursor.fetchone()


def execute(query: str, params=None):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params or ())
            if query.strip().lower().startswith("select"):
                return cursor.fetchall()
            conn.commit()
            return {"status": "success"}
