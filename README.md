# Python Todo List CLI

## Introduction

Today we're building a **command line interface**(cli) version of the world famous todo list!

What is a [command line interface](https://www.techopedia.com/definition/3337/command-line-interface-cli)? A program that you can use from the command line(terminal/git-bash/conemu/etc)!

Here's what an gif of the completed project:

![demo](https://i.imgur.com/dZvo4gb.gif)

## Learning Objectives ✍️📚📝

1. Learn how to pass and consume arguments from the command line.
2. Learn how to access a sql database from our Python applications.
3. Learn how to use the [SQLite3](https://marketplace.visualstudio.com/items?itemName=alexcvzz.vscode-sqlite) plugin for VScode.
4. Learn how to use [Fire](https://github.com/google/python-fire) to C.R.U.D. our resources.

## Features 🎯🥇🏆

[ ] The user can run your program from the command line.
[ ] The user can see all todos from the command line by passing a `list` command, sorted with the ones due first.
[ ] The user can add a todo from the command line by passing an `add` argument. The fields specified should be `body`, `due_date`, and `project_id`. The fields `due_date` and `project_id` are optional. Only `body` is required.
[ ] By default todos are incomplete.
[ ] The user should see a message giving information about the todo that was added.
[ ] User can mark a todo as complete by passing a command and an id.
[ ] User can mark a todo as incomplete by passing a command and an id.
[ ] If the user does not supply the correct arguments, or supplies a `--help` flag, the user sees a [usage](https://cdn-images-1.medium.com/max/1600/1*V5JwUvETGDLVdoCl--oMKw.png) message.
[ ] The user can supply arguments to the `list` command to only see todos that are `complete`.

## Optional Requirements

[ ] The user can supply arguments to the `list` command to only see todos of a particular `project_id`.
[ ] The user can supply arguments to the `list` command to reverse the default sort, to now see the todos by due_date descending.
[ ] The user can supply arguments to the `list` command to combine the above options.
[ ] The user can add a `user_id` to each todo.
[ ] The user can add a user to the system by passing `add_user`. Each user should have a `name`, `email_address`, and `id`.
[ ] The user can call a `list_users` command that shows all the users in the system.
[ ] The user can call a `staff` command that shows each project, combined with each of the users working on that project.
[ ] The user can call a `who_to_fire` command that lists all users who are not currently assigned a todo.
[ ] The user can add a project by calling `add_project`. Each project must have a `name`.
[ ] The user can see all projects from the command line.

### **Milestone 1 🛣🏃 Setup your project**

**A)** Create a new folder, in my case `todoList`, where you want to keep your work and create a file inside of it, `todos.py`.

![demo](https://i.imgur.com/s0e0qNt.png)

**B)** Import packages we'll be using for this lab at the top of `todos.py`.

```python
import os
import sys
import fire
import code
import sqlite3
from datetime import datetime
from termcolor import colored
```

**C)** Define a variable `DEFAULT_PATH` **below** the imported packages. This value will be used to generate a file named `database.sqlite3` in our working directory. We're using the `os` library provided by Python to determine where to put the file and what to name it. We're also using `__file__` which is a global like `console`, `navigator`, or `process` in javascript.

```python
DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'database.sqlite3')
```

**D)** Bookmark a connection to our sql database in a variable called `conn`. We get access to this connection through a call to `connect()` in `sqlite3`. `DEFAULT_PATH` is passed to `connect()`.

```python
conn = sqlite3.connect(DEFAULT_PATH)
```

**E)** Define a string `sql` which will issue a command to our database to create a table by the name of `todos` if it does not already exist. Take note of the arguments passed to this function call.

```python
sql = """
  CREATE TABLE IF NOT EXISTS todos(
    id INTEGER PRIMARY KEY,
    body TEXT NOT NULL,
    due_date TEXT NOT NULL,
    status TEXT DEFAULT "incomplete"
  )
"""
```

**F)** Call `cursor()` on our connection dictionary and store its return in a new variable `cur`.

```python
cur = conn.cursor()
```

**G)** Call `execute()` on our dictionary `cur`. Pass it the `sql` string we defined in the previous step. This is the command which will **execute** database queries.

```python
cur.execute(sql)
```

**H)** Define a **default** conditional which runs our application at the bottom of the file.

```python
if __name__  == '__main__':
  print('Main function executing')
```

**G)** Test we've setup everything correctly.

1. Run `python todos.py` in your terminal window and you should see the `print()` call execute. You'll see a file, `database.sqlite3`, created in your working directory.

2. Open the `sqlite3` extension in VScode, open your database and choose the `database.sqlite3` when prompted. You should see **no result found**.

![demo](https://i.imgur.com/OU1k2nC.gif)

### **Milestone 2 🛣🏃 Implement Todo List**

**A)** Implement accepting command line arguments and catching errors.

```python
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
```

A few notes on this code.

1. We've wrapped everything inside of a `try` & `except`. Recall `try` & `catch` from javascript.
2. `sys.argv[1]` is where we access the flag we pass after `python3 todos.py`.
3. If we see a `flag` of `--help` then we'll call a function we define `show_help_menu()`.
4. Otherwise, we'll use the `fire` package to listen for one of 5 potential commands; `add`, `delete`, `list`, `do` & `undo`.
5. The `keys` are mapped to `functions` we'll **define momentarily**.
5. If anything goes wrong then call `show_menu_help()` & exit.

**B)** Implement `show_help_menu()`

Feel free to change the colors & chars to your liking.

```python
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
```

**C)** Run `python3 todos.py` from the command line with and without `--help` to test the behavior.

![demo](https://i.imgur.com/Usp0VUN.gif)

**D)** Implement the `add` function.

```python
def add(body):
  print(colored('Adding Todo:', 'green'), body)
  sql = """
    INSERT INTO todos (body, due_date) VALUES ?, ?
  """
  cur.execute(sql, (body, datetime.now()))
  conn.commit()
```

1. Here we're printing a prompt and the body of the todo.
2. We create a sql `string` which contains our query. The `?`'s will have values inserted momentarily.
3. We execute the query by calling `execute()` and passing it two arguments. The first argument is our `sql` string, the second a [tuple](https://www.w3schools.com/python/python_tuples.asp) where we pass the values which will replacee the `?`'s.
4. We commit the execution to our databse with a call to `commit()`.

**E)** Refactor the call to `Fire()` within our main conditional.

```python
fire.Fire({
    'add': add,
})
```

![Demo](https://i.imgur.com/dK3m7PK.gif)

We should now see that we're able to run the command `python todos.py add 'My todo'` and see the result in out SQLite plugin for VSCode, **excellent**.

**F)** Implement displaying a list by adding the `list` key to our call to `Fire()`.

```python
fire.Fire({
    'add': add,
    'list': show_list,
})
```

**G)** Implement the `show_list()` function we just mapped to the flag `list`.

```python
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
```

![Demo](https://i.imgur.com/kmMrSzj.gif)

We should now be able to see our todolist in the terminal window by running the command.

```python
python todos.py list
```

# Tutorials

* https://stackabuse.com/a-sqlite-tutorial-with-python/
* https://www.pythoncentral.io/introduction-to-sqlite-in-python/

# Official Documentation

* https://docs.python.org/2/library/sqlite3.html