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


#Performing operations on selected user

def operations(user_id):
    requests_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    recent_posts =requests.get(requests_url).json()

    post_list = ["x"]
    for likes in recent_posts['data']:
            post_list.append(likes['id'])
            print "User_id : " + str(user_id) + " Post id: " + str(post_list.index(likes['id'])) + " likes :" + str(likes['likes']['count']) + " Comments : " +  str(likes['comments']['count'])

    post_id = raw_input("Enter Post Id you wan't to access OR B to go back: ")
    if post_id == "b" or post_id == "B":
        get_user_by_username()
    else:
        x = int(post_id) #converting post_id into integer

    if post_list[x] not in post_list:
        print "Invalid Post id !"
        operations(user_id)
    else:
        post_id = post_list[x]
        select_operation(user_id, post_id)

        

#Function to perform various operations

def select_operation(user_id , post_id):
    opr = raw_input("Enter L to like a Post \n  OR C to comment on a Post \n  OR D to Delete comment \n  "
                    "OR A to find average number of words per comment \n  OR B to go back : ").upper()
    if opr == "L" or opr == "l":
        like_post(user_id , post_id)
    elif opr == "C" or opr == "c":
        comment_post(user_id , post_id)
    elif opr == "B" or opr == "b":
        operations(user_id)
    elif opr == "D" or opr == "d":
        select_the_way_to_delete_comment(user_id,post_id)
    elif opr == "A" or opr == "a":
        Average_number_of_words(user_id,post_id)

#function to like the post


def like_post(uid, post_id):
    payload = {'access_token':APP_ACCESS_TOKEN}
    requests_url = (BASE_URL + 'media/%s/likes' % (post_id))
    response_to_like = requests.post(requests_url, payload).json() # post request to send data

    if len(response_to_like):
        print "Post liked successfully!"
        operations(uid)

    else:
        print "Something went wrong! Can't like the post"
        operations(uid)


# function to delete the comment using two word method and manual method

def select_the_way_to_delete_comment(user_id,post_id):
    response = raw_input("Enter D to delete comment by word OR M to delete comments manually OR B to go back :").upper()
    if response == "D" or response == "d":
        delete_comment_by_word(user_id,post_id)
    elif response == "M" or response == "m":
        delete_comment_manually(user_id,post_id)
    elif response == "B" or response == "b":
        operations(user_id)
    else:
        print "Please Select the correct Method."
        select_the_way_to_delete_comment(user_id,post_id)


#This Function is to comment on post

def comment_post(uid , post_id):
    comment = raw_input("Your Comment here : ")
    payload = {'access_token': APP_ACCESS_TOKEN , 'text':comment}
    requests_url = (BASE_URL + 'media/%s/comments' % (post_id))
    response_to_comments = requests.post(requests_url, payload).json()

    if len(response_to_comments):
        print "Comment posted successfully."
        operations(uid)

    else:
        print "Something went wrong! Cant post comment."
        operations(uid)



#function to delete multiple comments containing a single word

def delete_comment_by_word(user_id , post_id):
    word = raw_input("Enter the word you want to search in comments :")
    requests_url = (BASE_URL + 'media/%s/comments?access_token=%s' % (post_id, APP_ACCESS_TOKEN))
    result = requests.get(requests_url).json()
    result2 = result['data']
    comment_list = []

    #loop for storing comment id
    for i in range(len(result2)):

        split = result2[i]['text'].split()

        if word in split:
            comment_list.append(result2[i]['id'])


    if len(comment_list):
        for i in comment_list:
            requests_url2 = (BASE_URL + 'media/%s/comments/%s?access_token=%s' % (post_id, i, APP_ACCESS_TOKEN))
            response = requests.delete(requests_url2).json()
        print str(len(comment_list)) + " Hurray! Comment deleted successfully."
        operations(user_id)
    else:
        print "No comments found for " + str(word)
        operations(user_id)


# function to delete comments manually

def delete_comment_manually(user_id,post_id):
    requests_url = (BASE_URL + 'media/%s/comments?access_token=%s' % (post_id,APP_ACCESS_TOKEN))
    fetch = requests.get(requests_url).json()
    c = 1
    for comments in fetch['data']:
        if len(comments['text']):
            print "comment id : " + str(c) + " " + "text : " + str(comments['text'])
        else:
            print "No comments to delete !"
            operations(user_id)
        c = c + 1
    comment_y = raw_input("Enter the comment id you want to delete OR B to go Back  :")
    if comment_y == "b" or comment_y == "B":
        operations(user_id)
    else:

        comment_y = int(comment_y)

    comment_id =["x"]
    for x in fetch['data']:
        comment_id.append(x['id'])
    x = comment_id[comment_y]

    requests_url2 = (BASE_URL + 'media/%s/comments/%s?access_token=%s' % (post_id, x , APP_ACCESS_TOKEN))
    response = requests.delete(requests_url2).json()

    if response['data'] == None:
        print "comment deleted successfully."
        delete_comment_manually(user_id, post_id)

    else:
        print "Something Went wrong! Can't Delete the comment."
        delete_comment_manually(user_id,post_id)


# function to find the average number of words per comment on a post

def Average_number_of_words(user_id , post_id):
    requests_url = (BASE_URL + 'media/%s/comments?access_token=%s' % (post_id, APP_ACCESS_TOKEN))
    fetch = requests.get(requests_url).json()
    c = 1
    av = 0
    if len(fetch['data']) > 0:

        for comments in fetch['data']:
            if len(comments['text']):
                print "comment id : " + str(c) + " " + "text : " + str(comments['text'])
                x1 = comments['text'].split()
                k = 0
                for i in x1:
                    k = k +1
                av = av + k

            c = c + 1
        total_words = av
        total_comments = c - 1
        Average = total_words / total_comments
        print "Average number of words per comment is : " + str( Average)
        operations(user_id)
    else:
        print "No comments found !"
        operations(user_id)


