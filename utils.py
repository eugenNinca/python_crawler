import os
from urllib.parse import urlparse

# For each website make a folder
def create_website_dir(directory):
    if not os.path.exists(directory):
        print('Creating project ' + directory)
        os.makedirs(directory)


# write file to path
def write_file(path, data):
    print('Write a file ' + path)
    with open(path, 'w') as file:
        file.write(data)

# get subdomain
def get_subdomain(url):
    try:
        return urlparse(url).netloc
    except:
        return ''

# get domain
def get_domain(url):
    try:
        result = get_subdomain(url).split('.')
        return result[-2] + '.' + result[-1]
    except:
        return ''

# url to file path in project
def url_to_file_path(page_url, project_name, base_url):
    if page_url == base_url:
        file_path = os.path.join(os.getcwd(), project_name, 'index.html')
    else:
        url = urlparse(page_url)
        file = url.path.replace('/', '')
        file_path = os.path.join(os.getcwd(), project_name, ''.join(file.split('.')[0]) + '.html')
    return file_path

# check if url
def valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False
