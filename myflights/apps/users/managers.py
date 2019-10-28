from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    """Custom User Manager
    """

    def _create_user(self, email, password, **extra_fields):
        """Create and save a user with the given email, and password.

        :param email: email of a user
        :type email: str
        :param password: password of a user
        :type password: str
        :param extra_fields: keyword arguments to be passed through
        User.__init__ method
        :type extra_fields: Dict[str, Any]
        """

        if not email:
            raise ValueError('The email must be set')

        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_user(self, email, password, **extra_fields):
        """Create and save a regular user with the given email, and password.

        :param email: email of a user
        :type email: str
        :param password: password of a user
        :type password: str
        :param extra_fields: keyword arguments to be passed through
        User.__init__ method
        :type extra_fields: Dict[str, Any]
        """

        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a super user with the given email, and password.

        :param email: email of a user
        :type email: str
        :param password: password of a user
        :type password: str
        :param extra_fields: keyword arguments to be passed through
        User.__init__ method
        :type extra_fields: Dict[str, Any]
        """

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)
