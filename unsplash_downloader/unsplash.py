# Github: https://github.com/beh185
# Telegram: https://T.me/dr_xz
# e-mail: BehnamH.dev@gmail.com
# ____________________________________________

# ======== # Import Modules # ======== #
try:
    from os import system, path, name
    from requests import get, ConnectionError, ReadTimeout
    from urllib.request import urlretrieve
    from urllib.error import URLError
except ImportError:
    exit("[+] Please Install the required modules by running setup.py file!")

# =========== # Functions # =========== #

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
        
# ======== # Checking for errors # ======== #
    if(JsonImg.status_code != 200):
        if(JsonImg.status_code == 400):
            exit("[400 Error] The request was unacceptable, often due to missing a required parameter")
        elif(JsonImg.status_code == 401):
            exit("[401 Error] Invalid Access Token")
        elif(JsonImg.status_code == 403):
            exit("[403 Error] Missing permissions to perform request")
        elif(JsonImg.status_code == 404):
            exit("[404 Error] The requested resource doesn't exist")
        elif(JsonImg.status_code == 500 or JsonImg.status_code == 503):
            exit(f"[{JsonImg.status_code} Error] Something went wrong on unsplash's end")
        else:
            exit(f"[{JsonImg.status_code} Error] Something went wrong")
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
    
    # ======== # Checking for errors # ======== #
    if(JsonImg.status_code != 200):
        if(JsonImg.status_code == 400):
            exit("[400 Error] The request was unacceptable, often due to missing a required parameter")
        elif(JsonImg.status_code == 401):
            exit("[401 Error] Invalid Access Token")
        elif(JsonImg.status_code == 403):
            exit("[403 Error] Missing permissions to perform request")
        elif(JsonImg.status_code == 404):
            exit("[404 Error] The requested resource doesn't exist")
        elif(JsonImg.status_code == 500 or JsonImg.status_code == 503):
            exit(f"[{JsonImg.status_code} Error] Something went wrong on unsplash's end")
        else:
            exit(f"[{JsonImg.status_code} Error] Something went wrong")
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
    
    # ======== # Checking for errors # ======== #
    if(JsonImg.status_code != 200):
        if(JsonImg.status_code == 400):
            exit("[400 Error] The request was unacceptable, often due to missing a required parameter")
        elif(JsonImg.status_code == 401):
            exit("[401 Error] Invalid Access Token")
        elif(JsonImg.status_code == 403):
            exit("[403 Error] Missing permissions to perform request")
        elif(JsonImg.status_code == 404):
            exit("[404 Error] The requested resource doesn't exist")
        elif(JsonImg.status_code == 500 or JsonImg.status_code == 503):
            exit(f"[{JsonImg.status_code} Error] Something went wrong on unsplash's end")
        else:
            exit(f"[{JsonImg.status_code} Error] Something went wrong")
    else:
        JsonImg = JsonImg.json()
    
    id_list : list = list()
    for i in range(per_page):
        id_list.append(JsonData['results'][i]['id'])
    return(id_list)