#simple cli for archiver
import main as archiver
def cli():
    print("Welcome to archiver!")
    while True:
        print("Do you want to make an archive [1] or open an archive [2]?")
        choice = input("Enter 1 or 2: ")
        if choice == "1":
            print("Make an archive")
            print("Enter the name of the archive: ")
            archive_name = input()
            print("Enter the input folder: ")
            input_folder = input()
            print("Enter the password: ")
            password = input()
            print("Enter the output folder (\".\" for current folder): ")
            output_folder = input()
            print("Do you want to use k-means [1] or not [2]?")
            choice = input("Enter 1 or 2: ")
            if choice == "1":
                kmeans = True
            else:
                kmeans = False
            archiver.make_archive(archive_name, input_folder, password, output_folder,kmeans)
        elif choice == "2":
            print("Open an archive")
            print("Enter the name of the archive: ")
            archive_name = input()
            print("Enter the output folder (\".\" for here): ")
            output_folder = input()
            print("Enter the password: ")
            password = input()
            archiver.open_archive(archive_name, output_folder, password)
        else:
            print("invalid input")

if __name__ == "__main__":
    cli()