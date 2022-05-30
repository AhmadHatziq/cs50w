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
    
    # Create context dictionary 
    context_dict = {
        "html_content": html_content, 
        "entry_name": title
    }
    
    return render(request, "encyclopedia/wiki_entry.html", context_dict)
    

