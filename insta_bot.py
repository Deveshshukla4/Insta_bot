import requests # Requests library imported to perform different queries such as get , post , delete ,put


APP_ACCESS_TOKEN = "3068983250.94b2134.006490b178c24fefa74dba819dddaa1c" # access token

BASE_URL = "https://api.instagram.com/v1/"

#Function to prints the user info

def self_info():
    requests_url = (BASE_URL + 'users/self/?access_token=%s') % (APP_ACCESS_TOKEN) #req to fetech the user info
    my_info = requests.get(requests_url).json() #response from api


    print "Name :" + str(my_info['data']['full_name'])
    print "Bio :" + str(my_info['data']['bio'])
    print "Followers :" + str(my_info['data']['counts']['followed_by'])

    get_user_by_username()#calling function

#function to search the username and perform operations

