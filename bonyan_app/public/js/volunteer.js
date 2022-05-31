
frappe.ui.form.on("Volunteer", {
    refresh: function(frm) {

    frm.set_query("governorate_location", {"is_group": 1, "location_type" : 'Governorate'});

    frm.set_query("district_location", function() {
    return {
      filters: {
      parent_location: frm.doc.governorate_location ? frm.doc.governorate_location: ' ',
      location_type:"District",
        }
      }
    });

    frm.set_query("subdistrict_location", function() {
    return {
      filters: {
      parent_location: frm.doc.district_location ? frm.doc.district_location: ' ',
      location_type:"Subdistrict",
    }
    }
    });
    frm.set_query("location", function() {
    return {
      filters: {
      parent_location: frm.doc.subdistrict_location ? frm.doc.subdistrict_location: ' ',

      location_type:"Location",
      }
    }
    });
    }
});