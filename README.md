# Unsplash Downloader

This Python script allows you to download images from Unsplash. It can be used to download a single image, a collection of images, or all images that match a specific search query.

🔴 **Note: This script is still under development and not completed yet**
## Installation

To install the script, run the following command:

```
pip install .
```
**Make sure you are in the unsplash_downloader directory when your executing code**
## Usage
first import the library by

```python
from unsplash_downloader import unsplash
```

To download all images that match a specific search query, use the following command:

```python
search_photo(client_id = "YOUR_ACCESS_KEY", query="YOUR_SEARCH_QUERY")
```

To download a collection of images, use the following command:

```python
download_collection(client_id = "YOUR_ACCESS_KEY", id="YOUR_COLLATION_ID")

```

it gets collection id that can use on download collection

```python
get_collections_id(client_id = "YOUR_ACCESS_KEY", query="YOUR_SEARCH_QUERY")
```

## Code Explanation

The script is written in Python and uses the Unsplash API to download images. The code is well-commented and easy to understand.

The `search_photo()` function downloads most relevant images from Unsplash by. The function takes the following arguments:

* `client_id`: Your Unsplash client ID.
* `query`: The search query to use.
* `page`: The page number of the results to download.
* `per_page`: The number of images to download per page.
* `order_by`: The order in which to sort the results.
* `collections`: The collections to search.
* `content_filter`: The content filter to use.
* `color`: The color of the images to download.
* `orientation`: The orientation of the images to download.
* `_DownloadImg`: A boolean value indicating whether to download the images.
* `_FileName`: The name of the file to save the images to.
* `_Path`: The path to the directory to save the images to.

The `download_collection()` function downloads a collection of images from Unsplash. The function takes the following arguments:

* `client_id`: Your Unsplash client ID.
* `id`: The ID of the collection to download.
* `page`: The page number of the results to download.
* `per
