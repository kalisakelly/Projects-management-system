# Copyright (c) 2024, kalisakelly and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from rwanda import get_provinces, get_districts, get_sectors, get_cells, get_villages


class Issue(Document):
    pass

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