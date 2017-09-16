dhayes.me Source
================

Source code for dhayes.me, my personal website. This is a pretty basic Django powered website featuring a home page app, and a blog app.

Installation
-------
This assumes python3, pip, virtualenv, postgreSQL and git are already installed on your machine. 

    git clone https://github.com/imasnyper/danielhayes.git 
    createvirtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt
    
Follow PostgreSQL documentation for creating a user and database.  Then in `settings.py`, fill in the NAME and USER fields under the DATABASES variable:

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': '[name_of_database_created]',
            'USER': '[database username]',
            'PASSWORD': DB_PASS,
            'HOST': 'localhost',
            'PORT': '',
        }
    }

Create a text file named `db_pass.txt`, and place it in the same folder as `settings.py`. Add the password for the database user to the first line in the file and save it. Follow the same steps and create a file called `secret_key.txt`. Add a secret and arbitrary string of letters, numbers, and symbols, 20-30 characters should be fine.

Setup should now be complete. Do initial database setup, run `collectstatic` to collect all static files to the folder specified in `STATIC_ROOT` , and run the server!

    $ python manage.py makemigrations
    $ python manage.py migrate
    $ python manage.py collectstatic
    $ python manage.py runserver

Home App
-------

The home app has just one model with customizable snippets I call "Blurbs". Each Blurb has the following attributes:

 1. Title - the heading for the Blurb
 2. Text - the meat of the blurb which has all your desired information
 3. Order - pretty basic, lower values are placed on the page first, and continue left to right in rows of 3.
 
This is very minimal, but gets the job done. I wanted to have the ability to edit the content of the home page from the admin. I don't expect to want to update it that often, but it provides a very simple way to do so when I chose. 

## Blog App ##

Includes 3 models, a Post model, a PostImage model and a Tag model. Post model:

 1. author - a django.contrib.auth.models.User field
 2. title - title of the blog post
 3. slug - slug for the blog post. defaults to the title of the post, but can be modified. Must be unique.
 4. post - the actual blog post text
 5. pub_date - used to determine if a post is published on the site or not. Defaults to the current date and time in the admin, but can be adjusted to any date/time past or future. Dates in the future will cause the post to remain hidden from the website until that date.
 6. tags - a many-to-many field relating to Tag models for storing categorizing tags for the post. Can select previously created tags, or create new ones from the admin.

The PostImage model is used for storing images related to a specific post. Users can upload images to the admin site while creating a post and the images will appear at the bottom of the post. PostImage has the following fields:

 1. post - foreign key to the post the image is related to
 2. title - title for the image
 3. width - width of the image
 4. height - height of the image
 5. image - `models.ImageField`

The Tag model is used to apply zero or more categorization tags to the blog post. These tags let users easily access posts related to exactly the categories they're looking for. Contains just one model field, which is the tag itself. But it also contains methods for determining the ratio of any particular tag to the rest, which allows for making a rudimentary tag cloud in views.
