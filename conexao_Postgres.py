import psycopg2

def get_connection():
    conn = psycopg2.connect(
        dbname='tcc_chatbot_db',
        user='postgres',
        password='postgres',
        host='localhost',
        port="5432"
    )
    return conn
