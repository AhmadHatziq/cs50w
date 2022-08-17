import os 

def load_google_maps_API_key(): 
    '''
    Loads the Google Maps API key from the local directory. 
    '''

    current_directory = os.path.dirname(__file__)
    target_file = os.path.join(current_directory, 'api_key', 'GOOGLE_MAPS_API.txt')

    print(target_file)
    with open(target_file, 'r') as f: 
        extracted_api_key = f.read() 
        print('LOADED GOOGLE MAPS API KEY:', extracted_api_key, '\n')
        return extracted_api_key
