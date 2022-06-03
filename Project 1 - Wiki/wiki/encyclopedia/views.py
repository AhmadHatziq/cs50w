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
        
        # Search for matching substring in either title or content. 
        for entry in entries: 
            entry_content = util.get_entry(entry)
            # print(entry_content)
            
            if (search_string.lower()) in (str(entry).lower()): 
                matching_entries.append(entry)
            
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
    
# Handles creating of new pages. 
# If the user goes to /search, user will be presented with the template. 
# If the user submits the FORM data, data will be sent to this function, which will redirect the user to the index page
def create_page(request): 

    if request.method == "POST":
    
        # Editing will call this create_page route. 
        # If editing, will delete the old content before resuming the create page with the content. 
        if 'is_edit' in request.POST.keys():
            print("From EDIT, in CREATE.")
            title = request.POST["title"]
            util.delete_entry(title)
    
        # Extract form parameters
        title = request.POST["title"]
        markdown_content = request.POST["markdown_content"]
        
        # Check if a title already exists 
        current_entries = util.list_entries()
        if title in current_entries: 
            print(f'Unable to add {title} as already exists')
            return render(request, "encyclopedia/index.html", {
                "entries": util.list_entries(), 
                "message": f"ERROR: Unable to add '{title}' as it already exists"
            })
        
        # Add title and content to storage
        print("Adding new content:")
        print(f"Title: {title}")
        print(f"Markdown content: {markdown_content}")
        util.save_entry(title, markdown_content)
        
        # Redirect to index with different message depending on new creation or edit. 
        message = ""
        if 'is_edit' in request.POST.keys():
            message = f"Successfully updated the entry for '{title}'"
        else: 
            message = f"Successfully added entry for '{title}'"
            
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(), 
            "message": message 
        })
    
    else:
        # Case when the user just got to the create page. 
        return render(request, "encyclopedia/create_page.html")

def edit_page(request): 

    if request.method == "POST":
        
        # User will come here by clicking a button (in a form) from each entry page 
        title_to_edit = request.POST["entry_name"]
        markdown_content = util.get_entry_markdown(title_to_edit)
        print(f"User wants to edit {title_to_edit}")
        
        return render(request, "encyclopedia/edit_page.html", {
            "entry_name": title_to_edit, 
            "markdown_content": markdown_content
            })
        
    else: 

        # Returns an error page as user is not supposed to get here without POSTING data
        return render(request, "encyclopedia/index.html", {
                "entries": util.list_entries(), 
                "message": "ERROR with editing route."
            })

