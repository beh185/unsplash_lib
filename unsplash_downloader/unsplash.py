# Github: https://github.com/beh185
# Telegram: https://T.me/dr_xz
# e-mail: BehnamH.dev@gmail.com
# ____________________________________________

# ======== # Import Modules # ======== #
try:
    from os import system, path, name
    from requests import get, post, put ,ConnectionError, ReadTimeout, Response
    from urllib.request import urlretrieve
    from urllib.error import URLError
except ImportError:
    exit("[+] Please Install the required modules by running setup.py file!")

# =========== # Functions # =========== #

# ======== # Checking for http errors # ======== #
def __check_http_error__(respond) -> None:
    if(respond.status_code == 400):
        print("[400 Error] The request was unacceptable, often due to missing a required parameter")
    elif(respond.status_code == 401):
        print("[401 Error] Invalid Access Token")
    elif(respond.status_code == 403):
        print("[403 Error] Missing permissions to perform request")
    elif(respond.status_code == 404):
        print("[404 Error] The requested resource doesn't exist")
    elif(respond.status_code == 500 or respond.status_code == 503):
        print(f"[{respond.status_code} Error] Something went wrong on unsplash's end")
    else:
        print(f"[{respond.status_code} Error] Something went wrong")

# ======== # Downloading Images results for a query. # ======== #
def search_photo(client_id:str = str(), query:str = str(), page:int = int(), per_page:int = int(), order_by:str = str(), collections = str(), content_filter = str(), color = str(), orientation = str(), _DownloadImg=True, _FileName: str = 'S-image', _Path: str = str(), pass_errors: bool = False) -> dict | None: # type: ignore
    '''Download photos by search results.
|param     | Description   |    
---|---|   
|`client_id`: |  Your Unsplash Access Key. |
| `query`: |  Search terms. |
| `page`: |  The page number of the results to download. (Optional; default: 1) |
| `per_page`: |  The number of images to download per page. (Optional; default: 10)
| `order_by`: |  The order in which to sort the results. (Optional; default: relevant). Valid values are latest and relevant. |
| `collections`: |  Collection ID('s) to narrow search. Optional. If multiple, comma-separated. |
| `content_filter`: |  Limit results by [content safety](https://unsplash.com/documentation#content-safety). (Optional; default: low). Valid values are low and high. |
| `color`: |  Filter results by color. Optional. Valid values are: black_and_white, black, white, yellow, orange, red, purple, magenta, green, teal, and blue. |
| `orientation`: |  The orientation of the images to download. |
| `_DownloadImg`: |  A boolean value indicating whether to download the images. |
| `_FileName`: |  The name of the file to save the images to. |
| `_Path`: |  The path to the directory to save the images to. |
| `_pass_errors` : | If there an error during the process. It won't break the program. It will just skip the process|
    '''
    payload: dict = {
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
    PayLoad: dict = payload.copy()

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
        ResponseData: Response = get(unsplash_api, allow_redirects=True, timeout=25, params=PayLoad)
    except ConnectionError:
        exit("Connection Failed. It's might because of your network connection")
    except KeyboardInterrupt:
        exit('\nOperation canceled by user')
    except ReadTimeout:
        exit('Time out reached')
        
    # ======== # Checking for http errors # ======== #
    if(ResponseData.ok == False):
        if pass_errors == False:
            exit(__check_http_error__(ResponseData))
        else:
            pass
            return(__check_http_error__(ResponseData))
    else:        
        JsonImg: dict = ResponseData.json()
        
    # ======= # Download images# ======= #
    if(_DownloadImg):
        print('Downloading images ...')
        if(_Path != str()):
            if(path.exists(_Path) == False):
                exit(f'"{_Path}" is not exist')

            if(name == 'nt' and _Path.endswith('\\') == False):
                _Path: str = _Path + '\\'
            elif(name == 'posix' and _Path.endswith('/') == False):
                _Path: str = _Path + '/'

        for i in range(per_page):
            ImgLink: str = JsonImg['results'][i]['urls']['full'] #type: ignore
            try:
                urlretrieve(ImgLink, f"{_Path}{_FileName}-{i}.jpg")
            except URLError:
                exit('Error! It might be because of the network problem or your setting issues, such as proxy setting')
    else:
        return JsonImg
    
# ========== # Retrieve a collection’s photos. # ========== #
def download_collection(client_id: str = str(), id = None, page: int = int(), per_page: int = int(), orientation: str = str(), _DownloadImg: bool = True, _FileName: str = 'C-image', _Path: str = str(), pass_errors: bool = False) -> dict | None:# type: ignore
    '''Download a collection's photos.
| param | Description |
---|---|
|`client_id`: |  Your Unsplash Access Key. |
| `id` : | 	The collection's ID. Required. |
| `page` : | 	Page number to retrieve. (Optional; default: 1) |
| `per_page` : | 	Number of items per page. (Optional; default: 10) | 
| `orientation` : | 	Filter by photo orientation. Optional. (Valid values: landscape, portrait, squarish) |
| `_DownloadImg`: |  A boolean value indicating whether to download the images. |
| `_FileName`: |  The name of the file to save the images to. |
| `_Path`: |  The path to the directory to save the images to. |
| `_pass_errors` : | If there an error during the process. It won't break the program. It will just skip the process|'''
    payload: dict = {
        'client_id': client_id,
        'page': page,
        'per_page': per_page,
        'orientation':orientation}
    # ======== # Making copy to prevent RuntimeError: dictionary changed size during iteration # ======== #
    PayLoad: dict = payload.copy()

    # ====== # Removing values that user didn't specified # ====== #
    for key, value in payload.items():
        if (value == '' or value == 0):
            PayLoad.pop(key)

    # ======== # Checking requirement var # ======== #
    if ('client_id' not in PayLoad.keys()):
        exit('download_collection() missing 1 required positional argument. Please specify client_id')
    if(id == None):
        exit('download_collection() missing 1 required positional argument. Please specify id')

    unsplash_api: str = f'https://api.unsplash.com/collections/{str(id)}/photos'
    try:
        ResponseData: Response = get(unsplash_api, allow_redirects=True, timeout=25, params=PayLoad)
    except ConnectionError:
        exit("Connection Failed. It's might because of your network connection")
    except KeyboardInterrupt:
        exit('\nOperation canceled by user')
    except ReadTimeout:
        exit('Time out reached')
    
    # ======== # Checking for http errors # ======== #
    if(ResponseData.ok == False):
        if pass_errors == False:
            exit(__check_http_error__(ResponseData))
        else:
            pass
            return(__check_http_error__(ResponseData))
    else:
        JsonImg: dict = ResponseData.json()
        
    # ======= # Download images# ======= #
    if(_DownloadImg):
        print('Downloading images ...')
        if(_Path != str()):
            if(path.exists(_Path) == False):
                exit(f'"{_Path}" is not exist')

            if(name == 'nt' and _Path.endswith('\\') == False):
                _Path: str = _Path + '\\'
            elif(name == 'posix' and _Path.endswith('/') == False):
                _Path: str = _Path + '/'
        for i in range(per_page):  # type: ignore
            ImgLink: str = JsonImg[i]['urls']['full']
            try:
                urlretrieve(ImgLink, f"{_Path}{_FileName}-{i}.jpg")
            except URLError:
                exit('Error! It might be because of the network problem or your setting issues, such as proxy setting')
            except KeyboardInterrupt:
                exit('\nOperation canceled by user')
    else:
        return JsonImg


def get_collections_id(client_id: str = str(), query: str = str(), page: int = int(), per_page: int = int(), pass_errors: bool = False) -> list:
    '''You can search for collection and get the collection's id, Then you can use it in download_collection() func to download images
| param | Description |
---|---|
|`client_id`: |  Your Unsplash Access Key. |
|`query` : | Search terms. |
| `page`: |  The page number of the results to download. (Optional; default: 1) |
| `per_page`:  |  The number of images to download per page. (Optional; default: 10) |
| `_pass_errors` : | If there an error during the process. It won't break the program. It will just skip the process|'''
    
    payload: dict = {
        'client_id': client_id,
        'query':query,
        'page': page,
        'per_page':per_page}
    # ======== # Making copy to prevent RuntimeError: dictionary changed size during iteration # ======== #
    PayLoad: dict = payload.copy()

    # ====== # Removing values that user didn't specified # ====== #
    for key, value in payload.items():
        if (value == '' or value == 0):
            PayLoad.pop(key)
    
    # ======== # Checking requirement var # ======== #
    if ('client_id' not in PayLoad.keys()):
        exit('download_collection() missing 1 required positional argument. Please specify client_id')
    if ('query' not in PayLoad.keys()):
        exit('download_collection() missing 1 required positional argument. Please specify query')

    unsplash_api: str = 'https://api.unsplash.com/search/collections'
    try:
        ResponseData: Response = get(unsplash_api, allow_redirects=True, timeout=25, params=PayLoad)
    except ConnectionError:
        exit("Connection Failed. It's might because of your network connection")
    except KeyboardInterrupt:
        exit('\nOperation canceled by user')
    except ReadTimeout:
        exit('Time out reached')
    
    # ======== # Checking for http errors # ======== #
    if(ResponseData.ok == False):
        if pass_errors == False:
            exit(__check_http_error__(ResponseData))
        else:
            pass
            return __check_http_error__(ResponseData) # type: ignore
    else:
        JsonData: dict = ResponseData.json()
    
    # ======= # Returning collection id # ======= #
    id_list : list = list()
    for i in range(per_page):
        id_list.append(JsonData['results'][i]['id'])
    return(id_list)

# ======== # Get a single page of user results for a query # ======== #
def search_users(client_id: str = str(), query: str = str(), page: int = int(), per_page: int = int(), pass_errors: bool = False) -> list[dict]:
    '''Search for a user and getting back the results as list that contain a dictionary.
| param | Description|
---|---|
|`client_id`: |  Your Unsplash Access Key. |
| `query` : |	Search terms.|
| `page` : | The page number of the results to download. (Optional; default: 1)
| `per_page` : | The number of images to download per page.  (Optional; default: 10)
| `_pass_errors` : | If there an error during the process. It won't break the program. It will just skip the process|'''

    payload: dict = {
        'client_id': client_id,
        'query':query,
        'page': page,
        'per_page':per_page}
    # ======== # Making copy to prevent RuntimeError: dictionary changed size during iteration # ======== #
    PayLoad: dict = payload.copy()

    # ====== # Removing values that user didn't specified # ====== #
    for key, value in payload.items():
        if (value == '' or value == 0):
            PayLoad.pop(key)
    
    # ======== # Checking requirement var # ======== #
    if ('client_id' not in PayLoad.keys()):
        exit('download_collection() missing 1 required positional argument. Please specify client_id')
    if ('query' not in PayLoad.keys()):
        exit('download_collection() missing 1 required positional argument. Please specify query')
    
    unsplash_api: str = 'https://api.unsplash.com/search/users'
    
    try:
        ResponseData: Response = get(unsplash_api, allow_redirects=True, timeout=25, params=PayLoad)
    except ConnectionError:
        exit("Connection Failed. It's might because of your network connection")
    except KeyboardInterrupt:
        exit('\nOperation canceled by user')
    except ReadTimeout:
        exit('Time out reached')
    
    # ======== # Checking for http errors # ======== #
    if(ResponseData.ok == False):
        if pass_errors == False:
            exit(__check_http_error__(ResponseData))
        else:
            pass
            return __check_http_error__(ResponseData) # type: ignore
    else:
        JsonData: dict = ResponseData.json()
    
    return JsonData['results']

# ======= # Create a new collection. This requires the write_collections scope that can be activated on your api.unsplash.com account # ======= #
def create_collection(client_id: str = str(), title: str = str(), description: str = str(), private: bool = False, pass_errors: bool = False) -> str:
    '''Create a new collection. This requires the `write_collections` permission. Enable it on  Redirect URI & Permissions on your profile.
| param |	Description |
---|---|
|`client_id`: |  Your Unsplash Access Key. |
| title: |	The title of the collection. (Required.) |
| description: | 	The collection's description. (Optional.) |
| private: |	Whether to make this collection private. (Optional; default false). |
| `_pass_errors`: | If there an error during the process. It won't break the program. It will just skip the process|
'''
    payload: dict = {
        'client_id': client_id,
        'title': title,
        'description':description,
        'private': private}
    # ======== # Making copy to prevent RuntimeError: dictionary changed size during iteration # ======== #
    PayLoad: dict = payload.copy()

    # ====== # Removing values that user didn't specified # ====== #
    for key, value in payload.items():
        if (value == '' or value == 0):
            PayLoad.pop(key)
    
    # ======== # Checking requirement var # ======== #
    if ('client_id' not in PayLoad.keys()):
        exit('download_collection() missing 1 required positional argument. Please specify client_id')
    if ('title' not in PayLoad.keys()):
        exit('download_collection() missing 1 required positional argument. Please specify title')
        
    unsplash_api: str = 'https://api.unsplash.com/collections'
    
    try:
        ResponseData: Response = post(unsplash_api, allow_redirects=True, timeout=25, params=PayLoad)
    except ConnectionError:
        exit("Connection Failed. It's might because of your network connection")
    except KeyboardInterrupt:
        exit('\nOperation canceled by user')
    except ReadTimeout:
        exit('Time out reached')
    
    # ======== # Checking for http errors # ======== #
    if(ResponseData.ok == False):
        if pass_errors == False:
            exit(__check_http_error__(ResponseData))
        else:
            pass
            return(__check_http_error__(ResponseData)) # type: ignore

    return f'{title} created successfully'

# ======== # Update an existing collection belonging to the logged-in user. This requires the write_collections scope. # ======== #
def update_collection(client_id: str = str(), id: str = str(), title: str = str(), description: str = str(), private: bool = False, pass_errors: bool = False) -> str:
    '''Update an existing collection belonging to the logged-in user. This requires the write_collections permission. Enable it on  Redirect URI & Permissions on your profile.
| param |	Description |
---|---|
|`client_id`: |  Your Unsplash Access Key. |
| title:  |	The title of the collection. (Required.) |
| description: | 	The collection's description. (Optional.) |
| private: |	Whether to make this collection private. (Optional; default false). |
| `_pass_errors`:  |  If there an error during the process. It won't break the program. It will just skip the process|
    '''
    payload: dict = {
        'client_id': client_id,
        'title': title,
        'description':description,
        'private': private}
    # ======== # Making copy to prevent RuntimeError: dictionary changed size during iteration # ======== #
    PayLoad: dict = payload.copy()

    # ====== # Removing values that user didn't specified # ====== #
    for key, value in payload.items():
        if (value == '' or value == 0):
            PayLoad.pop(key)
    
    # ======== # Checking requirement var # ======== #
    if ('client_id' not in PayLoad.keys()):
        exit('download_collection() missing 1 required positional argument. Please specify client_id')
    if (id == str()):
        exit('download_collection() missing 1 required positional argument. Please specify id')
    
    unsplash_api: str = f'https://api.unsplash.com/collections/{id}'
    
    try:
        ResponseData: Response = put(unsplash_api, allow_redirects=True, timeout=25, params=PayLoad)
    except ConnectionError:
        exit("Connection Failed. It's might because of your network connection")
    except KeyboardInterrupt:
        exit('\nOperation canceled by user')
    except ReadTimeout:
        exit('Time out reached')
    
    # ======== # Checking for http errors # ======== #
    if(ResponseData.ok == False):
        if pass_errors == False:
            exit(__check_http_error__(ResponseData))
        else:
            pass
            return (__check_http_error__(ResponseData)) # type: ignore
        
    return 'The collection updated successfully'