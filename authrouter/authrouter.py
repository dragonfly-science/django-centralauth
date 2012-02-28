from django.conf import settings


class AuthRouter(object):
    """A router to control all database operations on models in
    the contrib.auth application"""

    def db_for_read(self, model, **hints):
        "Point all operations on auth models to 'AUTHENTICATION_DATABASE'"
        if model._meta.app_label == 'auth' and settings.AUTHENTICATION_DATABASE:
            return settings.AUTHENTICATION_DATABASE
        return None

    def db_for_write(self, model, **hints):
        "Point all operations on auth models to 'AUTHENTICATION_DATABASE'"
        if model._meta.app_label == 'auth' and settings.AUTHENTICATION_DATABASE:
            return settings.AUTHENTICATION_DATABASE
        return None

    def allow_relation(self, obj1, obj2, **hints):
        "Allow any relation if a model in Auth is involved"
        if obj1._meta.app_label == 'auth' or obj2._meta.app_label == 'auth':
            return True
        return None

    def allow_syncdb(self, db, model):
        "Make sure the auth app only appears on the 'AUTHENTICATION_DATABASE' db"
        if settings.AUTHENTICATION_DATABASE and db == settings.AUTHENTICATION_DATABASE:
            return model._meta.app_label == 'auth'
        elif model._meta.app_label == 'auth':
            return False
        return None


