frappe.listview_settings['Books'] = {
    onload: function(listview) {

        listview.page.add_inner_button('Import Books', function() {
            console.log("Import Books Button Clicked");
            frappe.call({
                method: "library_management.api.import_books",
                callback: function(response) {
                    console.log("API Response:", response);
                    listview.refresh();
                }
            });
        });

        console.log("Button Added Successfully");
    }
};
