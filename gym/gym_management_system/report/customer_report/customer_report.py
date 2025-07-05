# Copyright (c) 2025, Sneha and contributors
# For license information, please see license.txt

# import frappe


# def execute(filters=None):
# 	columns, data = [], []
# 	return columns, data

import frappe

def execute(filters=None):
    columns = [
        {"label": "Member ID", "fieldname": "name", "fieldtype": "Data", "width": 100},
        {"label": "Name", "fieldname": "name1", "fieldtype": "Data", "width": 150},
        {"label": "Contact", "fieldname": "contact", "fieldtype": "Phone", "width": 120},
        {"label": "Email", "fieldname": "email_id", "fieldtype": "Data", "width": 180},
        {"label": "Gender", "fieldname": "gender", "fieldtype": "Data", "width": 80},
        {"label": "Plan", "fieldname": "plans", "fieldtype": "Data", "width": 120},
        {"label": "Joining Date", "fieldname": "joining_date", "fieldtype": "Date", "width": 120},
        {"label": "Ending Date", "fieldname": "ending_date", "fieldtype": "Date", "width": 120},
    ]

    data = []

    if filters and filters.get("name1"):
        membership = frappe.get_all(
            "Gym Membership",
            filters={"name1": filters.get("name1")},
            fields=[
                "name", "name1", "contact", "email_id", "gender",
                "plans", "joining_date", "ending_date"
            ]
        )
        data = membership

    return columns, data

