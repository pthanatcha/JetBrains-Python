# Write your code here
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()

class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task, self.deadline

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

in_list = True

def today_task():
    today = datetime.today()
    print('Today {} {}'.format(today.day, today.strftime('%b')))
    if not session.query(Table).filter(Table.deadline == today).all():
        print('Nothing to do!')
    else:
        count = 0
        for index, value in enumerate(session.query(Table).filter(Table.deadline == today).all()):
            print("{0}. {1}".format(count, value))
            count += 1

def add_task():
    print('Enter task ')
    new_task = input()
    print('Enter deadline ')
    new_deadline_str = input()
    new_deadline = datetime.strptime(new_deadline_str, '%Y-%m-%d').date()
    new_row = Table(task=new_task, deadline=new_deadline)
    session.add(new_row)
    session.commit()
    print('The task has been added!')

def week_task():
    today = datetime.today()
    weekday = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    timedelta_index = 0
    while timedelta_index < 7:
        date = today + timedelta(days=timedelta_index)
        print(f"{weekday[date.weekday()]} {date.day} {date.strftime('%b')}:")
        if not session.query(Table).filter(Table.deadline == date.date()).all():
            print('Nothing to do!\n')
        else:
            for index, value in enumerate(session.query(Table.task).filter(Table.deadline == date.date()).all()):
                print(str(index + 1) + '. ' + value[0])
            print()
        timedelta_index += 1

def all_task():
    print('All tasks: ')
    for index, task_date in enumerate(session.query(Table.task, Table.deadline).all()):
        print(f"{index + 1}. {task_date[0]}. {task_date[1].day} {task_date[1].strftime('%b')}")

def missed_task():
    print('Missed tasks:')
    if not session.query(Table).filter(Table.deadline < datetime.today()).all():
        print('Nothing is missed!')
    else:
        for index, task_date in enumerate(session.query(Table.task, Table.deadline).filter(
                Table.deadline < datetime.today()).order_by(Table.deadline)):
            print(f"{index + 1}. {task_date[0]}. {task_date[1].day} {task_date[1].strftime('%b')}")

def del_task():
    if not session.query(Table).all():
        print('Nothing to delete')
    else:
        print('Chose the number of the task you want to delete: ')
        for index, task_date in enumerate(session.query(Table.task, Table.deadline).order_by(Table.deadline)):
            print(f"{index + 1}. {task_date[0]}. {task_date[1].day} {task_date[1].strftime('%b')}")
        task_number = int(input())
        rows = session.query(Table).all()
        delete = rows[task_number - 1]
        session.delete(delete)
        session.commit()
        print('The task has been deleted!')

def exit():
    global in_list
    print('Bye!')
    in_list = False

while in_list:
    print("""1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit
""")
    answer = int(input())
    if answer == 1:
        today_task()
    elif answer == 2:
        week_task()
    elif answer == 3:
        all_task()
    elif answer == 4:
        missed_task()
        print()
    elif answer == 5:
        add_task()
    elif answer == 6:
        del_task()
    elif answer == 0:
        exit()

