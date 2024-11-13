# Copyright (c) 2024, kalisakelly and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Project(Document):
    def validate(self):
       
        if not self.institution:
            frappe.throw("Institution is required for the Project.")

def get_permission_query_conditions(user):
   
    if not user: 
        user = frappe.session.user

    user_permissions = frappe.utils.user.get_user_permissions(user)
    if "Institution" in user_permissions:
        institutions = [perm.get("docname") for perm in user_permissions["Institution"]]
        if institutions:
            institution_list = "', '".join(institutions) 
            return f"`tabProject`.`institution` IN ('{institution_list}')"
    return ""

def has_permission(doc, user):
    """
    Checks whether the logged-in user has permission to access the given Project.
    """
    if not user:
        user = frappe.session.user

    user_permissions = frappe.utils.user.get_user_permissions(user)
    allowed_institutions = [perm.get("docname") for perm in user_permissions.get("Institution", [])]

    return doc.institution in allowed_institutions
