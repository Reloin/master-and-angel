# master-and-angel
A hassle free way for master and angel to communicate through email

## How would client use this program
Send an email to an agent email account. The first line of the content must include the keyword **angel** or **master**, then it will be sent to their corresponding angel or master after the script was executed.

## prerequisite
You will need to write 2 Json file on your own, one is master.json the other is pwd.json. The former one records the angel's email as key and master's email as value; the latter one just stores your email and password. After filling up master.json run `python swap.py` to swap key and values in master.json and generate angel.json. You could use cron or task scheduler to 
