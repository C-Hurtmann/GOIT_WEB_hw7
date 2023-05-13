from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


engine = create_engine("postgresql+psycopg2://czagorodnyi:Szk6zynbGNWtPT%40@localhost:5432/postgres")
DBSession = sessionmaker(bind=engine)
session = DBSession()

Base = declarative_base()


class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True)
    title = Column(String(10), nullable=False, unique=True)

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    fullname = Column(String(100), nullable=False)
    birthday = Column(Date)
    phone = Column(String(12))
    email = Column(String(20))
    group_id = Column(Integer, ForeignKey('groups.id'))
    group = relationship(Group)

class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True)
    fullname = Column(String(100), nullable=False, unique=True)

class Subject(Base):
    __tablename__ = "subjects"
    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    teacher_id = Column(Integer, ForeignKey('teachers.id'))
    teacher = relationship(Teacher)

class Grade(Base):
    __tablename__ = "grades"
    id = Column(Integer, primary_key=True)
    grade = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    student_id = Column(Integer, ForeignKey('students.id'))
    subject_id = Column(Integer, ForeignKey('subjects.id'))
    student = relationship(Student)
    subject = relationship(Subject)
    

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
Base.metadata.bind = engine

test_group = Group(title='Alpha')

session.add(test_group)
session.commit()

test_student = Student(fullname='Jane Dou', group_id=1)

session.add(test_student)
session.commit()