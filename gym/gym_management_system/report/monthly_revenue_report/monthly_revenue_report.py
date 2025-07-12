import frappe from datetime import datetime

def execute(filters=None):
    # Fetch raw joining_date and final_price
    data_raw = frappe.db.sql("""
        SELECT joining_date, final_price
        FROM `tabGym Membership`
        WHERE docstatus < 2 AND joining_date IS NOT NULL
    """, as_dict=True)

    # Aggregate revenue per month in Python
    revenue_by_month = {}
    for row in data_raw:
        month = row['joining_date'].strftime("%Y-%m")
        revenue_by_month[month] = revenue_by_month.get(month, 0) + row['final_price']

    # Convert dict to list of dicts sorted by month
    data = [{"month": month, "total_revenue": revenue_by_month[month]} for month in sorted(revenue_by_month)]

    columns = [
        {"label": "Month", "fieldname": "month", "fieldtype": "Data", "width": 150},
        {"label": "Total Revenue ₹", "fieldname": "total_revenue", "fieldtype": "Currency", "width": 200},
    ]

    chart = {
        "data": {
            "labels": [row["month"] for row in data],
            "datasets": [{
                "name": "Total Revenue",
                "values": [row["total_revenue"] for row in data]
            }]
        },
        "type": "bar",
        "colors": ["#36B37E"],
        "height": 300
    }

    return columns, data, None, chart
