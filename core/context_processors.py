### Context processors added to the base of all templates

def notifications(request):
    from django.conf import settings
    from messaging.redis_config import Helper
    helper = Helper()
    notification_objects = helper.get_notifications(request.user.id)
    return {'notifications': notification_objects}
