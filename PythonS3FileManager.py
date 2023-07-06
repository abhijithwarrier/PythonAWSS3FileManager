# Programmer - python_scripts (Abhijith Warrier)

# PYTHON GUI FOR UPLOADING AND DOWNLOADING FILES FROM AWS S3 BUCKET USING boto3 LIBRARY

# Amazon S3 is an object storage service that offers industry-leading scalability,
# data availability, security, and performance.
# Boto3 makes it easy to integrate our Python application, library, or script with
# AWS services including Amazon S3, Amazon EC2, Amazon DynamoDB, and more.

# The module can be installed using the command - pip install boto3

# Importing necessary packages
import os
import boto3
import tkinter as tk
from tkinter import *
from tkinter import filedialog

# Defining CreateWidgets() function to create necessary tkinter widgets
def CreateWidgets():
    inputFileLabel = Label(root, text="FILE: ", bg="hotpink4")
    inputFileLabel.grid(row=0, column=0, padx=5, pady=5)
    inputFileEntry = Entry(root, width=30, bg='snow3', textvariable=inputFileName)
    inputFileEntry.grid(row=0, column=1, padx=5, pady=5)
    inputFileEntry.config(foreground="black")

    fileBrowse = Button(root, text="BROWSE", command=browseFile)
    fileBrowse.grid(row=0, column=2, padx=5, pady=5)
    fileUpload = Button(root, text="UPLOAD TO S3", command=uploadFile)
    fileUpload.grid(row=1, column=0, padx=5, pady=5, columnspan=2)

    s3FilesListLabel = Label(root, text="S3 FILES LIST", bg="hotpink4")
    s3FilesListLabel.grid(row=2, column=0, padx=5, pady=5)
    root.s3FilesListBox = Listbox(root, width=55, height=20, bg='snow3')
    root.s3FilesListBox.grid(row=3, column=0, rowspan=12, columnspan=3, padx=5, pady=5)
    # Binding onS3FileSelect() event to the ListBox Widget
    root.s3FilesListBox.bind('<<ListboxSelect>>', onS3FileSelect)
    root.s3FilesListBox.config(foreground="black")

    selectedFileLabel = Label(root, text="S3 FILE: ", bg="hotpink4")
    selectedFileLabel.grid(row=18, column=0, padx=5, pady=5)
    root.selectedFileEntry = Entry(root, width=30, bg='snow3', textvariable=s3FileName)
    root.selectedFileEntry.grid(row=18, column=1, padx=5, pady=5)
    root.selectedFileEntry.config(foreground="black")

    downloadButton = Button(root, text="DOWNLOAD", command=downloadFile)
    downloadButton.grid(row=18, column=2, padx=5, pady=15)

    root.notificationLabel = Label(root, bg="hotpink4", font="'' 20")
    root.notificationLabel.grid(row=19, column=0, padx=5, pady=5, columnspan=3)

    # Calling configureAWSSession() function on application start
    configureAWSSession()

# Defining configureAWSSession() function to create AWS Session
def configureAWSSession():
    # Declaring global variables
    global s3BucketName, s3Client, s3Resource, s3BucketObject
    # Storing the AWS Bucket name to which files are to be uploaded
    s3BucketName = "<YOUR_AWS_S3_BUCKET_NAME>"
    # Creating AWS session using the boto3 library
    awsSession = boto3.session.Session(profile_name="<YOUR_AWS_PROFILE>", region_name="<YOUR_AWS_REGION>")
    # Creating S3 access object using the session
    s3Client = awsSession.client("s3")
    # Creating S3 Resource Object using the session
    s3Resource = awsSession.resource("s3")
    # Creating an object of S3 Bucket
    s3BucketObject = s3Resource.Bucket(s3BucketName)
    # Calling the listFiles() to list all files at application startup
    listFiles()

# Defining listFiles() to list all the files that are present in S3 Bucket
def listFiles():
    # Clearing the list widget and list before displaying the updated list
    root.s3FilesListBox.delete(0, END)
    s3FilesList = []
    # Fetching all the files that are stored in the S3 Bucket and adding them to a list
    for file in s3BucketObject.objects.all():
        s3FilesList.append(file.key) # Here key indicates the filename in S3 Bucket
    # Looping through the s3FilesList and displaying the file in the ListBox using insert() method
    for file in s3FilesList:
        root.s3FilesListBox.insert("end", file)

# Defining the browseFile() to select the file to upload to S3 Bucket
def browseFile():
    # Fetching the user-input filename using askopenfilename
    # Setting the initialdir and filetypes arguments are optional.
    f_name = filedialog.askopenfilename(initialdir='<YOUR_DEFAULT_FOLDER_PATH>',
                                          filetypes=(('Text File (*.txt)','*.txt'),
                                                     ('PNG File (*.png)','*.png'),
                                                     ('All File (*.*)', '*.*')))
    # Setting the inputFileName tkinter variable to the file_name value
    inputFileName.set(f_name)

# Defining onS3FileSelect() to display the ListBox Cursor Selection in the Entry widget
def onS3FileSelect(evt):
    # Fetching the ListBox cursor selection
    selectedFileName = root.s3FilesListBox.get(root.s3FilesListBox.curselection())
    # Displaying the selected text from ListBox in the widget using tkinter variable
    s3FileName.set(selectedFileName)

# Defining uploadFile() function to upload file to S3 and display it in the ListBox
def uploadFile():
    # Fetching the user-selected file from the widget using get() of the tkinter variable
    selectedFile = inputFileName.get()
    # Uploading the file to S3 using the upload_file() function of the AWS client created
    # Parameters: Bucket Name, Filename - Name of the selected file, Key - Name of file in S3
    try:
        s3UploadResponse = s3Client.upload_file(
            Bucket=s3BucketName, Filename=selectedFile, Key=os.path.basename(selectedFile)
        )
        # Calling the listFiles() to refresh the list of files that are stored in S3 Bucket
        listFiles()
        # Displaying success notification
        root.notificationLabel.config(text="File Uploaded Successfully!", foreground="springgreen4")
    except Exception:
        # Displaying error notification
        root.notificationLabel.config(text="Error While Uploading File!", foreground="red")

# Defining downloadFile() function to download the selected file from S3 Bucket
def downloadFile():
    # Fetching and storing the user-selected file from the widget using the get() method
    selectedFile = s3FileName.get()
    # Downloading the file from the S3 using the download_file function of AWS client
    # Uploading the file to S3 using the upload_file() function of the AWS client created
    # Parameters: Bucket Name, Filename - Local path and filename, Key - Name of file in S3
    try:
        s3DownloadResponse = s3Client.download_file(
            Bucket=s3BucketName, Key=selectedFile, Filename=f"<YOUR_DESTINATION_PATH>/{selectedFile}"
        )
        # Displaying success notification
        root.notificationLabel.config(text="File Downloaded Successfully!", foreground="springgreen4")
    except Exception:
        # Displaying error notification
        root.notificationLabel.config(text="Error While Downloading File!", foreground="red")

# Creating object of tk class
root = tk.Tk()

# Setting the title, background color, windowsize &
# disabling the resizing property
root.title("PythonS3FileManager")
root.config(background="hotpink4")
root.resizable(False, False)

# Creating the tkinter variables
inputFileName = StringVar()
s3FileName = StringVar()
# Creating an empty list
s3FilesList = []

# Calling the CreateWidgets() function
CreateWidgets()

# Defining infinite loop to run application
root.mainloop()
