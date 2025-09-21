from utils import preparedb
import contact

preparedb()


while True: 
    print("\n----- Contact Management System -----")
    print("1. create new contact")
    print("2. view all contacts")
    print("3. search contact")
    print("4. update contact")
    print("5. delete contact")

    print("6. add group")
    print("7. view all groups")
    print("8. exit")
    user_input = input("Enter your choice: ")
    match user_input:
        case "1":
            contact.add_contact()
        case "2":
            contact.view_contacts()
        case "3":
            name = input("Enter name to search: ")
            contact.search_contact(name)
        case "4":
            contact_id = int(input("Enter contact ID to update: "))
            contact.update_contact(contact_id)
        case "5":
            contact_id = int(input("Enter contact ID to delete: "))
            contact.delete_contact(contact_id)
        case "6":
            group_name = input("Enter group name: ")
            contact.add_group(group_name)
        case "7":
            contact.view_groups_table()
        case "8":
            print("Exiting...")
            break
        case _:
            print("Invalid choice. Please try again.")