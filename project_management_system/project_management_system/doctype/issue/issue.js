// Copyright (c) 2024, kalisakelly and contributors
// For license information, please see license.txt

frappe.ui.form.on("Issue", {
  refresh(frm) {
    frm.add_custom_button("Respond Issue", function () {
      frm.trigger("respond_issue");
    });
    

    if (frm.doc.level && frm.doc.workflow_state !== "Resolved") {
      frm.add_custom_button("Escalate", function () {
        frappe.call({
          method: "project_management_system.project_management_system.doctype.issue.issue.escalate_issue",
          args: { issue_name: frm.doc.name },
          callback: function (r) {
            if (!r.exc) {
              frm.reload_doc();
            }
          }
        });
      });
    }

    frm.trigger("toggle_email_field");

      if (frm.doc.workflow_state !== "Resolved") {
      frm.add_custom_button("Resolve", function () {
        frappe.call({
          method: "frappe.model.workflow_action.submit",
          args: { doctype: "Issue", name: frm.doc.name },
          callback: function (r) {
            if (!r.exc) {
              frm.reload_doc();
            }
          }
        });
      });
    }
    
  },

  province: function (frm) {
    frm.trigger("fetch_districts");
  },

  fetch_districts(frm) {
    if (!frm.doc.province) {
      frappe.msgprint(__('Please select a province to fetch districts.'));
      frm.set_value('district', null); 
      return;
    }

    frappe.call({
      method: 'project_management_system.project_management_system.doctype.issue.issue.get_districts',
      args: {
        province: frm.doc.province
      },
      callback: function (r) {
        if (r.message) {
          frm.set_df_property('district', 'options', r.message);
          frm.set_value('district', r.message[0] || null); 
        } else {
          frm.set_df_property('district', 'options', []); 
          frm.set_value('district', null);
        }
      }
    });
  },
  receive_updates_from_facilitator(frm) {
    frm.trigger("toggle_email_field");
  },

  toggle_email_field(frm) {
    frm.toggle_display("email", frm.doc.receive_updates_from_facilitator === 1);
  },

  respond_issue(frm) {
    let dialog = new frappe.ui.Dialog({
      title: __('Enter your comment'),
      fields: [
        {
          label: 'Comment',
          fieldname: 'comment',
          fieldtype: 'Small Text',
          reqd: true, 
        }
      ],
      primary_action: function () {
        const comment = dialog.get_value('comment');

        if (!comment) {
          frappe.msgprint(__('Comment is mandatory. Please enter a comment.'));
          return;
        }

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
              frm.reload_doc(); 
            }
          }
        });
      },
      primary_action_label: __('Submit'),
    });

    dialog.show();
  },
});
