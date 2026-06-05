# E/R diagram
![E/R diagram](IMG/ER_diagram.png)

# Running DIS-project
 Assuming Python 3 and PostgreSQL 18

 (1) Run this code to install dependencies.
 >$ pip install -r requirements.txt

 (2) Go into the app.py file and insert your PostgreSQL password in the database configuration

 (3) You must be inside the location of the data folder and then to initialize the database you must run this command.
 >$ psql -U postgres -f data_test.sql

 If the above mentioned command does not work use this command below.
 >$ & "C:\Program Files\PostgreSQL\18\bin\psql.exe" -U postgres -d data_test -f data_test.sql

 (4) Now navigate to the main directory DIS-projekt and then run this command.
 >$ python app.py

 If the above mentioned command does not work use this command below.
 >$ py app.py

 (5) Copy the link into your desired webbrowser.

 (6) Choose a gender, age and input the various hours for studying, gaming and sleeping within a max value of 10 hours for each.

 (7) After all fields have been filled press the calculate button and you will receive an average grade of people with a similar profile as yourself and a Gauss distribution curve will be displayed at the bottom.

 # AI declaration
 No AI has been used
