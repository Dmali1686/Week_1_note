import os  # Import the 'os' module, which lets Python talk to the Operating System (to check if files exist)

# This is an infinite loop. The 'while True:' means "Keep doing this forever until I say stop (break)"
while True:
    # Print a blank line to make the menu easier to read in the terminal
    print("\n")
    # Print the title of our application
    print("=== My Persistent Notes App ===")
    # Print option 1 for the user
    print("1. Add a note")
    # Print option 2 for the user
    print("2. View all notes")
    # Print option 3 to let the user quit the application
    print("3. Exit")
    
    # Wait for the user to type something and press Enter. Store their answer in a variable called 'choice'
    choice = input("Choose an option (1, 2, or 3): ")

    # Check if the user typed the string "1"
    if choice == "1":
        # Ask the user to type the note they want to save and store it in the variable 'new_note'
        new_note = input("Enter your note: ")
        
        # 'with open(...)' safely opens a file and ensures it gets closed when we are done
        # "notes.txt" is the name of the file we are opening on the hard drive
        # "a" stands for "append mode". If the file exists, it adds to the end of it. If it doesn't exist, it creates it!
        # 'as file' means we are naming this opened file object 'file' so we can use it on the next line
        with open("notes.txt", "a") as file:
            # Write the user's note into the file.
            # The '\n' at the end is a special character that means "New Line" (like pressing Enter). 
            # This ensures the next note will be on a new line instead of glued to this one.
            file.write(new_note + "\n")
            
        # Print a success message so the user knows it worked
        print("✅ Note saved successfully to the hard drive!")

    # Check if the user typed the string "2"
    elif choice == "2":
        # First, we check if the file "notes.txt" actually exists on the hard drive.
        # If they haven't saved any notes yet, the file won't exist, and trying to read it would cause an error.
        if os.path.exists("notes.txt"):
            # Print a header for the notes
            print("\n--- Your Saved Notes ---")
            
            # Open "notes.txt" again, but this time with "r", which stands for "read mode".
            with open("notes.txt", "r") as file:
                # 'file.read()' reads all the text inside the file at once
                # We store all that text inside the variable 'saved_notes'
                saved_notes = file.read()
                
                # We print the 'saved_notes' variable to the terminal screen so the user can see them
                print(saved_notes)
                
            # Print a footer line to show where the notes end
            print("------------------------")
        else:
            # If the file doesn't exist (os.path.exists was False), tell the user they don't have notes yet
            print("❌ No notes found. Try adding one first!")

    # Check if the user typed the string "3"
    elif choice == "3":
        # Print a goodbye message
        print("Goodbye! Your notes are safe on the hard drive.")
        # 'break' stops the 'while True:' infinite loop, allowing the program to end
        break

    # If the user typed anything other than 1, 2, or 3
    else:
        # Tell them they made an invalid choice
        print("❌ Invalid choice. Please try again.")
