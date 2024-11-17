# Copyright (c) 2024, kalisakelly and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from rwanda import get_provinces, get_districts, get_sectors, get_cells, get_villages


class Issue(Document):
    pass

def get_permission_query_conditions(user):
    """
    Restrict Issue queries to show only issues at or below the user's level.
    """
    staff = frappe.db.get_value("Staff", {"email": user}, ["level", "institution"], as_dict=True)

    if staff:
        level = staff.get("level")
        institution = staff.get("institution")
        return f"""
            `tabIssue`.`level` <= '{level}' AND `tabIssue`.`institution` = '{institution}'
        """
    return ""

def has_permission(doc, user):
    """
    Ensure the user can only view or act on issues within their level and institution.
    """
    staff = frappe.db.get_value("Staff", {"email": user}, ["level", "institution"], as_dict=True)

    if staff:
        return doc.level <= staff.get("level") and doc.institution == staff.get("institution")
    return False

# @frappe.whitelist()
# def get_districts(province):
#     """
#     Fetch districts for the selected province.
#     """
#     if not province:
#         frappe.throw("Province is required to fetch districts.")
    
#     try:
#         districts = get_districts(province)
#         return districts
#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), "Error fetching districts")
#         frappe.throw(e)

@frappe.whitelist()
def escalate_issue(issue_name):
    """
    Escalate the issue to the next level, if possible.
    """
    issue = frappe.get_doc("Issue", issue_name)
    current_level = issue.level

    # Map escalation levels
    escalation_flow = {
        "1": "2",
        "2": "3",
        "3": None  # No further escalation
    }

    next_level = escalation_flow.get(current_level)

    if not next_level:
        frappe.throw("This issue is already at the highest level and cannot be escalated further.")

    # Find staff at the next level
    next_staff = frappe.get_all(
        "Staff",
        filters={
            "level": next_level,
            "institution": issue.institution
        },
        limit=1
    )

    if not next_staff:
        frappe.throw(f"No staff available at {next_level} in this institution.")

    # Assign the issue to the next level and update fields
    issue.level = next_level
    issue.status = "Escalated"
    issue.save()

    frappe.msgprint(f"Issue escalated to {next_level} and assigned to {next_staff[0]}.")
