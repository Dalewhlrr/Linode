from linode_api4 import LinodeClient
import getpass
import subprocess
import os


# Replace 'your_api_token_here' with your actual Linode API token
API_TOKEN = '###'
client = LinodeClient(API_TOKEN)

def create_ubuntu_vm():
    # Define the parameters for the new Linode instance
    region = 'us-ord'  # You can choose the region that suits you
    linode_type = 'g6-nanode-1'  # 1GB shared option (cheapest)
    image = 'linode/ubuntu22.04'  # Ubuntu 22.04 LTS image
    root_password = getpass.getpass("Create password: ")  # Set a secure root password
    label = input("name linode: ")  # A label for your new Linode

    # Create the Linode instance
    new_linode = client.linode.instance_create(
        linode_type,
        region,
        image=image,
        root_pass=root_password,
        label=label
    )

    print(f"New Linode created with ID: {new_linode.id}")
    print("Linode IP:", new_linode.ipv4[0])
    input("Press Enter to return to the main menu...")

def clear_screen():
    try:
        if os.name == 'nt':  # For Windows
            subprocess.run('cls', shell=True)
        else:  # For Linux and Mac
            subprocess.run('clear', shell=True)
    except Exception as e:
        print(f"An error occurred while clearing the screen: {e}")    


def show_running_instances():
    my_linode = client.linode.instances()
    print("All Instances:")
    print("-" * 20)  # Separator for clarity
    for instance in my_linode:
        print(f"Label: {instance.label}")
        print(f"ID: {instance.id}")
        print(f"Linode IP: {instance.ipv4[0]}")
        print("-" * 20)  # Separator for clarity
    input("Press Enter to return to the main menu...")

def delete_linode(linode_id):
    try:
        # Find the Linode instance by ID
        linode = next((linode for linode in client.linode.instances() if linode.id == linode_id), None)
        if linode:
            # Delete the Linode
            linode.delete()
            print(f"Linode {linode_id} deleted successfully.")
        else:
            print(f"Linode with ID {linode_id} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    input("Press Enter to return to the main menu...")

def main():
    while True:
        clear_screen()
        print("1. Create Linode")
        print("2. View Running Linodes")
        print("3. Delete Linode")
        print("4. Exit")

        choice = input("Enter the number of your choice: ")
        choice = int(choice)

        if choice == 1:
            create_ubuntu_vm()
        elif choice == 2:
            show_running_instances()
        elif choice == 3:
            linode_id = int(input("Enter the ID of the Linode to delete: "))
            delete_linode(linode_id)
        elif choice == 4:
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
