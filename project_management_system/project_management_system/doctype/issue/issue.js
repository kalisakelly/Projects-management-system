// Copyright (c) 2024, kalisakelly and contributors
// For license information, please see license.txt

frappe.ui.form.on("Issue", {
  refresh(frm) {
    // Add a custom button to respond to the issue
    frm.add_custom_button("Respond Issue", function () {
      frm.trigger("respond_issue");
    });

    // Fetch districts dynamically when the province is set
    // if (frm.doc.province) {
    //   frm.trigger("fetch_districts");
    // }
  },

  province: function (frm) {
    // Trigger fetching districts when the province is changed
    frm.trigger("fetch_districts");
  },

  fetch_districts(frm) {
    // Ensure province is selected
    if (!frm.doc.province) {
      frappe.msgprint(__('Please select a province to fetch districts.'));
      frm.set_value('district', null); // Clear district if no province
      return;
    }

    frappe.call({
      method: 'project_management_system.project_management_system.doctype.issue.issue.get_districts',
      args: {
        province: frm.doc.province
      },
      callback: function (r) {
        if (r.message) {
          // Populate the district field with options
          frm.set_df_property('district', 'options', r.message);
          frm.set_value('district', r.message[0] || null); // Set the first district as default
        } else {
          frm.set_df_property('district', 'options', []); // Clear options if no results
          frm.set_value('district', null); // Clear district value
        }
      }
    });
  },

  respond_issue(frm) {
    // Create a dialog to prompt for a response comment
    let dialog = new frappe.ui.Dialog({
      title: __('Enter your comment'),
      fields: [
        {
          label: 'Comment',
          fieldname: 'comment',
          fieldtype: 'Small Text',
          reqd: true, // Mark the comment field as required
        }
      ],
      primary_action: function () {
        const comment = dialog.get_value('comment');

        if (!comment) {
          frappe.msgprint(__('Comment is mandatory. Please enter a comment.'));
          return;
        }

        // Call the Frappe method to add the comment
        frappe.call({
          method: "frappe.desk.form.utils.add_comment",
          args: {
            reference_doctype: frm.doctype,
            reference_name: frm.docname,
            content: comment,
            comment_email: frappe.session.user,
            comment_by: frappe.session.user_fullname
          },
          callback: function (r) {
            if (!r.exc) {
              frappe.msgprint(__('Comment added successfully.'));
              dialog.hide();
              frm.reload_doc(); // Reload the document to reflect the comment
            }
          }
        });
      },
      primary_action_label: __('Submit'),
    });

    // Show the dialog
    dialog.show();
  },
});
