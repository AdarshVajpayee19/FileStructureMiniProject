import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
from tkinter import Grid

# Hash table to store transactions
hashTable = [[] for _ in range(10)]

class Transaction:
    def __init__(self, accountNo, date, description, amount, transactionId):
        self.accountNo = accountNo
        self.date = date
        self.description = description
        self.amount = amount
        self.transactionId = transactionId

# Hash function
def hashFunction(accountNo):
    return accountNo % 10

def insertTransaction():
    insert_window = tk.Toplevel(window)
    insert_window.title("Insert Transaction")
    insert_window.geometry("1000x800")

    # Load the background image
    background_image = Image.open("Fs.jpeg")
    background_photo = ImageTk.PhotoImage(background_image)

    # Create a Label widget to hold the background image
    background_label = tk.Label(insert_window, image=background_photo)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Create a Frame to hold the content
    frame = tk.Frame(insert_window, bg="white")
    frame.pack(expand=True, padx=50, pady=50)

    def insertLogic():
        accountNo = int(account_entry.get())
        date = date_entry.get()
        description = description_entry.get()
        amount = float(amount_entry.get())
        hashValue = hashFunction(accountNo)
        bucket = hashTable[hashValue]
        if len(bucket) < 4:
            # Generate a unique transaction ID
            transactionId = f"Txn-{len(bucket)+1}"
            transaction = Transaction(accountNo, date, description, amount, transactionId)
            bucket.append(transaction)
            messagebox.showinfo("Insert Transaction", "Transaction inserted successfully!")

            # Replace the "#" symbol with the transaction ID in transactions.txt
            with open("transactions.txt", "a") as file:
                file.write(f"Account Number: {transaction.accountNo} | Date: {transaction.date} | Description: {transaction.description} | Amount: {transaction.amount}\n")
            saveTransactionsToFile()
            saveHashTableToFile()
        else:
            messagebox.showerror("Insert Transaction", "Maximum number of transactions reached for this hash key.")
    
  # Set the font size
    font_size = 16
    
    # Create labels and entry fields for user input
    account_label = tk.Label(frame, text="Account Number:", font=("Arial", font_size), bg="white")
    account_label.grid(row=0, column=0, sticky="e")
    account_entry = tk.Entry(frame, font=("Arial", font_size))
    account_entry.grid(row=0, column=1)

    date_label = tk.Label(frame, text="Date:", font=("Arial", font_size), bg="white")
    date_label.grid(row=1, column=0, sticky="e")
    date_entry = tk.Entry(frame, font=("Arial", font_size))
    date_entry.grid(row=1, column=1)

    description_label = tk.Label(frame, text="Description:", font=("Arial", font_size), bg="white")
    description_label.grid(row=2, column=0, sticky="e")
    description_entry = tk.Entry(frame, font=("Arial", font_size))
    description_entry.grid(row=2, column=1)

    amount_label = tk.Label(frame, text="Amount:", font=("Arial", font_size), bg="white")
    amount_label.grid(row=3, column=0, sticky="e")
    amount_entry = tk.Entry(frame, font=("Arial", font_size))
    amount_entry.grid(row=3, column=1)

    # Create an insert button
    insert_button = tk.Button(frame, text="Insert", font=("Arial", font_size), bg="green", command=insertLogic)
    insert_button.grid(row=4, columnspan=2, pady=10)

    insert_window.mainloop()

# Function to update the transactions.txt file
def updateTransactionsFile1():
    transactionDetails = ""
    for bucket in hashTable:
        for transaction in bucket:
            transactionDetails += f"Account Number: {transaction.accountNo} | Date: {transaction.date} | Description: {transaction.description} | Amount: {transaction.amount}\n"

    with open("transactions.txt", "w") as file:
        file.write(transactionDetails)
    saveTransactionsToFile()
    saveHashTableToFile()

