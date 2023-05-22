from xnat_api import api_images_from_xnat, unzip

xnat_url = input("Please enter your localhost: ")
user = input("Please enter your username: ")
password = input("Please enter your password: ")
project_id = input("Please enter your project ID: ")

output = api_images_from_xnat(xnat_url, user, password, project_id)
unzip(output)