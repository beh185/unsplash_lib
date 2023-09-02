# Github: https://github.com/beh185
# Telegram: https://T.me/dr_xz
# e-mail: BehnamH.dev@gmail.com
# ____________________________________________

# ======== # Import Modules # ======== #
try:
    from os import system, path, name
    from requests import get, post ,ConnectionError, ReadTimeout
    from urllib.request import urlretrieve
    from urllib.error import URLError
except ImportError:
    exit("[+] Please Install the required modules by running setup.py file!")

# =========== # Functions # =========== #

# ======== # Checking for http errors # ======== #
def __check_http_error__(respond):
    if(respond.status_code == 400):
        exit("[400 Error] The request was unacceptable, often due to missing a required parameter")
    elif(respond.status_code == 401):
        exit("[401 Error] Invalid Access Token")
    elif(respond.status_code == 403):
        exit("[403 Error] Missing permissions to perform request")
    elif(respond.status_code == 404):
        exit("[404 Error] The requested resource doesn't exist")
    elif(respond.status_code == 500 or respond.status_code == 503):
        exit(f"[{respond.status_code} Error] Something went wrong on unsplash's end")
    else:
        exit(f"[{respond.status_code} Error] Something went wrong")

# ======== # Downloading Images results for a query. # ======== #
def search_photo(client_id = str(), query = str(), page = int(), per_page = int(), order_by = str(), collections = str(), content_filter = str(), color = str(), orientation = str(), _DownloadImg=True, _FileName: str = 'S-image', _Path = str()):
    payload = {
        'client_id': client_id,
        'query': query,
        'page': page,
        'per_page': per_page,
        'order_by': order_by,
        'collections': collections,
        'content_filter': content_filter,
        'color': color,
        'orientation': orientation}
    # ======== # Making copy to prevent RuntimeError: dictionary changed size during iteration # ======== #
    PayLoad = payload.copy()

    # ====== # Removing values that user didn't specified # ====== #
    for key, value in payload.items():
        if (value == '' or value == 0):
            PayLoad.pop(key)
    
    # ======== # Checking requirement var # ======== #
    if ('client_id' not in PayLoad.keys()):
        exit('download_collection() missing 1 required positional argument. Please specify client_id')
    if ('query' not in PayLoad.keys()):
        exit('download_collection() missing 1 required positional argument. Please specify query')
    
    unsplash_api = 'https://api.unsplash.com/search/photos'
    try:
        JsonImg = get(unsplash_api, allow_redirects=True, timeout=25, params=PayLoad)
    except ConnectionError:
        exit("Connection Failed. It's might because of your network connection")
    except KeyboardInterrupt:
        exit('\nOperation canceled by user')
    except ReadTimeout:
        exit('Time out reached')
        
    # ======== # Checking for http errors # ======== #
    if(JsonImg.status_code != 200):
        __check_http_error__(JsonImg)
    else:
        JsonImg = JsonImg.json()
        
    # ======= # Download images# ======= #
    if(_DownloadImg):
        print('Downloading images ...')
        if(_Path != str()):
            if(path.exists(_Path) == False):
                exit(f'"{_Path}" is not exist')

            if(name == 'nt' and _Path.endswith('\\') == False):
                _Path = _Path + '\\'
            elif(name == 'posix' and _Path.endswith('/') == False):
                _Path = _Path + '/'

        for i in range(per_page):
            ImgLink = JsonImg['results'][i]['urls']['full']
            try:
                urlretrieve(ImgLink, f"{_Path}{_FileName}-{i}.jpg")
            except URLError:
                exit('Error! It might be because of the network problem or your setting issues, such as proxy setting')
    else:
        return JsonImg
    
# ========== # Retrieve a collection’s photos. # ========== #
def download_collection(client_id = str(), id = str(), page = int, per_page = int, orientation = str(), _DownloadImg = True, _FileName = 'C-image', _Path = str()):
    payload = {
        'client_id': client_id,
        'page': page,
        'per_page': per_page,
        'orientation':orientation}
    # ======== # Making copy to prevent RuntimeError: dictionary changed size during iteration # ======== #
    PayLoad = payload.copy()

    # ====== # Removing values that user didn't specified # ====== #
    for key, value in payload.items():
        if (value == '' or value == 0):
            PayLoad.pop(key)

    # ======== # Checking requirement var # ======== #
    if ('client_id' not in PayLoad.keys()):
        exit('download_collection() missing 1 required positional argument. Please specify client_id')
    if(id == str()):
        exit('download_collection() missing 1 required positional argument. Please specify id')

    unsplash_api = f'https://api.unsplash.com/collections/{str(id)}/photos'
    try:
        JsonImg = get(unsplash_api, allow_redirects=True, timeout=25, params=PayLoad)
    except ConnectionError:
        exit("Connection Failed. It's might because of your network connection")
    except KeyboardInterrupt:
        exit('\nOperation canceled by user')
    except ReadTimeout:
        exit('Time out reached')
    
    # ======== # Checking for http errors # ======== #
    if(JsonImg.status_code != 200):
        __check_http_error__(JsonImg)
    else:
        JsonImg = JsonImg.json()
        
    # ======= # Download images# ======= #
    if(_DownloadImg):
        print('Downloading images ...')
        if(_Path != str()):
            if(path.exists(_Path) == False):
                exit(f'"{_Path}" is not exist')

            if(name == 'nt' and _Path.endswith('\\') == False):
                _Path = _Path + '\\'
            elif(name == 'posix' and _Path.endswith('/') == False):
                _Path = _Path + '/'
        for i in range(per_page):
            ImgLink = JsonImg[i]['urls']['full']
            try:
                urlretrieve(ImgLink, f"{_Path}{_FileName}-{i}.jpg")
            except URLError:
                exit('Error! It might be because of the network problem or your setting issues, such as proxy setting')
            except KeyboardInterrupt:
                exit('\nOperation canceled by user')
    else:
        return JsonImg


