from django.db import connections
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.template import RequestContext

try:
    from django.conf import settings
except ImportError:
    settings = {'REQUIRED_PERMISSIONS':[], 'AUTHENTICATION_DATABASE': 'default'}

# will use the AUTHENTICATION_DATABASE settings if available

# Middleware to ensure authenticated users have the correct permissions
required_permissions = settings.REQUIRED_PERMISSIONS or []
class RequiredPermissions:

    def process_request(self, request):
        if request.user.is_anonymous(): 
            return None
        if 'logout' in request.path:
            return None
        perms = request.user.get_all_permissions()
        if perms.intersection(set(required_permissions)):
            return None
        return render_to_response('not_allowed.html', dict(),
            context_instance=RequestContext(request))

class ModelBackend(object):
    """
    Authenticates against django.contrib.auth.models.User.
    """
    supports_object_permissions = False
    supports_anonymous_user = True

    # TODO: Model, login attribute name and password attribute name should be
    # configurable.
    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_group_permissions(self, user_obj):
        """
        Returns a set of permission strings that this user has through his/her
        groups.
        """
        if not hasattr(user_obj, '_group_perm_cache'):
            database = settings.AUTHENTICATION_DATABASE or 'default'
            cursor = connections[database].cursor()
            qn = connections[database].ops.quote_name
            sql = """
                SELECT ct.%s, p.%s
                FROM %s p, %s gp, %s ug, %s ct
                WHERE p.%s = gp.%s
                    AND gp.%s = ug.%s
                    AND ct.%s = p.%s
                    AND ug.%s = %%s""" % (
                qn('app_label'), qn('codename'),
                qn('auth_permission'), qn('auth_group_permissions'),
                qn('auth_user_groups'), qn('django_content_type'),
                qn('id'), qn('permission_id'),
                qn('group_id'), qn('group_id'),
                qn('id'), qn('content_type_id'),
                qn('user_id'),)
            cursor.execute(sql, [user_obj.id])
            user_obj._group_perm_cache = set(["%s.%s" % (row[0], row[1]) for row in cursor.fetchall()])
        return user_obj._group_perm_cache

    def get_all_permissions(self, user_obj):
        if user_obj.is_anonymous():
            return set()
        if not hasattr(user_obj, '_perm_cache'):
            user_obj._perm_cache = set([u"%s.%s" % (p.content_type.app_label, p.codename) for p in user_obj.user_permissions.select_related()])
            user_obj._perm_cache.update(self.get_group_permissions(user_obj))
        return user_obj._perm_cache

    def has_perm(self, user_obj, perm):
        return perm in self.get_all_permissions(user_obj)

    def has_module_perms(self, user_obj, app_label):
        """
        Returns True if user_obj has any permissions in the given app_label.
        """
        for perm in self.get_all_permissions(user_obj):
            if perm[:perm.index('.')] == app_label:
                return True
        return False

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

