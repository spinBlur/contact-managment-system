import mysql.connector

def preparedb():
    creatdb()
    create_table()

def creatdb():
    try:
        db = mysql.connector.connect(
            host="localhost",
            username="root",
            password="123456"
        )
        mycursor = db.cursor()
        mycursor.execute("CREATE DATABASE IF NOT EXISTS contactdb")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if 'db' in locals():
            db.close()

def create_table():
    db = get_db_connection()
    mycursor = db.cursor()
    # Create groups table
    query = """
    CREATE TABLE IF NOT EXISTS groups_table (
        group_id INT AUTO_INCREMENT PRIMARY KEY,
        group_name VARCHAR(255) UNIQUE NOT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """
    mycursor.execute(query)

    # Create contacts table
    query = """
    CREATE TABLE IF NOT EXISTS contacts (
        contact_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) UNIQUE,
        group_id INT,
        FOREIGN KEY (group_id) REFERENCES groups_table(group_id)
            ON DELETE SET NULL ON UPDATE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """
    mycursor.execute(query)

    # Create phone table
    query = """
    CREATE TABLE IF NOT EXISTS phone (
        phone_id INT AUTO_INCREMENT PRIMARY KEY,
        contact_id INT,
        phone_number VARCHAR(20) NOT NULL UNIQUE,
        note VARCHAR(255),
        FOREIGN KEY (contact_id) REFERENCES contacts(contact_id)
            ON DELETE CASCADE ON UPDATE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """
    mycursor.execute(query)

def get_db_connection():
    db = mysql.connector.connect(
        host="localhost",
        username="root",
        password="123456",
        database="contactdb"
    )
    return db