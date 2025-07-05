
import frappe
import json
@frappe.whitelist()
def get_filtered_trainers(doctype, txt, searchfield, start, page_len, filters=None):
    import json

    if filters and isinstance(filters, str):
        filters = json.loads(filters)
    elif not filters:
        filters = {}

    specialization = filters.get('specialization')
    conditions = []
    values = []

    if specialization:
        conditions.append("specialization = %s")
        values.append(specialization)

    start = int(start)
    page_len = int(page_len)

    query = f"""
        SELECT name, name1 FROM `tabTrainerReg`
        WHERE {searchfield} LIKE %s
    """

    values = [f"%{txt}%"] + values

    if conditions:
        query += " AND " + " AND ".join(conditions)

    query += " LIMIT %s OFFSET %s"
    values += [page_len, start]

    results = frappe.db.sql(query, values, as_dict=True)


    mapped_results = [{"value": r["name"], "label": r["name1"]} for r in results]

    return mapped_results




import frappe
from frappe import _

@frappe.whitelist()
def get_membership_report(member_id):
    try:
        if not member_id:
            return None

       
        if frappe.db.exists("Gym Membership", member_id):
            membership = frappe.get_doc("Gym Membership", member_id)

            return {
                "name1": membership.get("name1"),
                "contact": membership.get("contact"),
                "email_id": membership.get("email_id"),
                "joining_date": membership.get("joining_date"),
                "ending_date": membership.get("ending_date")
            }

       
        result = frappe.get_all(
            "Gym Membership",
            filters={"name1": ["like", f"%{member_id}%"]},
            fields=["name1", "contact", "email_id", "joining_date", "ending_date"],
            limit=1
        )
        if result:
            return result[0]

        return None

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), " Customer Report API Error")
        frappe.throw(_("Something went wrong while generating the report."))
