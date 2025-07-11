# Copyright (c) 2025, Sneha
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class GymMembers(Document):
    def after_insert(self):
        self.create_user()

    def create_user(self):
        if not self.email:
            frappe.throw("Email is required to create user.")

     
        if frappe.db.exists("User", self.email):
            frappe.msgprint(f"User {self.email} already exists.")
            return

        
        user_type = "System User" if self.role == "Gym Admin" else "Website User"

        
        user = frappe.get_doc({
            "doctype": "User",
            "email": self.email,
            "first_name": self.name1,  
            "user_type": user_type,
            "send_welcome_email": 0,
            "new_password": self.password  
        })

        
        if self.role:
            user.append("roles", {"role": self.role})

      
        user.insert(ignore_permissions=True)
        frappe.msgprint(f"User {self.email} created with role {self.role}.")
