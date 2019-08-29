import os
import sys
import fire
import code
import sqlite3
from datetime import datetime
from termcolor import colored

# code.interact(local=dict(globals(), **locals()))
DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'database.sqlite3')

conn = sqlite3.connect(DEFAULT_PATH)

sql = """
  CREATE TABLE IF NOT EXISTS todos(
    id INTEGER PRIMARY KEY,
    body TEXT NOT NULL,
    due_date TEXT NOT NULL,
    status TEXT DEFAULT "incomplete"
  )
"""

cur = conn.cursor()
cur.execute(sql)

def show_help_menu():
  os.system('cls' if os.name == 'nt' else 'clear')
  print(colored('Todo List Options:', 'green'))
  print(colored('*' * 50, 'green'))
  print(colored('1. List all todos:', 'green'))
  print(colored('\t python3 todos.py list', 'white'))
  print(colored('2. Add a new todo:', 'green'))
  print(colored('\t python3 todos.py add "My Todo Body"', 'white'))
  print(colored('3. Delete a todo:', 'green'))
  print(colored('\t python3 todos.py delete 1', 'white'))
  print(colored('4. Mark a todo complete:', 'green'))
  print(colored('\t python3 todos.py do 1', 'white'))
  print(colored('5. Mark a todo uncomplete:', 'green'))
  print(colored('\t python3 todos.py undo 1', 'white'))
  print(colored('-' * 100, 'green'))

def add(body):
  print(colored('Adding Todo:', 'green'), body)
  sql = """
    INSERT INTO todos (body, due_date) VALUES (?, ?)
  """
  cur.execute(sql, (body, datetime.now()))
  conn.commit()

def show_list(thingy = None):
  if thingy == None:
    sql = """
      SELECT * FROM todos 
      ORDER BY status DESC
    """
    cur.execute(sql)
    results = cur.fetchall()

  if thingy == "done":
    sql = """
      SELECT * FROM todos
      WHERE status = ?
    """
    cur.execute(sql, ("complete",))
    results = cur.fetchall()

  print(colored('Todo List:', 'green'), len(results), 'todos')
  print(colored('*' * 50, 'green'))
  for row in results:
    print(colored("{0}.".format(row[0]), 'green'), row[1])

def delete(id):
  print(colored('Deleting Todo:', 'green'), id)
  sql = """
    DELETE FROM todos WHERE id = ?
  """
  cur.execute(sql, (id,))
  conn.commit()

def do(id):
  print(colored('Marking todo complete:', 'green'), id)
  sql = """
    UPDATE todos
    SET status="complete"
    WHERE id = ?
  """
  cur.execute(sql, (id,))
  conn.commit()

def undo(id):
  print(colored('Marking todo incomplete:', 'green'), id)
  sql = f"""
    UPDATE todos
    SET status="incomplete"
    WHERE id={id};
  """
  cur.execute(sql)
  conn.commit()

if __name__  == '__main__':
  try:
    arg1 = sys.argv[1]
    if arg1 == '--help':
      show_help_menu()
    else:
      fire.Fire({
        'do': do,
        'add': add,
        'undo': undo,
        'delete': delete,
        'list': show_list,
      })

  except IndexError:
    show_help_menu()
    sys.exit(1)
