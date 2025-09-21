import utils as utils
from mysql.connector import Error

def add_contact():
    name = input("Enter name: ")
    email = input("Enter email: ")
    phone_numbers = {}
    while True:
        phone_number = input("Enter phone number (or 'done' to finish): ")
        if phone_number.lower() == 'done':
            break
        note = input("Enter note for this number (or leave blank): ")
        phone_numbers.update({phone_number: note})

    print("Available groups:")
    view_groups_table()
    group_id = input("Enter group ID (or leave blank for no group): ")
    group_id = int(group_id) if group_id else None

    try:
        connection = utils.get_db_connection()
        cursor = connection.cursor()

        # Insert contact
        insert_contact_query = "INSERT INTO contacts (name, email, group_id) VALUES (%s, %s, %s)"
        cursor.execute(insert_contact_query, (name, email, group_id))
        contact_id = cursor.lastrowid

        # Insert phone numbers
        insert_phone_query = "INSERT INTO phone (contact_id, phone_number, note) VALUES (%s, %s, %s)"
        for number, note in phone_numbers.items():
            cursor.execute(insert_phone_query, (contact_id, number, note))

        connection.commit()
        print("Contact added successfully.")

    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def view_contacts():
    try:
        connection = utils.get_db_connection()
        cursor = connection.cursor()

        query = """SELECT c.contact_id, c.name, c.email, g.group_name, p.phone_number
                   FROM contacts c
                   LEFT JOIN groups_table g ON c.group_id = g.group_id
                   LEFT JOIN phone p ON c.contact_id = p.contact_id
                   ORDER BY c.contact_id"""
        cursor.execute(query)
        results = cursor.fetchall()

        contacts = {}
        for row in results:
            contact_id, name, email, group_name, phone_number = row
            if contact_id not in contacts:
                contacts[contact_id] = {
                    "name": name,
                    "email": email,
                    "group": group_name,
                    "phone_numbers": []
                }
            if phone_number:
                contacts[contact_id]["phone_numbers"].append(phone_number)

        for contact in contacts.values():

            print(f"Name: {contact['name']} \nEmail: {contact['email']} \nGroup: {contact['group']} \nPhones: {', '.join(contact['phone_numbers'])}")

    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def search_contact(name):
    try:
        connection = utils.get_db_connection()
        cursor = connection.cursor()

        query = """SELECT c.contact_id, c.name, c.email, g.group_name, p.phone_number
                   FROM contacts c
                   LEFT JOIN groups_table g ON c.group_id = g.group_id
                   LEFT JOIN phone p ON c.contact_id = p.contact_id
                   WHERE c.name LIKE %s
                   ORDER BY c.contact_id"""
        cursor.execute(query, (f"%{name}%",))
        results = cursor.fetchall()

        contacts = {}
        for row in results:
            contact_id, name, email, group_name, phone_number = row
            if contact_id not in contacts:
                contacts[contact_id] = {
                    "name": name,
                    "email": email,
                    "group": group_name,
                    "phone_numbers": []
                }
            if phone_number:
                contacts[contact_id]["phone_numbers"].append(phone_number)

        for contact in contacts.values():
            print(f"Name: {contact['name']}, Email: {contact['email']}, Group: {contact['group']}, Phones: {', '.join(contact['phone_numbers'])}")

    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def update_contact(contact_id):
    try:
        connection = utils.get_db_connection()
        cursor = connection.cursor()

        # Fetch current contact info
        cursor.execute("""
            SELECT c.name, c.email, g.group_name, c.group_id
            FROM contacts c
            LEFT JOIN groups_table g ON c.group_id = g.group_id
            WHERE c.contact_id = %s
        """, (contact_id,))
        contact = cursor.fetchone()
        if not contact:
            print("Contact not found.")
            return

        name, email, group_name, group_id = contact

        # Fetch current phone numbers
        cursor.execute("SELECT phone_number, note FROM phone WHERE contact_id = %s", (contact_id,))
        phones = cursor.fetchall()

        print(f"Current Info - Name: {name}, Email: {email}, Group: {group_name}, Phones: {', '.join([p[0] for p in phones])}")

        # Get new values
        new_name = input(f"Name [{name}]: ") or name
        new_email = input(f"Email [{email}]: ") or email

        print("Available groups:")
        view_groups_table()
        new_group_id = input(f"Group ID [{group_id if group_id else 'None'}]: ")
        new_group_id = int(new_group_id) if new_group_id else group_id

        # Update contact info
        cursor.execute("""
            UPDATE contacts SET name = %s, email = %s, group_id = %s WHERE contact_id = %s
        """, (new_name, new_email, new_group_id, contact_id))

        # Update phone numbers
        update_phones = input("Update phone numbers? (y/n): ").lower()
        if update_phones == 'y':
            cursor.execute("DELETE FROM phone WHERE contact_id = %s", (contact_id,))
            while True:
                phone_number = input("Enter phone number (or 'done' to finish): ")
                if phone_number.lower() == 'done':
                    break
                note = input("Enter note for this number (or leave blank): ")
                cursor.execute(
                    "INSERT INTO phone (contact_id, phone_number, note) VALUES (%s, %s, %s)",
                    (contact_id, phone_number, note)
                )

        connection.commit()
        print("Contact updated successfully.")

    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def delete_contact(contact_id):
    try:
        connection = utils.get_db_connection()
        cursor = connection.cursor()

        cursor.execute("DELETE FROM phone WHERE contact_id = %s", (contact_id,))
        cursor.execute("DELETE FROM contacts WHERE contact_id = %s", (contact_id,))

        connection.commit()
        print("Contact deleted successfully.")

    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def add_group(group_name):
    try:
        connection = utils.get_db_connection()
        cursor = connection.cursor()

        cursor.execute("INSERT INTO groups_table (group_name) VALUES (%s)", (group_name,))
        connection.commit()
        print("Group added successfully.")

    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def view_groups_table():
    try:
        connection = utils.get_db_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT group_id, group_name FROM groups_table")
        results = cursor.fetchall()

        for row in results:
            print(f"Group ID: {row[0]}, Group Name: {row[1]}")

    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
