import facebook
from django.conf import settings

class Facebook(object):
    def __init__(self, user=None):
        if user is None:
            self.uid = None
        else:
            self.uid = user['uid']
            self.user = user
            self.access_token = user['access_token']
            self.graph = facebook.GraphAPI(user['access_token'])


class FacebookMiddleware(object):
    def process_request(self, request):
        """
        Enables ``request.facebook`` and ``request.facebook.graph`` in your views 
        once the user authenticated the  application and connected with facebook. 
        You might want to use this if you don't feel confortable with the 
        javascript library.
        """
        fb_user = facebook.get_user_from_cookie(request.COOKIES,
          settings.FACEBOOK_API_KEY, settings.FACEBOOK_SECRET_KEY)

        if getattr(settings, 'FACEBOOK_OFFLINE_ACCESS', False):
            if request.user.is_authenticated() and not fb_user:
                profiles = request.user.facebookprofile_set.all()
                if len(profiles):
                    for profile in profiles:
                        if profile.access_token:
                            fb_user = {
                                'uid': profile.uid,
                                'access_token': profile.access_token,
                                'expires': 0,
                                'base_domain': request.META['HTTP_HOST'],
                                'secret': settings.FACEBOOK_SECRET_KEY,
                                'sig': '',
                                'session_key': 'offline',
                            }
                            break

        request.facebook = Facebook(fb_user)
        
        return None
