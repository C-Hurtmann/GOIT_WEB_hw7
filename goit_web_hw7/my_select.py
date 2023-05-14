from sqlalchemy import select, func, desc

from pprint import pprint
from seeds import postgres_session as session
from models import Group, Student, Teacher, Subject, Grade


def select_1():
    query = session.execute(
        select(
            func.round(func.avg(Grade.grade), 2).label("average_grade"),
            Student.fullname,
        )
        .join(Student)
        .group_by(Student.fullname)
        .order_by(desc("average_grade"))
        .limit(5)
    )
    return [i for i in query]


def select_2():
    query = session.execute(
        select(
            func.round(func.avg(Grade.grade), 2).label("average_grade"),
            Student.fullname,
        )
        .join(Subject, Grade.subject_id == Subject.id)
        .filter(Subject.title == "Law")
        .join(Student, Grade.student_id == Student.id)
        .group_by(Student.fullname)
        .order_by(desc("average_grade"))
        .limit(1)
    )
    return list(query)


def select_3():
    query = session.execute(
        select(func.round(func.avg(Grade.grade), 2), Group.title)
        .select_from(Grade)
        .join(Student)
        .join(Group)
        .join(Subject)
        .filter(Subject.title == "Design")
        .group_by(Group.title)
    )
    return list(query)


def select_4():
    query = session.execute(select(func.round(func.avg(Grade.grade), 2)))
    return list(query)


def select_5():
    query = session.execute(
        select(Subject.title, Teacher.fullname)
        .join(Teacher)
        .filter(Teacher.fullname == "Michele Harrison")
    )
    return list(query)


def select_6():
    query = session.execute(
        select(Student.fullname, Group.title).join(Group).filter(Group.title == "Alpha")
    )
    return list(query)


def select_7():
    query = session.execute(
        select(Grade.grade, Student.fullname)
        .join(Student)
        .join(Group)
        .filter(Group.title == "Beta")
        .join(Subject)
        .filter(Subject.title == "Economics")
    )
    return list(query)


def select_8():
    query = session.execute(
        select(func.round(func.avg(Grade.grade)), Subject.title)
        .join(Subject)
        .join(Teacher)
        .filter(Teacher.fullname == "Travis Glass")
        .group_by(Subject.title)
    )
    return list(query)


def select_9():
    query = session.execute(
        select(func.count(Grade.grade).label("grades_qty"), Subject.title)
        .join(Subject)
        .filter(Student.fullname == "Michael Stein")
        .join(Student)
        .group_by(Subject.title)
        .order_by(desc("grades_qty"))
    )
    return list(query)


def select_10():
    query = session.execute(
        select(func.distinct(Subject.title))
        .select_from(Student)
        .filter(Student.fullname == "Mary Ruiz")
        .join(Grade)
        .join(Subject)
        .join(Teacher)
        .filter(Teacher.fullname == "Lisa Moody")
    )
    return list(query)


def select_11():
    query = session.execute(
        select(func.round(func.avg(Grade.grade), 2), Subject.title)
        .join(Student)
        .filter(Student.fullname == "Robert Wu")
        .join(Subject)
        .join(Teacher)
        .filter(Teacher.fullname == "Lisa Moody")
        .group_by(Subject.title)
    )
    return list(query)


def select_12():
    query = session.execute(
        select(Grade.grade, Student.fullname)
        .select_from(Grade)
        .filter(Grade.on_date == select(func.max(Grade.on_date)))
        .join(Student)
        .join(Subject)
        .filter(Subject.title == "Computer Science")
        .join(Group, Student.group_id == Group.id)
        .filter(Group.title == "Gamma")
    )
    return list(query)