def get_collections_id(client_id = str(), query = str(), page = int(), per_page = int()):
    payload = {
        'client_id': client_id,
        'query':query,
        'page': page,
        'per_page':per_page}
    # ======== # Making copy to prevent RuntimeError: dictionary changed size during iteration # ======== #
    PayLoad = payload.copy()

    # ====== # Removing values that user didn't specified # ====== #
    for key, value in payload.items():
        if (value == '' or value == 0):
            PayLoad.pop(key)
    
    # ======== # Checking requirement var # ======== #
    if ('client_id' not in PayLoad.keys()):
        exit('download_collection() missing 1 required positional argument. Please specify client_id')
    if ('query' not in PayLoad.keys()):
        exit('download_collection() missing 1 required positional argument. Please specify query')

    unsplash_api = 'https://api.unsplash.com/search/collections'
    try:
        JsonData = get(unsplash_api, allow_redirects=True, timeout=25, params=PayLoad)
    except ConnectionError:
        exit("Connection Failed. It's might because of your network connection")
    except KeyboardInterrupt:
        exit('\nOperation canceled by user')
    except ReadTimeout:
        exit('Time out reached')
    
    # ======== # Checking for http errors # ======== #
    if(JsonData.status_code != 200):
        __check_http_error__(JsonData)
    else:
        JsonData = JsonData.json()
    
    # ======= # Returning collection id # ======= #
    id_list : list = list()
    for i in range(per_page):
        id_list.append(JsonData['results'][i]['id'])
    return(id_list)

# ======== # Get a single page of user results for a query # ======== #
def search_users(client_id = str(), query = str(), page = int(), per_page = int()):
    payload = {
        'client_id': client_id,
        'query':query,
        'page': page,
        'per_page':per_page}
    # ======== # Making copy to prevent RuntimeError: dictionary changed size during iteration # ======== #
    PayLoad = payload.copy()

    # ====== # Removing values that user didn't specified # ====== #
    for key, value in payload.items():
        if (value == '' or value == 0):
            PayLoad.pop(key)
    
    # ======== # Checking requirement var # ======== #
    if ('client_id' not in PayLoad.keys()):
        exit('download_collection() missing 1 required positional argument. Please specify client_id')
    if ('query' not in PayLoad.keys()):
        exit('download_collection() missing 1 required positional argument. Please specify query')
    
    unsplash_api = 'https://api.unsplash.com/search/users'
    
    try:
        JsonData = get(unsplash_api, allow_redirects=True, timeout=25, params=PayLoad)
    except ConnectionError:
        exit("Connection Failed. It's might because of your network connection")
    except KeyboardInterrupt:
        exit('\nOperation canceled by user')
    except ReadTimeout:
        exit('Time out reached')
    
    # ======== # Checking for http errors # ======== #
    if(JsonData.status_code != 200):
        __check_http_error__(JsonData)
    else:
        JsonData = JsonData.json()
    
    return JsonData['results']

# ======= # Create a new collection. This requires the write_collections scope that can be activated on your api.unsplash.com account # ======= #
def create_collection(client_id = str(), title = str(), description = str(), private = False):
    payload = {
        'client_id': client_id,
        'title': title,
        'description':description,
        'private': private}
    # ======== # Making copy to prevent RuntimeError: dictionary changed size during iteration # ======== #
    PayLoad = payload.copy()

    # ====== # Removing values that user didn't specified # ====== #
    for key, value in payload.items():
        if (value == '' or value == 0):
            PayLoad.pop(key)
    
    # ======== # Checking requirement var # ======== #
    if ('client_id' not in PayLoad.keys()):
        exit('download_collection() missing 1 required positional argument. Please specify client_id')
    if ('title' not in PayLoad.keys()):
        exit('download_collection() missing 1 required positional argument. Please specify title')
        
    unsplash_api = 'https://api.unsplash.com/collections'
    
    try:
        JsonData = post(unsplash_api, allow_redirects=True, timeout=25, params=PayLoad)
    except ConnectionError:
        exit("Connection Failed. It's might because of your network connection")
    except KeyboardInterrupt:
        exit('\nOperation canceled by user')
    except ReadTimeout:
        exit('Time out reached')
    
    # ======== # Checking for http errors # ======== #
    if(JsonData.status_code != 200):
        __check_http_error__(JsonData)
    else:
        JsonData = JsonData.json()

    return JsonData