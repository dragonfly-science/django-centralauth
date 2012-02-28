from distutils.core import setup
setup(name              = 'django-centralauth',
        version         = '0.1',
        description     = 'Django support for a seperate authentication database',
        url             = 'https://github.com/dragonfly-science/django-authrouter.git',
        packages        = ['centralauth', 'centralauth.centralauth', 'centralauth.authrouter']
)

