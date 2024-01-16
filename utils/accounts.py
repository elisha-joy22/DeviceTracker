from accounts.models import CustomUser


def update_or_create_user(user):
    try:
        print('inside update_or_create user')
        returned_user,is_created_now = CustomUser.objects.update_or_create(          #returns boolean true if new obj created
                                        slack_id=user.get('slack_id'),
                                        defaults=user
                                    )
    except CustomUser.DoesNotExist:
        return {'error':'User creation falied!!'}
    
    return returned_user



def create_user_info(user_info_response):
    slack_id = user_info_response.get("https://slack.com/user_id")
    email = user_info_response.get("email")
    picture_url = user_info_response.get("https://slack.com/user_image_48")
    
    user_info = {
                "slack_id" : user_info_response.get("https://slack.com/user_id"),
                "email" : user_info_response.get("email"),
                "name" : user_info_response.get("name"),
                "picture_url":picture_url
                }        

    return user_info



