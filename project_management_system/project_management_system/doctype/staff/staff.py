import frappe
from frappe.model.document import Document

class Staff(Document):
    def on_submit(self):
        if not self.email or not self.institution:
            frappe.throw("Email and Institution are mandatory to create a user.")

        create_user(self.email, self.institution, "Translator")  

def create_user(email, institution, role):
    try:
        if frappe.db.exists("User", email):
            frappe.throw(f"User with email {email} already exists.")

        # Create user
        user = frappe.get_doc({
            "doctype": "User",
            "email": email,
            "first_name": email.split('@')[0],  
            "send_welcome_email": 1,  
            "roles": [{"role": role}]  
        })
        user.insert(ignore_permissions=True)

        frappe.permissions.add_user_permission("Institution", institution, user.name)
        
        frappe.msgprint(f"User {email} created and assigned to {institution}")
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Staff User Creation Error")
        frappe.throw(f"An error occurred while creating the user: {str(e)}")
