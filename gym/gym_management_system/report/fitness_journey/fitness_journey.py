import frappe

def execute(filters=None):
    if not filters or not filters.get("member"):
        frappe.logger().info("No member filter provided.")
        return [], [], None, None

    member = filters.get("member")
    frappe.logger().info(f"Fetching BMI for member email: {member}")

    bmi_name = frappe.db.get_value("BMI", {"email": member}, "name")
    if not bmi_name:
        frappe.logger().info(f"No BMI record found for {member}")
        return [], [], None, None

    data = frappe.db.sql("""
        SELECT date, weight, height, calories, bmi
        FROM `tabMetric Update`
        WHERE parent = %s
        ORDER BY date ASC
    """, (bmi_name,), as_dict=True)

    if not data:
        frappe.logger().info(f"No Metric Update data for BMI {bmi_name}")
        return [], [], None, None

    # Clean data - replace None with 0 or reasonable default
    for row in data:
        for key in ['weight', 'height', 'calories', 'bmi']:
            if row[key] is None:
                frappe.logger().info(f"Null value found in {key} for date {row['date']}, setting to 0")
                row[key] = 0

    columns = [
        {"label": "Date", "fieldname": "date", "fieldtype": "Date", "width": 100},
        {"label": "Weight (kg)", "fieldname": "weight", "fieldtype": "Float", "width": 100},
        {"label": "Height (cm)", "fieldname": "height", "fieldtype": "Float", "width": 100},
        {"label": "Calories", "fieldname": "calories", "fieldtype": "Float", "width": 100},
        {"label": "BMI", "fieldname": "bmi", "fieldtype": "Float", "width": 100},
    ]

    labels = [row["date"].strftime("%Y-%m-%d") if hasattr(row["date"], "strftime") else str(row["date"]) for row in data]

    # Debug print labels and dataset lengths
    frappe.logger().info(f"Labels count: {len(labels)}")
    frappe.logger().info(f"Weight data count: {len([row['weight'] for row in data])}")
    frappe.logger().info(f"Calories data count: {len([row['calories'] for row in data])}")
    frappe.logger().info(f"BMI data count: {len([row['bmi'] for row in data])}")

    chart = {
        "data": {
            "labels": labels,
            "datasets": [
                {"name": "Weight", "values": [row["weight"] for row in data]},
                {"name": "Calories", "values": [row["calories"] for row in data]},
                {"name": "BMI", "values": [row["bmi"] for row in data]},
            ]
        },
        "type": "line",
        "line_options": {
            "curve": "linear",
            "fill": 0,
        },
        "colors": ["#FF5733", "#33C3FF", "#33FF57"]
    }

    return columns, data, None, chart
