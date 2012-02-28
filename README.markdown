# Django Authrouter

An authentication router that lets
you use a central authentication database
across multiple web applications.

## Usage

Install ths in ypour python path, and
then in your django settings file you
will need something like the following

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'foo',
            'USER': 'foo',
        },  
        'auth': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'credentials',
            'USER': 'credentials',
            'HOST': 'authserver',
        },
    }   
    DATABASE_ROUTERS = ['authrouter.authrouter.AuthRouter']
    AUTHENTICATION_DATABASE = 'auth'

With this setup, authentication calls will get routed to the
`auth' database.

## Attribution

The code was plucked out of a forum
somewhere on the internet. 
[Bradon Belew](http://groups.google.com/group/django-users/browse_thread/thread/462c7b523856e10b/f7deeef5e055693f#f7deeef5e055693f)
discussed it on google groups, and it may
originally have been his. We can't remember. If this
is your code, let us know and we will attribute it correctly!