def searchTransaction():
    search_window = tk.Toplevel(window)
    search_window.title("Search Transaction")
    search_window.geometry("1000x800")
    # search_window.configure(bg="#6f66f7")

    background_image = Image.open("Fs.jpeg")
    background_photo = ImageTk.PhotoImage(background_image)

    # Create a Label widget to hold the background image
    background_label = tk.Label(search_window, image=background_photo)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    
    def searchLogic():
        accountNo = int(account_entry.get())
        description = description_entry.get()

        # Read the transactions from the file
        with open("transactions.txt", "r") as file:
            transactionLines = file.readlines()

        matchingTransactions = []

        for line in transactionLines:
            if line.startswith("Account Number: "):
                transactionData = line.split("|")
                if len(transactionData) == 4:
                    currentTransaction = Transaction(0, "", "", 0, 0)
                    currentTransaction.accountNo = int(transactionData[0].split(":")[1].strip())
                    currentTransaction.date = transactionData[1].split(":")[1].strip()
                    currentTransaction.description = transactionData[2].split(":")[1].strip()
                    currentTransaction.amount = transactionData[3].split(":")[1].strip()

                    if currentTransaction.accountNo == accountNo and description in currentTransaction.description:
                        matchingTransactions.append(currentTransaction)

        if not matchingTransactions:
            messagebox.showinfo("Search Transaction", "No transactions found for the specified account number and description.")
        else:
            searchWindow = tk.Toplevel(window)
            searchWindow.title("Transaction Details")
            searchWindow.geometry("1000x800")

            background_image = Image.open("Fs.jpeg")
            background_photo = ImageTk.PhotoImage(background_image)

            # Create a Label widget to hold the background image
            background_label = tk.Label(searchWindow, image=background_photo)
            background_label.place(x=0, y=0, relwidth=1, relheight=1)

            for transaction in matchingTransactions:
                transactionDetails = f"Account Number: {transaction.accountNo}\n" \
                                    f"Date: {transaction.date}\n" \
                                    f"Description: {transaction.description}\n" \
                                    f"Amount: {transaction.amount}\n"

                transactionLabel = tk.Label(searchWindow, text=transactionDetails,font=("Arial", font_size))
                transactionLabel.pack()
        
        search_window.destroy()
    
    # Set the font size
    font_size = 16
    
# Create a Frame to hold the content
    frame = tk.Frame(search_window, bg="white")
    frame.pack(expand=True, padx=50, pady=50)
    
    # Create labels and entry fields for user input
    account_label = tk.Label(frame, text="Account Number:", font=("Arial", font_size), bg="white")
    account_label.grid(row=0, column=0, sticky="e")
    account_entry = tk.Entry(frame, font=("Arial", font_size))
    account_entry.grid(row=0, column=1)

    description_label = tk.Label(frame, text="Description:", font=("Arial", font_size), bg="white")
    description_label.grid(row=1, column=0, sticky="e")
    description_entry = tk.Entry(frame, font=("Arial", font_size))
    description_entry.grid(row=1, column=1)

    # Create a search button
    search_button = tk.Button(frame, text="Search", font=("Arial", font_size), bg="orange", command=searchLogic)
    search_button.grid(row=2, columnspan=2, pady=10)

    search_window.mainloop()

