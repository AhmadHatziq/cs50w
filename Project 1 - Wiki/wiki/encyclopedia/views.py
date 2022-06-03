from django.shortcuts import render

from . import util


def index(request):

    # Debug statement. 
    # print(util.list_entries())
    # util.list_entries() is ['CSS', 'Django', 'Git', 'HTML', 'Python']

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def display_entry(request, title): 
    
    # Get html content of markdown file 
    html_content = util.get_entry(title)
    
    if html_content is not None: 
    
        # Create context dictionary 
        context_dict = {
            "html_content": html_content, 
            "entry_name": title
        }
        
        return render(request, "encyclopedia/wiki_entry.html", context_dict)
        
    else: 
        # Display error page 
        # print(f"Error for {title}")
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(), 
            "message": f"Specified entry for '{title}' does not exist. Please choose from the list below."
            })
    
# Handles /search, which is called when the FORM POSTS data     
def search(request): 
    if request.method == "POST":
    
        # Extract search string inputted by user
        search_string = request.POST["q"]
        # print(f"Search string is: {search_string}")
        
        # Get queries that match the search string 
        entries = util.list_entries()
        matching_entries = []
        for entry in entries: 
            entry_content = util.get_entry(entry)
            # print(entry_content)
            
            if (search_string.lower()) in (str(entry_content).lower()): 
                matching_entries.append(entry)

        # Redirect to index if no matching queries found
        if len(matching_entries) == 0: 
            return render(request, "encyclopedia/index.html", {
                "entries": matching_entries, 
                "message": f"No matching entries found for search term '{search_string}'"
                })
                
        # If there is only 1 matching entry, redirect to that page. 
        # Else, display a list of matching entries. 
        if len(matching_entries) == 1: 
            matching_entry = matching_entries[0]
            context_dict = {
                "html_content": util.get_entry(matching_entry),
                "entry_name": matching_entry
            }
        
            return render(request, "encyclopedia/wiki_entry.html", context_dict)
        
        # Last case, where there are multuple search results. 
        # Show the index page, but only for matching entries. 
        return render(request, "encyclopedia/index.html", {
            "entries": matching_entries,
            "message": f"Below are the entries that containt the search term '{search_string}'"
        })
        
    else: 
        # User got to /search without POSTING data. 
        # Redirect to /index with error message. 
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(), 
            "message": "Error, no search term detected. Please enter search term into form again"
        })
    

