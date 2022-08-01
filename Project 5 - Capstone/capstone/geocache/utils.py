import os 

def load_google_maps_API_key(): 
    '''
    Loads the Google Maps API key from the local machine. 
    '''
    FILE_PATH = r"C:\\API_KEYS\\GOOGLE_MAPS_API.txt"
    
    API_KEY = ""
    with open(FILE_PATH, 'r') as f: 
        API_KEY = (f.read())
        return API_KEY