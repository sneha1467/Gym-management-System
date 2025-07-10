import frappe
from frappe.auth import LoginManager
from frappe import _

@frappe.whitelist()
def authenticate_user(email, password, role):
    """Authenticate the user using email, password, and role."""
    
   
    gym_member = frappe.get_all(
        "Gym Members", 
        filters={"email": email}, 
        fields=["name1", "role", "password"] 
    )

    if not gym_member:
        return {"success": False, "message": "Invalid email"}  

    
    stored_password = gym_member[0]["password"]
    
    
    if stored_password != password:
        return {"success": False, "message": "Invalid password"}  
    

    if gym_member[0]["role"] != role:
        return {"success": False, "message": "Invalid role"}  

   
    return {"success": True, "message": "Authentication successful", "role": gym_member[0]["role"]}


import frappe
from datetime import datetime

@frappe.whitelist(allow_guest=True)
def get_member_details(email):

  
    membership = frappe.get_doc("Gym Membership", email)

  
    today = datetime.today().date()
    ending_date = membership.ending_date
    remaining_days = (ending_date - today).days if ending_date else None

   
    booking = frappe.get_all("Gym Class Booking",
                             filters={"email": email},
                             fields=["trainer_name"],
                             limit_page_length=1)

    trainer_name = booking[0].trainer_name if booking else None
    trainer_info = {}
    
    if trainer_name:
        trainer = frappe.get_doc("TrainerReg", trainer_name)
        trainer_info = {
            "name": trainer.name,
            "email_id": trainer.email_id,
            "contact_no": trainer.contact_no,
            "address": trainer.address,
            "gender": trainer.gender
        }

    return {
        "email": membership.email_id,
        "contact": membership.contact,
        "plan": membership.plans,
        "joining_date": membership.joining_date,
        "ending_date": membership.ending_date,
        "remaining_days": remaining_days,
        "trainer": trainer_info
    }
