from django.urls import path 
from . import views # Use '.' to import from the same directory

urlpatterns = [
    path("", views.index, name="index"),   # This URL pattern has the name index   
    path("brian", views.hello_brian, name="brian"), 
    path("<str:name>", views.greet, name="greet") # This route will take in any string, which has the name 'name' 
                                                  # The function greet can access the parameter with the var name 'name' 
]

