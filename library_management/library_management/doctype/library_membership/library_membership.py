# Copyright (c) 2025, kumkum  and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class LibraryMembership(Document):
    def validate(self):
        if self.from_date and self.to_date and self.from_date > self.to_date:
            frappe.throw("End Date should be greater than Start Date")
            
    # check before submitting this document
    def before_save(self):
        exists = frappe.db.exists(
            "Library Membership",
            {
                "library_member": self.library_member,
                "docstatus": 1,
                # check if the membership's end date is later than this membership's start date
                "to_date": (">", self.from_date),
            },
        )
        if exists:
            frappe.throw("There is an active membership for this member")

        # get loan period and compute to_date by adding membership_period to from_date
        membership_period = frappe.db.get_single_value("Library Settings", "membership_period")
        self.to_date = frappe.utils.add_days(self.from_date, membership_period or 30)


