# Device Tracker Backend

## Overview

This Django app serves as the backend for the "Device Tracker" application. It provides various endpoints for managing devices, user accounts, and assignments.

## URLs and Endpoints

- **`DeviceTracker`**: Main project folder.
  - **`DeviceTracker/urls.py`**: Main URL configuration for the project.
  - **`accounts/urls.py`**: URL configuration for the accounts app.
  - **`assign/urls.py`**: URL configuration for the assign app.
  - **`device/urls.py`**: URL configuration for the device app.


In the main `urls.py` file (`DeviceTracker/urls.py`), the following endpoints are defined:

- `/health`: Endpoint for health checks.
                If server is up, the response will be {"status":"up"}

- `/admin/`: Django admin panel.
                This opens admin dashboard page if logged in.
                Keep in mind that,default User model is assigned as admin.
                A when deployment done for the first time, dont forget to give value for
                DEFAULT_SUPERUSER_USERNAME,
                DEFAULT_SUPERUSER_PASSWORD,
                DEFAULT_SUPERUSER_EMAIL inside .env file as it will be the default superuser.

- `/accounts/`: Endpoints related to user accounts.
                    This app implements slack authentication for users.
                    Remember, This users will be CustomUser model instances.


                In the `accounts` app (`accounts/urls.py`), the following endpoints are defined:
                    1. create a slack app.

                    2. Go through the docs thoroughly and note what info the app should collect.
                        By default it collects slack_id,email,name and picture_url.
                        If you want to change the info it collects - (add or remove)
                            change the code in create_user_info function in utils.accounts
                    
                    3. Add SLACK_CLIENT_ID, SLACK_CLIENT_SECRET,
                            SLACK_REDIRECT_URI_PROD, SLACK_REDIRECT_URI_DEV in .env file.
                        
                        Note: SLACK_REDIRECT_URI_PROD will be redirect_url in "production".
                                SLACK_REDIRECT_URI_DEV will be redirect_url in "development". 


        - `/user/oauth/start`: Initiates the OAuth process for Slack.
                                This provides a link as response and when link is click it redirects to
                                slack auth page.
                                When Allow button is clicked in the slack UI, gets redirected to the redirect_url.
        
        - `/user/oauth/redirect`: Handles the OAuth redirect from Slack.
                                    1. If the redirected url and the redirect_url given the slack app isnt
                                        identical an error will be thrown and auth fails.
                                    
                                    2. If auth from slack is success, profile information of requested fields
                                    is taken.
                                    
                                    3. Also a jwt is set and sent to store in the browsers cookie as auth_token.
                                    
                                    4. Set the required jwt secret key and algorthm as
                                        JWT_SECRET_KEY, JWT_ALGORITHM in .env file.

                                    The response will be a profile information.

        - `/user/profile`: Retrieves the user's profile information.
                            if the user have the jwt_ccokie verified - 
                            profile info is given as response.





- `/device/`: Endpoints related to devices.

        - `/device/`: If the request method is:
                GET - returns a list of all devices.
                POST - creates a device as per given in the body if it satisfies the requirements.


        - `/device/{id}` : id is the id of device.say for eg:5.
                    if request method is:
                    GET - returns specific device of that id.
                    PUT - this will update the device as in the body.
                    PATCH - partial update the particular field given in the body.
                    DELETE - delete the particular device.


        - `/device_status?status=value` : will expect a query param "status".
                            value of "status" will be: 
                                available - fetching available devices
                                in_use - fetching devices in user
                                under_maintainance - fetches devices under maintainance.


        - `/user_device/`: Endpoint for managing devices in user_perspective.
            If the request method is:
                GET - returns a list of all devices user is having.


        - `/user_device/history` : returns the history of 10 device actions by a user
                                        in descending order of returned date.
    
        
        
        - `/device_action/`: Endpoint for device actions.
                            no methods implemented.

        - `/device_action/take_device`:
              method : POST
              body : device_id 
                *user_id will be taken from request.user.slack_id.
                *Assignlog is created with these ids with  current date and timerecorded in took_at attribute.
                *The returned_at attribute of Assignlog will be null.
                *In Device object, the status attribute will be changed to in_use.
                *Also the user attribute will be changed to current user id.

        - `/device_action/return_device`:
              method : POST
              body : device_id 
                *user_id will be taken from request.user.slack_id.
                *Checked wheather the device is in use by the requested user.
                *If so,
                    Assignlog is queried with these ids where the returned_date is null.
                *If an object found,
                    returned_at attribute of Assignlog will be updated with current date and time.
                *In Device object,
                        the status attribute will be changed to available.
                *Also the user attribute will be changed to null.





- `/assign/`: Endpoints related to device assignments.
        -if method is:
            POST - and matches the model requirements in the body - log can be created.
            GET  - returns a list of all logs.

        - `/assign/{id}`: 
            -if method is:
                GET  - returns the particular log with that id.
                DELETE - deletes the particular log with that id
    
    Please note : These above routes are not implemented well.
        Even if it becomes,its not meant to custom users.

        - `/assign/user_device_log/`:
                gets the user from request.user and returns the logs of 
                    all devices taken by that user.



