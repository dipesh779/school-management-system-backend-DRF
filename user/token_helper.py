from user.models import MyUser


def token_helper(request=None, **kwargs):
    user_id = request._auth.payload['user_id']
    user = MyUser.objects.get(id=user_id)
    if user.schools is not None:
        school = user.schools
        return school
