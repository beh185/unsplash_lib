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
def search_photo(client_id = str(), query = str(), page = int(), per_page = int(), order_by = str(), collections = str(), content_filter = str(), color = str(), orientation = str(), _DownloadImg=True, _FileName: str = 'image', _Path = str()):
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

    unsplash_api = 'https://api.unsplash.com/search/photos'
    try:
        JsonImg = get(unsplash_api, allow_redirects=True, timeout=25, params=PayLoad)
        if JsonImg.ok == False:
            exit(f"[{JsonImg.status_code} Error] occurred while downloading images")
        JsonImg = JsonImg.json()
    except ConnectionError:
        exit("Connection Failed. It's might because of your network connection")
    except KeyboardInterrupt:
        exit('\nOperation canceled by user')
    except ReadTimeout:
        exit('Time out reached')

    if(_DownloadImg):
        # ======= # Download images# ======= #
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
# ======== # Get a single page of collection results for a query. # ======== #
def search_collections(client_id = str ,query = str, page = int, per_page = int, _DownloadImg = True, _FileName=str(), _Path = str()):
    payload = {
        'client_id': client_id,
        'query': query,
        'page': page,
        'per_page': per_page }
    # ======== # Making copy to prevent RuntimeError: dictionary changed size during iteration # ======== #
    PayLoad = payload.copy()

    # ====== # Removing values that user didn't specified # ====== #
    for key, value in payload.items():
        if (value == '' or value == 0):
            PayLoad.pop(key)

    unsplash_api = 'https://api.unsplash.com/search/collections'
    try:
        JsonImg = get(unsplash_api, allow_redirects=True, timeout=25, params=PayLoad)
        if JsonImg.ok == False:
            exit(f"[{JsonImg.status_code} Error] occurred while downloading images")
        JsonImg.json()
    except ConnectionError:
        exit("Connection Failed. It's might because of your network connection")
    except KeyboardInterrupt:
        exit('\nOperation canceled by user')
    except ReadTimeout:
        exit('Time out reached')
    if(_DownloadImg):
        # ======= # Download images# ======= #
        if(_Path != str()):
            if(path.exists(_Path) == False):
                exit(f'"{_Path}" is not exist')

            if(name == 'nt' and _Path.endswith('\\') == False):
                _Path = _Path + '\\'
            elif(name == 'posix' and _Path.endswith('/') == False):
                _Path = _Path + '/'

        for i in range(per_page):
            ImgLink = JsonImg['results'][i]['tags']['urls']['full']
            try:
                urlretrieve(ImgLink, f"{_Path}{_FileName}-{i}.jpg")
            except URLError:
                exit('Error! It might be because of the network problem or your setting issues, such as proxy setting')
    else:
        return JsonImg