def updateTransaction():
    update_window = tk.Toplevel(window)
    update_window.title("Update Transaction")
    update_window.geometry("1000x800")

    background_image = Image.open("Fs.jpeg")
    background_photo = ImageTk.PhotoImage(background_image)

    # Create a Label widget to hold the background image
    background_label = tk.Label(update_window, image=background_photo)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    def updateLogic():
        accountNo = int(account_entry.get())
        hashValue = hashFunction(accountNo)
        bucket = hashTable[hashValue]
        matchingTransactions = []

        for transaction in bucket:
            if transaction.accountNo == accountNo:
                matchingTransactions.append(transaction)

        if len(matchingTransactions) == 0:
            messagebox.showinfo("Update Transaction", "No transactions found for the specified account number.")
        elif len(matchingTransactions) == 1:
            transaction = matchingTransactions[0]

            update_window = tk.Toplevel(window)
            update_window.title("Update Transaction")
            update_window.geometry("1000x800")
                    
            background_image = Image.open("Fs.jpeg")
            background_photo = ImageTk.PhotoImage(background_image)

            # Create a Label widget to hold the background image
            background_label = tk.Label(update_window, image=background_photo)
            background_label.place(x=0, y=0, relwidth=1, relheight=1)
            
            description_label = tk.Label(update_window, text="Enter New Description:", font=("Arial", font_size))
            description_label.pack()
            description_entry = tk.Entry(update_window, font=("Arial", font_size))
            description_entry.pack()

            amount_label = tk.Label(update_window, text="Enter New Amount:", font=("Arial", font_size))
            amount_label.pack()
            amount_entry = tk.Entry(update_window, font=("Arial", font_size))
            amount_entry.pack()

            def updateTransactionLogic():
                description = description_entry.get()
                amount = amount_entry.get()

                transaction.description = description
                transaction.amount = amount

                updateTransactionsFile()  # No parameters required

                messagebox.showinfo("Update Transaction", "Transaction updated successfully!")
                update_window.destroy()

            update_button = tk.Button(update_window, text="Update", font=("Arial", font_size), bg="green", command=updateTransactionLogic)
            update_button.pack()

        else:
            selection = simpledialog.askinteger("Update Transaction", "Multiple transactions found. Select an index to update (0 to exit):", minvalue=0, maxvalue=len(matchingTransactions)-1)

            if selection is not None and selection >= 0:
                transaction = matchingTransactions[selection]

                update_window = tk.Toplevel(window)
                update_window.title("Update Transaction")
                update_window.geometry("1000x800")

                background_image = Image.open("Fs.jpeg")
                background_photo = ImageTk.PhotoImage(background_image)

                # Create a Label widget to hold the background image
                background_label = tk.Label(update_window, image=background_photo)
                background_label.place(x=0, y=0, relwidth=1, relheight=1)

                description_label = tk.Label(update_window, text="Enter New Description:", font=("Arial", font_size))
                description_label.pack()
                description_entry = tk.Entry(update_window, font=("Arial", font_size))
                description_entry.pack()

                amount_label = tk.Label(update_window, text="Enter New Amount:", font=("Arial", font_size))
                amount_label.pack()
                amount_entry = tk.Entry(update_window, font=("Arial", font_size))
                amount_entry.pack()

                def updateTransactionLogic():
                    description = description_entry.get()
                    amount = amount_entry.get()

                    transaction.description = description
                    transaction.amount = amount

                    updateTransactionsFile()  # No parameters required

                    messagebox.showinfo("Update Transaction", "Transaction updated successfully!")
                    update_window.destroy()

                update_button = tk.Button(update_window, text="Update", font=("Arial", font_size), bg="green", command=updateTransactionLogic)
                update_button.pack()

    font_size = 16
    # Create a Frame to hold the content
    frame = tk.Frame(update_window, bg="white")
    frame.pack(expand=True, padx=50, pady=50)

    # Create labels and entry fields for user input
    account_label = tk.Label(frame, text="Account Number:", font=("Arial", font_size), bg="white")
    account_label.grid(row=0, column=0, sticky="e")
    account_entry = tk.Entry(frame, font=("Arial", font_size))
    account_entry.grid(row=0, column=1)

    # Create an update button
    update_button = tk.Button(frame, text="Update", font=("Arial", font_size), bg="green", command=updateLogic)
    update_button.grid(row=1, columnspan=2, pady=10)

    update_window.mainloop()


#Update transaction in transactions.txt file
def updateTransactionsFile():
    transactionDetails = ""
    for bucket in hashTable:
        for transaction in bucket:
            transactionDetails += f"Account Number: {transaction.accountNo} | Date: {transaction.date} | Description: {transaction.description} | Amount: {transaction.amount}\n"

    with open("transactions.txt", "w") as file:
        file.write(transactionDetails)
    saveTransactionsToFile()
    saveHashTableToFile()

