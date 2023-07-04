from sql_connection import SQLConnection, print_table


sql = SQLConnection.from_env()

# check connection
print(sql.inspector.get_table_names())
df = sql.query("SELECT * FROM trazado LIMIT 10")
print_table(df)
