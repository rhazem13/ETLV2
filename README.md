# SQL Compiler
---------------------
> A compiler with a good GUI that can not only scan, parse and compile SQL-like statements into python code but also excutes the code.

The need for this tool arises as nowadays we have lots of data source types, So e thought it'll be beneficial to make an easy-to-use tool that acts as an interface between the user and their data which lies on different file formats and databases.

We know that all of that can be done in python easily using Pandas for example; but not all users have this kind of technical background. A GUI application would be great with even easier syntax than Python (SQL-like).

Here is what we have made (so far):
!(https://drive.google.com/file/d/1juoTf76jpQc79_GMUBuCNfjqO13_OWs9/view?usp=sharing)

We first built a small ETL module that is built on top of Pandas which provides three main interfaces (functions):

- extract()

Which takes the path of the file or the connection string, do the magic, and return a Pandas `DataFrame` holding the data of that source.

- transform()

Which takes a Pandas `DataFrame` and a criteria dict and based on that criteria filters the data and return the result.

- load()
Which takes the the data as `DataFrame` also and the data destination you want (regardless of its type) and *append* the data into it. 

Then there is the compiler module which uses ply (lex and yacc) to scan and parse an input string and return the Python code equevelant to that string.

This covers a wide varaiety of syntax including (selecting and inserting); features include:

- **select**: 
 - Which extracts data according to some criteria and present them to the GUI.
 - example: `select id, name from [C:\users\username\Desktop\students.csv];`.
- **select into**: 
 - Which do the same the thing but load the result into the specified data destination.
 - example: `select * from [C:\users\username\Desktop\students.csv] into [C:\users\username\Desktop\students_start_with_A.db] where name like "A.*";`.
- **insert into**:
 - Which inserts the values you give into a data destination.
 - example: `insert into [C:\users\username\Desktop\students_start_with_A.db] columns (name, age) values ("Name1", 22), ("Name2", 23);`
 
Finally, we built a GUI window to work as an interface between the tool and the user, it gives the following layout:
 - **Input text box** for the SQL-like commands.
 - **Output text box** for the generated Python code.
 - **Results table** for showing the results if any.
 - **Compile Button** that compiles the commands you gave to Python.
 - **Execute Button** that executes the Python code.
 
You can edit the generated Python before proceeding to execution.

Here is a diagram that helps you understand the flow of the app:
!(https://drive.google.com/file/d/1mudzktH2SjKv5CGLUJgDdqB2w4EFSVdx/view?usp=sharing)


### Run and Installation
1. Run `git clone https://github.com/MostafaAmin1299/ETL-Compiler.git` to get this repo.
2. Run `pip install -r requirements.txt` to install the needed requirements.
3. Run `python main.py` inside a shell inside the repo.



### Helpful Resouces
1. [PLY](http://www.dabeaz.com/ply/ply.html) (Python Lex-Yacc)
2. [Pandas](https://pandas.pydata.org/docs/)
3. [PyQT5](https://doc.bccnsoft.com/docs/PyQt5/)