def deleteTransaction():
    # Create a new top-level window with increased size
    delete_window = tk.Toplevel(window)
    delete_window.title("Delete Transaction")
    delete_window.geometry("1000x800")
    # delete_window.configure(bg="#6f66f7")
    background_image = Image.open("Fs.jpeg")
    background_photo = ImageTk.PhotoImage(background_image)

    # Create a Label widget to hold the background image
    background_label = tk.Label(delete_window, image=background_photo)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    def deleteLogic():
        accountNo = int(account_entry.get())
        description = description_entry.get()
        hashValue = hashFunction(accountNo)
        bucket = hashTable[hashValue]
        matchingTransactions = []

        for transaction in bucket:
            if transaction.accountNo == accountNo and transaction.description == description:
                matchingTransactions.append(transaction)
                transaction.accountNo = '#'

        if len(matchingTransactions) == 0:
            messagebox.showinfo("Delete Transaction", "No transactions found for the specified account number.")
        elif len(matchingTransactions) == 1:
            messagebox.showinfo("Delete Transaction", "Transaction deleted successfully!")
            updateTransactionsFile1()

        else:
            deleteWindow = tk.Toplevel(window)
            deleteWindow.title("Delete Transaction")
            deleteWindow.geometry("1000x800")
            # deleteWindow.configure(bg="light blue")
            background_image = Image.open("Fs.jpeg")
            background_photo = ImageTk.PhotoImage(background_image)

            # Create a Label widget to hold the background image
            background_label = tk.Label(deleteWindow, image=background_photo)
            background_label.place(x=0, y=0, relwidth=1, relheight=1)

            selectionVar = tk.IntVar()
            selectionVar.set(-1)

            def deleteConfirmationButtonPressed():
                selection = selectionVar.get()

                if selection >= 0 and selection < len(matchingTransactions):
                    transaction = matchingTransactions[selection]
                    confirmation = messagebox.askyesno(
                        "Delete Transaction",
                        "Are you sure you want to delete this transaction?\n\nAccount Number: {}\nDate: {}\nDescription: {}\nAmount: {}".format(
                            transaction.accountNo, transaction.date, transaction.description, transaction.amount),
                    )

                    if confirmation:
                        #bucket.remove(transaction)
                        matchingTransactions.append(transaction)
                        transaction.accountNo = '#'
                        messagebox.showinfo("Delete Transaction", "Transaction deleted successfully!")
                        updateTransactionsFile1()
                        deleteWindow.destroy()
                else:
                    messagebox.showerror("Delete Transaction", "Invalid selection. Please select a valid index.")

            accountNoLabel = tk.Label(deleteWindow, text="Account Number:", font=("Arial", 12))
            accountNoLabel.pack()

            accountNoEntry = tk.Entry(deleteWindow, font=("Arial", 12))
            accountNoEntry.pack()

            selectionLabel = tk.Label(deleteWindow, text="Select Transaction to Delete:", font=("Arial", 12))
            selectionLabel.pack()

            for i, transaction in enumerate(matchingTransactions):
                radioBtn = tk.Radiobutton(
                    deleteWindow,
                    text=f"Transaction {i+1}",
                    variable=selectionVar,
                    value=i,
                    font=("Arial", 12),
                )
                radioBtn.pack()

            deleteConfirmationBtn = tk.Button(deleteWindow, text="Delete", command=deleteConfirmationButtonPressed, font=("Arial", 12), bg="red")
            deleteConfirmationBtn.pack()

    # Set the font size and button color
    font_size = 16
    button_color = "red"

    # Create a Frame to hold the content
    frame = tk.Frame(delete_window, bg="white")
    frame.pack(expand=True, padx=50, pady=50)

    # Create labels and entry fields for user input
    account_label = tk.Label(frame, text="Account Number:", font=("Arial", font_size), bg="white")
    account_label.grid(row=0, column=0, sticky="e")
    account_entry = tk.Entry(frame, font=("Arial", font_size))
    account_entry.grid(row=0, column=1)

    description_label = tk.Label(frame, text="Transaction Description:", font=("Arial", font_size), bg="white")
    description_label.grid(row=1, column=0, sticky="e")
    description_entry = tk.Entry(frame, font=("Arial", font_size))
    description_entry.grid(row=1, column=1)

    # Create a delete button
    delete_button = tk.Button(frame, text="Delete", font=("Arial", font_size), bg=button_color, command=deleteLogic)
    delete_button.grid(row=2, columnspan=2, pady=10)

    delete_window.mainloop()


def displayTransactions():
    transactionDetails = ""
    for bucket in hashTable:
        for transaction in bucket:
            if transaction.accountNo != '#':
                transactionDetails += f"Account Number: {transaction.accountNo}\nDate: {transaction.date}\nDescription: {transaction.description}\nAmount: {transaction.amount}\n\n"

    if transactionDetails:
        displayWindow = tk.Toplevel(window)
        displayWindow.title("Display Transactions")
        displayWindow.geometry("1000x800")

        # Load the background image
        background_image = Image.open("Fs.jpeg")
        background_photo = ImageTk.PhotoImage(background_image)

        # Create a Label widget to hold the background image
        background_label = tk.Label(displayWindow, image=background_photo)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Make the label fill the entire window
        displayWindow.resizable(width=True, height=True)

        # Create a Frame to hold the content
        frame = tk.Frame(displayWindow)
        frame.pack(expand=True, padx=50, pady=50)

        # Create a scrollable text widget to display the transaction details
        transaction_text = tk.Text(frame, font=("Arial", 12))
        transaction_text.pack(fill=tk.BOTH, expand=True)

        # Insert the transaction details into the text widget
        transaction_text.insert(tk.END, transactionDetails)

        # Create a scrollbar for the text widget
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the scrollbar to work with the text widget
        transaction_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=transaction_text.yview)

        closeButton = tk.Button(displayWindow, text="Close", command=displayWindow.destroy, font=("Arial", 12), bg="red")
        closeButton.pack(pady=10)
    else:
        messagebox.showinfo("Display Transactions", "No transactions found.")


