# Library Management System

## Overview
The **Library Management System** is designed to help a librarian efficiently track books, manage book transactions, and charge rent fees. The system allows book imports via the Frappe API, provides a user-friendly interface for book transactions and membership form, ensures proper fee tracking, sends monthly email notifications to library members with pending fees, and displays a query report for books.

## Features
### 1. Book Management
- Perform **CRUD operations** (Create, Read, Update, Delete) on books.
- Maintain book stock.
- Import books using **Frappe API**.
- Search for books by **name** and **author**.

### 2. Member Management
- Perform **CRUD operations** on library members.
- Maintain members' outstanding fees.
- Prevent members from borrowing books if their outstanding debt exceeds **Rs. 500**.

### 3. Book Transactions
- Issue a book to a member.
- Process book returns.
- Charge rent fees upon late return.
- Maintain a query report tracking book issues and returns.
- A **www folder page** allows users to view book lists and perform transactions directly.

### 4. Automated Fee Notifications
- Monthly email notifications are sent to members whose outstanding balance exceeds **Rs. 500**.
- Uses **Frappe Scheduler Event** to automate the process.

## Frappe API Integration for Book Import
The system integrates with the **Frappe API** to import books in batches of 20 at a time. The librarian can specify parameters such as:
- **Title**
- **Authors**
- **ISBN**
- **Publisher**
- **Quantity**

### How to Use the API
1. Navigate to the **Book Import** section in the application.
2. Click **Import Books** to fetch data from the Frappe API.
3. The imported books will be added to the system.
4. To import a specific book, you can do so by its title and author.

## Installation
### Prerequisites
Ensure you have **Frappe Bench** installed before proceeding.

### Steps to Install
1. Clone the repository from GitHub:
   ```sh
   git clone https://github.com/your-repository/library-management.git
   ```
2. Navigate to the project directory:
   ```sh
   cd library-management
   ```
3. Install the application using **Bench**:
   ```sh
   cd $PATH_TO_YOUR_BENCH
   bench get-app https://github.com/your-repository/library-management --branch main
   bench install-app library_management
   ```

## Usage
- **Manage Books**: Add, edit, delete, search, and import books.
- **Manage Members**: Add, edit, delete members and track their outstanding fees.
- **Issue Books**: Issue books to members and track due dates.
- **Return Books**: Process book returns and charge rent fees.
- **Automated Notifications**: Ensure members with pending dues receive email reminders.

## Contributing
If you want to contribute:
1. Fork the repository.
2. Create a new branch:
   ```sh
   git checkout -b feature-name
   ```
3. Make your changes and commit them:
   ```sh
   git commit -m "Added new feature"
   ```
4. Push to your forked repository:
   ```sh
   git push origin feature-name
   ```
5. Submit a **Pull Request**.

## License
This project is licensed under the **MIT License**.

## Contact
For any issues or inquiries, reach out via email: **kumkumtiwari23@navgurukul.org**.

