from django.shortcuts import render

from . import util


def index(request):

    # Debug statement. 
    print(util.list_entries())
    # util.list_entries() is ['CSS', 'Django', 'Git', 'HTML', 'Python']

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