def displayHashTable():
    hashTableDetails = ""
    ac = []
    d = []

    for i, bucket in enumerate(hashTable):
        if len(bucket) == 0:
            bucketDetails = f"Bucket {i}: {'/' * 4}"  # Display '#' for empty bucket
        else:
            accountNumbers = [str(transaction.accountNo) for transaction in bucket]
            ac.clear()
            ac.extend(accountNumbers)

            date = [str(transaction.date) for transaction in bucket]
            d.clear()
            d.extend(date)

            description = [str(transaction.description) for transaction in bucket]
            amount = [str(transaction.amount) for transaction in bucket]

            bucketDetails = f"Bucket {i}: "
            for j in range(len(ac)):
                if ac[j] != '#':
                    data = ac[j] + "|" + d[j] + "|" + description[j] + "|" + amount[j]
                    bucketDetails += data + ", "
                else:
                    bucketDetails += "#, "

            if len(bucket) < 4:
                # Display remaining '#' symbols for partially filled bucket
                bucketDetails += '/' * (4 - len(bucket))

        hashTableDetails += bucketDetails + "\n"

    if hashTableDetails == "":
        messagebox.showinfo("Display Hash Table", "Hash table is empty.")
    else:
        displayWindow = tk.Toplevel(window)
        displayWindow.title("Display Hash Table")
        displayWindow.geometry("1000x800")

        # Load the background image
        background_image = Image.open("Fs.jpeg")
        background_photo = ImageTk.PhotoImage(background_image)

        # Create a Canvas widget to hold the background image
        canvas = tk.Canvas(displayWindow, width=1000, height=250)
        canvas.pack(fill=tk.BOTH, expand=True)

        # Set the background image on the canvas
        canvas.create_image(0, 0, image=background_photo, anchor=tk.NW)

        # Create a Frame to hold the content
        frame = tk.Frame(canvas)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Create a scrollable text widget to display the hash table details
        hash_table_text = tk.Text(frame, font=("Arial", 12), bg="white")
        hash_table_text.pack(fill=tk.BOTH, expand=True)

        # Insert the hash table details into the text widget
        hash_table_text.insert(tk.END, hashTableDetails)

        # Create a scrollbar for the text widget
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the scrollbar to work with the text widget
        hash_table_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=hash_table_text.yview)

        closeButton = tk.Button(displayWindow, text="Close", command=displayWindow.destroy, font=("Arial", 12), bg="red")
        closeButton.pack(pady=10)

# Save the transactions to a file
def saveTransactionsToFile():
    transactionDetails = ""
    for bucket in hashTable:
        for transaction in bucket:
            if transaction.accountNo!='#':
                transactionDetails += f"Account Number: {transaction.accountNo} | Date: {transaction.date} | Description: {transaction.description} | Amount: {transaction.amount}\n"

    if transactionDetails:
        with open("transactions.txt", "w") as file:
            file.write(transactionDetails)
        messagebox.showinfo("Save Transactions to File", "Transactions saved to file successfully.")
    else:
        messagebox.showinfo("Save Transactions to File", "No transactions to save.")

def saveHashTableToFile():
    try:
        with open("hash_table.txt", "w") as file:
            hashTableDetails = ""
            ac = []
            d = []

            for i, bucket in enumerate(hashTable):
                if len(bucket) == 0:
                    bucketDetails = f"Bucket {i}: {'/' * 4}"  # Display '#' for empty bucket
                else:
                    accountNumbers = [str(transaction.accountNo) for transaction in bucket]
                    ac.clear()
                    ac.extend(accountNumbers)

                    date = [str(transaction.date) for transaction in bucket]
                    d.clear()
                    d.extend(date)

                    description = [str(transaction.description) for transaction in bucket]
                    amount = [str(transaction.amount) for transaction in bucket]

                    bucketDetails = f"Bucket {i}: "
                    for j in range(len(ac)):
                        if ac[j] != '#':
                            data = ac[j] + "|" + d[j] + "|" + description[j] + "|" + amount[j]
                            bucketDetails += data + ", "
                        else:
                            bucketDetails += "#, "

                    if len(bucket) < 4:
                        # Display remaining '#' symbols for partially filled bucket
                        bucketDetails += '/' * (4 - len(bucket))

                hashTableDetails += bucketDetails + "\n"

            file.write(hashTableDetails)

        messagebox.showinfo("Write Hash Table to File", "Hash table written to 'hash_table.txt' file.")
    except IOError:
        messagebox.showerror("Write Hash Table to File", "Error occurred while writing the hash table to the file.")    

