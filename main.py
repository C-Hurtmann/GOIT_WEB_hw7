import argparse
from datetime import datetime
from sys import modules
from sqlalchemy import inspect
from pprint import pprint

from src.seeds import postgres_session as session
from src.models import Grade, Student, Subject, Teacher, Group


def gather_fields(namespace):
    Model = getattr(modules[__name__], namespace.model)  # find Model by argument
    needed_fields = [i.key for i in inspect(Model).mapper.column_attrs]
    result = {k: v for k, v in vars(namespace).items() if k in needed_fields and v}
    return Model, result


def create(namespace):
    Model, field_map = gather_fields(namespace)
    if not field_map.get("id"):
        last_id = session.query(Model).order_by(Model.id.desc()).first().id
        field_map.update({"id": last_id + 1})
    session.add(Model(**field_map))
    session.commit()
    print(f"New row in {Model.__tablename__} created with {field_map}")


def read(namespace):
    Model, keys = gather_fields(namespace)
    query = session.query(Model).filter_by(**keys).all()
    for i in query:
        result = i.__dict__
        del result["_sa_instance_state"]
        pprint(i.__dict__)


def update(namespace):
    Model, keys = gather_fields(namespace)
    try:
        id = keys.pop("id")
    except:
        print("This action seach only by id")
    else:
        session.query(Model).filter(Model.id == id).update(keys)
        session.commit()
        print(f"{Model} row with {id} updated with {keys}")


def delete(namespace):
    Model, keys = gather_fields(namespace)
    try:
        id = keys.pop("id")
    except:
        print("This action seach only by id")
    else:
        row = session.get(Model, id)
        session.delete(row)
        session.commit()
        print(f"{row} row with id {id} was deleted from {Model}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-a", "--action")
    parser.add_argument("-m", "--model")
    parser.add_argument("-i", "--id", type=int)
    parser.add_argument("-n", "--fullname", type=str)
    parser.add_argument("-t", "--title", type=str)
    parser.add_argument("-b", "--birthday", type=datetime)
    parser.add_argument("-p", "--phone", type=str)
    parser.add_argument("-e", "--email", type=str)
    parser.add_argument("-g", "--grade", type=int)
    parser.add_argument("-d", "--date", type=datetime)
    parser.add_argument("-gi", "--group_id", type=int)
    parser.add_argument("-ti", "--teacher_id", type=int)
    parser.add_argument("-sti", "--student_id", type=int)
    parser.add_argument("-sui", "--subject_id", type=int)

    args = parser.parse_args()
    action = getattr(modules[__name__], args.action)
    action(args)