from sql_connection import SQLConnection, print_table


db = SQLConnection.from_env()

# check connection
print(db.inspector.get_table_names())
df = db.query("SELECT * FROM trazado LIMIT 10")
print_table(df)
