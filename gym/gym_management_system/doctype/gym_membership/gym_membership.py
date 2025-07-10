# Copyright (c) 2025, Sneha and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document

class GymMembership(Document):
    def validate(self):
        if self.assign_locker == "Yes" and self.locker_available:
            existing = frappe.db.exists("Gym Membership",
                {"assign_locker": "Yes", "locker_available": self.locker_available, "name": ("!=", self.name)})
            if existing:
                frappe.throw(_("Locker {0} is already assigned to another member.").format(self.locker_available))


@frappe.whitelist()
def get_available_lockers(doctype, txt, searchfield, start, page_len, filters):
    assigned_lockers = frappe.db.sql_list("""
        SELECT locker_available FROM `tabGym Membership`
        WHERE assign_locker='Yes' AND locker_available IS NOT NULL
    """)
    frappe.logger().debug(f"Assigned Lockers: {assigned_lockers}")

    if not assigned_lockers:
        assigned_lockers = ['']

    lockers = frappe.db.sql("""
        SELECT name FROM `tabLocker Available`
        WHERE name NOT IN ({assigned})
        AND name LIKE %s
        LIMIT %s OFFSET %s
    """.format(assigned=','.join(['%s']*len(assigned_lockers))),
    tuple(assigned_lockers) + ('%' + txt + '%', page_len, start), as_dict=1)

    frappe.logger().debug(f"Available Lockers: {lockers}")

    return lockers
