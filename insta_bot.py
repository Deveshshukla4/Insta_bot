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

def get_user_by_username():
    user_name = raw_input("Enter Username  you wants to Search  OR S to Check your profile  OR Q to quit : ")
    requests_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (user_name , APP_ACCESS_TOKEN)
    search_results = requests.get(requests_url).json()


    if len(search_results['data']) :
        print "User id : " + str(search_results['data'][0]['id'])
        print "Full name : " + str(search_results['data'][0]['full_name'])
        print "Bio : " + str(search_results['data'][0]['bio'])
        response = raw_input("Enter Y to perform operations or N to continue search : ").upper()
        if response == "Y":
            operations(search_results['data'][0]['id'])
        else:
            get_user_by_username()
    elif user_name == "s" or user_name == "S":
        self_info()

    elif user_name == "q" or user_name == "Q":
        exit()
    else:
        print "User doesn't exists !"
        get_user_by_username()

