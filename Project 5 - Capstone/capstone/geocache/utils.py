import os 

def load_google_maps_API_key(): 
    '''
    Loads the Google Maps API key from the local directory. 
    Looks for either the file called 'GOOGLE_MAPS_API.txt' or 'google_maps_api_key.txt'. 
    '''

    current_directory = os.path.dirname(__file__)
    api_folder = os.path.join(current_directory, 'api_key')

    for file in os.listdir(api_folder): 
        os.chdir(api_folder)
        with open(file, 'r') as f: 
            extracted_api_key = f.read() 
            if len(extracted_api_key) > 1 and 'replace' not in extracted_api_key.lower(): 
                print('LOADED GOOGLE MAPS API KEY:', extracted_api_key, '\n')
                return extracted_api_key

    # Print error message as no API key found. 
    print('UNABLE TO FIND ANY API KEY STRINGS in: ', api_folder)
    quit()
    
