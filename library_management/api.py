
import requests   # API se data fetch karne ke liye 
import frappe  

# url = "https://frappe.io/api/method/frappe-library?page=1"  # API endpoint
# response = requests.get(url)  # API call

# if response.status_code == 200:  # Agar API successfully call ho gayi
#     data = response.json()  # JSON response ko parse karein
#     print(data)  # Pure response ko print karein
# else:
#     print("Failed to fetch data")  # Agar API fail ho gayi to error show karein


@frappe.whitelist()    # Is function ko API me accessible banane ke liye
def import_books(title=None):  
    settings = frappe.get_single("Library Settings")  
    last_page = settings.get("last_imported_page") or 0  
    page = last_page + 1  

    url = f"https://frappe.io/api/method/frappe-library?page={page}"
    # Agar librarian filter lagaye (title, author), to URL me add karein
    if title:
        url += f"&title={title}"

    # API Call 
    response = requests.get(url)
    # Response Check
    if response.status_code == 200:  
        data = response.json().get("message", [])[:20] # JSON response se "message" fetch karein

        if not data:  
            frappe.msgprint("No more books to import!")
            return "No more books to import"
        # Har book ko database me save karein
        for book in data:
            if not frappe.db.exists("Books", {"isbn": book["isbn"]}):  
                frappe.get_doc({
                    "doctype": "Books", # Books Doctype me insert karna hai
                    "book_name": book["title"],
                    "author": book["authors"],
                    "isbn": book["isbn"],
                    "publisher": book["publisher"],
                    "quantity": 5,
                    # "num_pages": book["num_pages"],  
                    # "image": book["image_url"],  
                    # "description": book["description"],  
                    # "status": book["availability"], 
                }).insert()
        
        settings.db_set("last_imported_page", page)
        frappe.msgprint(f"Books Imported successfully")
        return f"Books imported successfully from Page {page}"

    return "Failed to fetch books"  # Agar API call fail ho to message return karein

