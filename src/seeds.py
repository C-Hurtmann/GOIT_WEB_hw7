from sqlite3 import connect, Row
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

from src.models import Group, Student, Subject, Teacher, Grade

TABLES = ["groups", "students", "teachers", "subjects", "grades"]
TABLE_MAP = {
    "groups": Group,
    "students": Student,
    "subjects": Subject,
    "teachers": Teacher,
    "grades": Grade,
}

sqlite = create_engine("sqlite:////home/czagorodnyi/git/homeworks/GOIT_WEB_hw6/main.db")
postgres = create_engine(
    "postgresql+psycopg2://czagorodnyi:Szk6zynbGNWtPT%40@localhost:5432/postgres"
)

SQLiteSession = sessionmaker(bind=sqlite)
sqlite_session = SQLiteSession()

PostgresSession = sessionmaker(bind=postgres)
postgres_session = PostgresSession()


def fetch_from_sqlite(table):
    with connect("/home/czagorodnyi/git/homeworks/GOIT_WEB_hw6/main.db") as con:
        con.row_factory = Row
        cur = con.cursor()
        cur.execute(f"SELECT * FROM {table};")
        result = cur.fetchall()
        return [dict(row) for row in result]


def commit_to_postgres(table, data):
    obj_list = []
    for item in data:
        obj = TABLE_MAP[table](**item)
        obj_list.append(obj)
    postgres_session.add_all(obj_list)
    postgres_session.commit()
    print(f"{table} filled")


if __name__ == "__main__":
    #    for table in [TABLES]:
    #        data = fetch_from_sqlite(table)
    #        commit_to_postgres(table, data)
    t = Teacher(fullname="Bob")
    postgres_session.add(t)
    postgres_session.commit()
