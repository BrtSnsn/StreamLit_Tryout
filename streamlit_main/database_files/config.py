# db_user = 'myusername'
db_user = 'postgres'
# db_pass = 'mypassword'
db_pass = 'postgres'
db_host = 'db'
# db_host = 'localhost'
db_port = '5432'
db_name = 'postgres'

# Connect to to the database
db_string = f'postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'