from users.models import Users


class UserProfile(Users):
    class Meta:
        proxy = True
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
