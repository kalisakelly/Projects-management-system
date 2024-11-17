// Copyright (c) 2024, kalisakelly and contributors
// For license information, please see license.txt

frappe.ui.form.on("Project", {
  refresh(frm) {
    frm.add_custom_button("New Issue", function () {
      frm.trigger("create_issue");
    });
  },

  create_issue(frm) {
    frappe.new_doc("Issue", {
      project: frm.doc.name,
      institution: frm.doc.institution
    });
  },
});
