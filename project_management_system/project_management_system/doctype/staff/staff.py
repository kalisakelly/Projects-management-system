import frappe
from frappe.model.document import Document

class Staff(Document):
    def on_submit(self):
        if not self.email or not self.institution:
            frappe.throw("Email and Institution are mandatory to create a user.")
        
        create_user(self.email, self.institution, self.role)

    def autoname(self):
        full_name(self)
    
    def validate(self):
        user=frappe.session.user
        print(user)

def create_user(email, institution, role):
    try:
        if frappe.db.exists("User", email):
            frappe.throw(f"User with email {email} already exists.")

        user = frappe.get_doc({
            "doctype": "User",
            "email": email,
            "first_name": email.split('@')[0],  
            "send_welcome_email": 1,  
            "roles": [{"role": role}]  
        })
        user.insert(ignore_permissions=False)

        frappe.permissions.add_user_permission("Institution", institution, user.name)
        
        frappe.msgprint(f"User {email} created and assigned to {institution}")
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Staff User Creation Error")
        frappe.throw(e)

def full_name(doc):
    full_name = f'{doc.first_name} {doc.last_name}'
    doc.full_name = full_name

def get_permission_query_conditions(user):
    """
    Restrict Staff queries to only show staff within the logged-in user's institution.
    """
    if not user:
        user = frappe.session.user

    user_permissions = frappe.utils.user.get_user_permissions(user)
    if "Institution" in user_permissions:
        # Get the list of institutions the user is allowed to access
        institutions = [perm.get("docname") for perm in user_permissions["Institution"]]
        if institutions:
            institution_list = "', '".join(institutions)
            return f"`tabStaff`.`institution` IN ('{institution_list}')"
    return ""

def has_permission(doc, user):
    """
    Check if the user has permission to view a specific Staff document.
    """
    if not user:
        user = frappe.session.user

    # Fetch user permissions for Institution
    user_permissions = frappe.utils.user.get_user_permissions(user)
    allowed_institutions = [perm.get("docname") for perm in user_permissions.get("Institution", [])]

    # Allow access if the Staff's institution matches an allowed institution
    return doc.institution in allowed_institutions
