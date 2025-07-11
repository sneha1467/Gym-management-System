import frappe
from frappe.utils import nowdate, getdate

@frappe.whitelist()
def get_member_details():
    user_email = frappe.session.user


    gym_member_name = frappe.get_value("Gym Members", {"email": user_email}, "name")
    if not gym_member_name:
        return {}

 
    membership = frappe.get_all(
        'Gym Membership',
        filters={'email_id': gym_member_name},
        limit=1,
        order_by='creation desc',
        fields=['email_id', 'contact', 'plans', 'joining_date', 'ending_date']
    )

    if not membership:
        return {}

    member = membership[0]

 
    remaining_days = None
    if member.get('ending_date'):
        remaining_days = (getdate(member['ending_date']) - getdate(nowdate())).days

  
    booking = frappe.get_all(
        'Gym Class Booking',
        filters={'email': user_email},
        limit=1,
        order_by='creation desc',
        fields=['trainer_name']
    )

    trainer_name = booking[0]['trainer_name'] if booking else 'N/A'

    return {
        "email": user_email,
        "contact": member.get('contact'),
        "plan": member.get('plans'),
        "joining_date": member.get('joining_date'),
        "ending_date": member.get('ending_date'),
        "remaining_days": remaining_days,
        "trainer": {
            "name": trainer_name
        }
    }
