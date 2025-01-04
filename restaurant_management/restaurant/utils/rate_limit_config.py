from rest_framework.throttling import SimpleRateThrottle

class BurstRateThrottle(SimpleRateThrottle):
    """
    Appears at the half of the rate 60 = 30.  
    """
    scope = 'burst'
    rate = '60/minute'

    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            return f"{self.scope}_{request.user.id}"
        return self.get_ident(request)


class SustainedRateThrottle(SimpleRateThrottle):
    scope = 'sustained'
    rate = '200/hour'


    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            return f"{self.scope}_{request.user.id}"
        return self.get_ident(request)