# Function to handle the delete button press event
def deleteButtonPressed():
    deleteTransaction()
    displayTransactions()

# Create the main window
window = tk.Tk()
window.title("Transaction Management System")
WINDOW_TITLE = "Transaction Management System"
WINDOW_WIDTH = 1300
WINDOW_HEIGHT = 1000

button_bg = "#202123"
button_fg = "white"
button_width = 16
button_height = 2
button_font = ("Arial", 14, "bold")

background_image = Image.open("Fs.jpeg")
background_image = background_image.resize((WINDOW_WIDTH, WINDOW_HEIGHT), Image.ANTIALIAS)
background_photo = ImageTk.PhotoImage(background_image)

# Create a label to hold the background image
background_label = tk.Label(window, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# # Add the heading text to the label
# heading_text = "Banking System Using Hashing And Buckets"
# heading_label = tk.Label(window, text=heading_text, font=("Arial", 10, "bold"),pady=20)
# heading_label.configure(highlightthickness=0)
# heading_label.place(relx=0.5, rely=0, anchor="n")

# Function to change button colors when hovered
def on_button_hover(event):
    event.widget.config(bg="#222325", fg="yellow")

# Function to change button colors when not hovered
def on_button_leave(event):
    event.widget.config(bg="#202123", fg="white")

# Create a frame to hold the buttons
button_frame = tk.Frame(window,bg="#cbccd0")
button_frame.pack(pady=150)

# Create the first four buttons and align them horizontally in the center
insert_button = tk.Button(button_frame, text="Insert Transaction", bg=button_bg, fg=button_fg, width=button_width, height=button_height, font=button_font, padx=20, pady=30, command=insertTransaction)
insert_button.bind("<Enter>", on_button_hover)
insert_button.bind("<Leave>", on_button_leave)
insert_button.pack(side="left", padx=10)

search_button = tk.Button(button_frame, text="Search Transaction", bg=button_bg, fg=button_fg, width=button_width, height=button_height, font=button_font, padx=20, pady=30, command=searchTransaction)
search_button.bind("<Enter>", on_button_hover)
search_button.bind("<Leave>", on_button_leave)
search_button.pack(side="left", padx=10)

update_button = tk.Button(button_frame, text="Update Transaction", bg=button_bg, fg=button_fg, width=button_width, height=button_height, font=button_font, padx=20, pady=30, command=updateTransaction)
update_button.bind("<Enter>", on_button_hover)
update_button.bind("<Leave>", on_button_leave)
update_button.pack(side="left", padx=10)

delete_button = tk.Button(button_frame, text="Delete Transaction", bg=button_bg, fg=button_fg, width=button_width, height=button_height, font=button_font, padx=20, pady=30, command=deleteButtonPressed)
delete_button.bind("<Enter>", on_button_hover)
delete_button.bind("<Leave>", on_button_leave)
delete_button.pack(side="left", padx=10)

# Create a new frame for the next two buttons
button_frame2 = tk.Frame(window,bg="#cbccd0")
button_frame2.pack(pady=75)

# Use the grid method to align the buttons in a vertical column at the center
display_button = tk.Button(button_frame2, text="Display Transactions", bg=button_bg, fg=button_fg, width=button_width, height=button_height, font=button_font, padx=20, pady=30, command=displayTransactions)
display_button.bind("<Enter>", on_button_hover)
display_button.bind("<Leave>", on_button_leave)
display_button.grid(row=1, column=0, padx=10, pady=10)

display_hash_button = tk.Button(button_frame2, text="Display Hash Table", bg=button_bg, fg=button_fg, width=button_width, height=button_height, font=button_font, padx=20, pady=30, command=displayHashTable)
display_hash_button.bind("<Enter>", on_button_hover)
display_hash_button.bind("<Leave>", on_button_leave)
display_hash_button.grid(row=1, column=1, padx=10, pady=10)

# Configure the grid to center the buttons
Grid.columnconfigure(button_frame2, 0, weight=1)
Grid.rowconfigure(button_frame2, 0, weight=1)
Grid.rowconfigure(button_frame2, 1, weight=1)

# Run the main window loop
window.mainloop()
