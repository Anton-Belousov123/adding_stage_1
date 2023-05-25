import psycopg2
import os
import dotenv

dotenv.load_dotenv()


def get_element(table_name):
    conn, cur = _create_connection()
    cur.execute(f"SELECT * FROM {table_name} WHERE stage=%s", ("upload_error_by_copy",))  # Suggested
    record = cur.fetchone()
    conn.close()
    if not record: return None
    return record[0], record[1], record[11]


def change_status(table_name, element, new_status):
    print(f'Для таблицы {table_name} элемента {element[1]} установлен статус {new_status}.')
    conn, cur = _create_connection()
    cur.execute(f"UPDATE {table_name} SET stage=%s WHERE s_article=%s", (new_status, str(element[0])))
    conn.commit()
    conn.close()


def _create_connection():
    """Возвращает соединение и курсор базы данных"""
    conn = psycopg2.connect(
        host=os.getenv('DATABASE_HOST'),
        database=os.getenv('DATABASE_NAME'),
        user=os.getenv('DATABASE_LOGIN'),
        password=os.getenv('DATABASE_PASSWORD'),
    )
    cur = conn.cursor()
    return conn, cur
