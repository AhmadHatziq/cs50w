from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect 
from django import forms 
from django.urls import reverse 

# Create your views here.

# Declare tasks list as a global variable. Removed in favour of user sessions 
# tasks = ['eat breakfast', 'brush teeth', 'say hello world']


# Declare new task form 
class NewTaskForm(forms.Form): 
    task = forms.CharField(label="New Task")
    priority = forms.IntegerField(label="Priority", min_value=1, max_value=10)

def index(request): 
    # context_dict = {"tasks": tasks}
    
    # Hello world, to test if views.py is working
    # return HttpResponse("Hello Tasks!")
    
    # Create tasklist for a new user session 
    if "tasks" not in request.session: 
        request.session['tasks'] = []
    if request.session['tasks'] is None: 
        request.session['tasks'] = []
    
    # Renders a index.html file located in /templates
    return render(request, "tasks/index.html", {
        "tasks": request.session['tasks']
    })
    
def add(request): 
    
    # Initialize dict with a clean, new form 
    context_dict = {
        'form': NewTaskForm()
    }
    
    # Handles the case when the user had just POST / submitted data via the form 
    if request.method == "POST": 
        form = NewTaskForm(request.POST)
        if form.is_valid(): 
        
            # Extract task and append to current tasklist 
            task = form.cleaned_data["task"]
            request.session["tasks"] += [task]
            
            # Log changes 
            print("Added new task: {}".format(task))
            print("Task list is now: " + str(request.session['tasks']))
            
            # Redirect the user to the tasks page 
            # Get Django to automatically retrieve the URL meant for tasks:index and redirect the user there
            # We want to avoid hardcoding the HTTP routes 
            return HttpResponseRedirect(reverse("tasks:index"))
        else: 
        
            # Form is not valid,return back the form object back to them, with the data they just submitted
            return render(request, "tasks/add.html", context_dict)

    return render(request, "tasks/add.html", context_dict)
    
