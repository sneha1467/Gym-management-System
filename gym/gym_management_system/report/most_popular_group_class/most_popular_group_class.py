import frappe

def execute(filters=None):
    columns = [
        {
            "label": "Class (Category)",
            "fieldname": "specialization",
            "fieldtype": "Data",
            "width": 300
        },
        {
            "label": "Total Bookings",
            "fieldname": "total",
            "fieldtype": "Int",
            "width": 150
        }
    ]

    data = frappe.db.sql("""
        SELECT
            c.specialization,
            COUNT(*) AS total
        FROM `tabGym Class Booking` b
        JOIN `tabCategory` c ON b.class_boooking = c.name
        WHERE b.class_boooking IS NOT NULL
        GROUP BY c.specialization
        ORDER BY total DESC
    """, as_dict=True)

    chart = {
        "data": {
            "labels": [row["specialization"] for row in data],
            "datasets": [
                {
                    "name": "Total Bookings",
                    "values": [row["total"] for row in data]
                }
            ]
        },
        "type": "bar",
        "colors": ["#00AEEF"]
    }

    return columns, data, None, chart
