# Django centralauth

An authentication router that lets
you use a central authentication database
across multiple web applications.

This is code that we have used in
some of our projects, and
is here for our own purposes. 
Standard health warnings
apply.

## Usage

Install this in ypour python path, and
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
    DATABASE_ROUTERS = ['centralauth.authrouter.AuthRouter']
    AUTHENTICATION_BACKENDS = ['centralauth.centralauth.ModelBackend']
    AUTHENTICATION_DATABASE = 'auth'

With this setup, authentication calls will get routed to the
`auth' database.

## Issues

Usage may vary. Under some circumstances, the use of this authentication model breaks the use of tools
that expect a standard setup. In particular you may have trouble using `South`,
or running `python manage.py syncdb`. This is due to problems with foreign keys
spanning multiple databases.


## Attribution

The authrouter code was plucked out of a forum
somewhere on the internet. 
[Bradon Belew](http://groups.google.com/group/django-users/browse_thread/thread/462c7b523856e10b/f7deeef5e055693f#f7deeef5e055693f)
discussed it on google groups, and it may
originally have been his. We can't remember. If this
is your code, let us know and we will attribute it correctly!



