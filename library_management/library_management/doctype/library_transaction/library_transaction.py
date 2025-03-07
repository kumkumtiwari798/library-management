import frappe
from frappe.model.document import Document
from datetime import datetime

class LibraryTransaction(Document):
    def before_submit(self):
        if self.status == "Issue":
            self.validate_issue()
            self.validate_maximum_limit()
            
            # Set the book status to Issued
            book = frappe.get_doc("Books", self.book)
            book.status = "Issued"
            book.save()

        elif self.status == "Return":
            self.process_return()

    def process_return(self):
        """ Handle book return, check late fees, and update status """
        book = frappe.get_doc("Books", self.book)

        # Ensure the book is actually issued before returning
        if book.status != "Issued":
            frappe.throw("Book cannot be returned without being issued first")

        # Get issue date from previous transaction
        issue_transaction = frappe.get_list(
            "Library Transaction",
            filters={
                "library_member": self.library_member,
                "book": self.book,
                "status": "Issue",
                "docstatus": 1,
            },
            fields=["date"],
            order_by="creation desc",
            limit=1,
        )

        if not issue_transaction:
            frappe.throw("No issue transaction found for this book")

        issue_date = issue_transaction[0]["date"]  # Get issue date
        return_date = self.date  # Current transaction date is return date

        if not issue_date:
            frappe.throw("Issue date not found for this transaction")

        # Convert to datetime
        issue_date = datetime.strptime(str(issue_date), "%Y-%m-%d")
        return_date = datetime.strptime(str(return_date), "%Y-%m-%d")

        # Ensure return date is not before issue date
        if return_date < issue_date:
            frappe.throw("Return date cannot be before the issue date")

        # Get max allowed days from Library Settings
        max_days_allowed = frappe.db.get_single_value("Library Settings", "max_day_of_book") or 10  # Default: 10 days
        daily_rent = 5  # ₹5 per extra day

        # Calculate number of days used
        days_used = (return_date - issue_date).days

        # Calculate late fees only if overdue
        late_days = max(0, days_used - max_days_allowed)
        late_fee = late_days * daily_rent

        # Save late fee in the transaction
        self.late_return_fees = late_fee

        # Update outstanding fees **only if late fee > 0**
        if late_fee > 0:
            member = frappe.get_doc("Library Membership", {"library_member": self.library_member})
            member.outstanding_fees += late_fee
            member.save()
            frappe.msgprint(f"Late Fee of ₹{late_fee} added for {self.library_member}")

        # Set book status to Available
        book.status = "Available"
        book.save()

    def validate_issue(self):
        self.validate_membership()

        member = frappe.get_doc("Library Membership", {"library_member": self.library_member})
        if member.outstanding_fees > 500 and not member.paid:
            frappe.throw("Member has outstanding fees. Please clear dues before issuing a new book.")

        book = frappe.get_doc("Books", self.book)
        if book.status == "Issued":
            frappe.throw("Book is already issued by another member")

    def validate_maximum_limit(self):
        max_books = frappe.db.get_single_value("Library Settings", "maximum_number_of_issued_articles")
        count = frappe.db.count(
            "Library Transaction",
            {
                "library_member": self.library_member,
                "status": "Issue",
                "docstatus": 1,
            },
        )
        if count >= max_books:
            frappe.throw("Maximum limit reached for issuing articles")

    def validate_membership(self):
        """ Check if a valid membership exists for this library member """
        valid_membership = frappe.db.exists(
            "Library Membership",
            {
                "library_member": self.library_member,
                # "docstatus": 1,
                "from_date": ("<=", self.date),
                "to_date": (">=", self.date),
            },
        )
        if not valid_membership:
            frappe.throw("The member does not have a valid membership")
