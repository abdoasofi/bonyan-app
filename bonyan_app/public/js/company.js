frappe.ui.form.on('Company', {
    refresh: function(frm){
        frm.set_query('default_employee_covenant_account', () =>
         { return { filters: {company: frm.doc.name, root_type: "Asset"} } });
    },

});