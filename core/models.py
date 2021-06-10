from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models import Q


class UserManager(BaseUserManager):

    def create_user(self, username, password=None):
        if not username:
            raise ValueError('Username is required!')

        user = self.model(
            username=username
        )

        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None):
        if not username:
            raise ValueError('Username is required!')

        user = self.create_user(
            username=username
        )
        user.set_password(password)
        user.is_active = True
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True

        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(verbose_name='User Name', max_length=60, null=False, blank=False, unique=True)
    date_joined = models.DateTimeField(verbose_name='Date Joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='Last Login', auto_now=True)

    is_active = models.BooleanField(verbose_name='Is Active', default=True)
    is_staff = models.BooleanField(verbose_name='Is Staff', default=False)
    is_admin = models.BooleanField(verbose_name='Is Admin', default=False)
    is_superuser = models.BooleanField(verbose_name='Is Superuser', default=False)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ('date_joined',)

    USERNAME_FIELD = 'username'

    objects = UserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class ProductManager(models.Manager):
    def search(self, query):
        lookup = (
                Q(title__icontains=query) |
                Q(description__icontains=query)

        )
        return self.get_queryset().filter(lookup).distinct()


class Task(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(verbose_name='Title', max_length=200)
    description = models.TextField(verbose_name='Description', null=True, blank=True)
    complete = models.BooleanField(verbose_name='Completed', default=False)
    created = models.DateTimeField(verbose_name='Date Created', auto_now_add=True)

    objects = ProductManager()

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        # ordering = ('created',)
        order_with_respect_to = 'user'

    def __str__(self):
        return self.title

    @property
    def get_absolute_url(self):
        return f'/task-detail/{self.id}'