##Authentication
We have slack auth and jwt authentication implemented for this app.

By default, the expiry date is set as 1 day.
If you want to change, git to generate_jwt function in utils.jwt 
    and change the exp key in payload accordingly.

We have TokenAuthenticationMixin

##CustomMixins
    TokenAuthenticationMixin - in accounts.mixins
        It checks wheather the user is authenticated or not.


##CutomBackends
    TokenBackend - in accounts.auth_backends.CustomBackend
        It recieves token as a parameter.
        if token decoded successfully,
        searches for the particular user in db and 
        if found,
            sets user.is_authenticated = True  (TokenAuthenticationMixin checks this attribute of request.user whaether its True or False)
            returns user
        else 
            throws error if user not found or other exceptions
        
        If token is not present, returns None.

    Added this in AUTHENTICATION_BACKENDS in top before the default auth ModelBackend.

##CustomMiddlewares
    JWTAuthenticationMiddleware - in accounts.CustomMiddlewares
        placed after default Authentication middleware in settings.py


##How this CustomMiddleware,CustomBackend and CustomMixin?
    - CustomMiddleware runs and calls the authenticate method of the TokenBackend for every request.
    - If TokenBackend returns the user, this middleware sets to request.user 
        and pass the request object to next middleware.
    - If TokenBackend doesnt return the user,say its None, the request object is passed as it received.
        request.user will be Anonymous user as it came from Authentication middleware early.

    - So when url directs to a view, 
        before executing the code inside the view,
         if its a child of TokenAuthneticationMixin:
            It executes TokenAuthenticationMixin and checkes request.user.is_authenticated.
        If its true it directs it to code inside view function
        else:
            it redirects to the particular url we mentioned in the mixin.
            Here, its accounts/user/oauth/start.

Keep in mind, this mixin is excecuted after every middleware is run.


##Admin
- We use django unfold to customise styling in admin page.
- So django-unfold is installed and also added in INSTALLED_APPS.
- Make sure it comes before before django.admin in the order.
- If you want the default admin page, remove the unfold from INSTALLED_APPS.

##WhiteNoise to serve static fields
- we've installed whitenoise and added it as a middleware to serve static contents.


##production
- We use render for deployment. So production environment is adjusted to suit that.
- Ensure ENV=prod in .env file.
- Make sure DEBUG=False in .env file.
- As render doesnt provide a shell access for free tier - we use a web instance as well as a postgres instance seperately.
- So ,dj_database_url is installed and
            DATABASES['default'] = dj_database_url.config(
                default=os.environ.get("DB_URL"),
                conn_max_age=600
            )
    the above code is ensured in settings.py. Make sure its the default DB.
- Add the DB_URL in the .env file. Its the internal connection url in renders postgres instance.
- Also ensure build.sh is present.
- Make sure a requirements.txt is present.

    -build.sh:-
        This file is read for build in render.
        - Ensure installation of all dependencies remains in the top of this file.
        - As we use WhiteNoise as webserver to serve static files, we dont need a collectstatic for this
            project right now.
        - Ensure makemigrations and migration commands are present.
        -  We have python manage.py run_startup_functions in the last.
            Its because we havent access to the server shell so we cant ran createsuperuser command manually.
        - So we use this alternative, as superuser is created initially during the app spins up for te 1st time.
        - Make sure you give DEFAULT_SUPERUSER_USERNAME, DEFAULT_SUPERUSER_PASSWORD, DEFAULT_SUPERUSER_EMAIL in the .env file.
        - By using this default username and password you can log in to admin dashboard for the 1st time.
        - Then as that superuser, from admin dashboard you can create your needed superusers.

        Note:- This is for only this specific case. When using an amazon EC2 instance you wont need this case as it provides shell access. 


##development
    - Set DEBUG in .env into True.
    - Set ENV in .env into dev
    - Make sure you have postgres installed and provide necessary values for 
        DB_NAME,DB_USER,DB_PASSWORD,DB_PORT.
    - You can also change your DB conf as per your wish but make sure 
        you make necessary changes in settings.py as well to avoid errors.
    - In development stage - during slack authentication :-
         redirect url will fail as the slack auth server wont point to your localhost.
        So use tunnelling services like ngrok and use it. Take that link instead of localhost.
        eg:"https://3487-103-141-56-118.ngrok-free.app/accounts/user/oauth/redirect"

##Custom Commands
- in accounts.management.commands we have run_startup_functions module
- Contains the logic of creating initial superuser and also changing admin header,index_title and site title is changed.


Note:-
    - Make sure you have sample .env file to obtain the necessary keys needed for your .env file.
    - Also ensure you have your values for them.

Happy Coding!!