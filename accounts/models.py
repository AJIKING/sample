from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.conf import settings
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import RegexValidator
import uuid as uuid_lib
from django.dispatch import receiver
import os
import uuid
from uuid import UUID
from json import JSONEncoder
from groups.models import Group

#ImageFileの名前をUUIDに設定する関数
def get_file_path(instance, filename):
  ext = filename.split('.')[-1]
  filename = "%s.%s" % (uuid.uuid4(), ext)
  return os.path.join('profile/', filename)


#JSONEncordeするための関数
JSONEncoder_olddefault = JSONEncoder.default

def JSONEncoder_newdefault(self, o):
    if isinstance(o, UUID): return str(o)
    return JSONEncoder_olddefault(self, o)

JSONEncoder.default = JSONEncoder_newdefault



class UserManager(BaseUserManager):
    #UserManagerクラスは、ユーザ名、メールアドレス、パスワードに関するメソッドを提供するBaseUserManagerを継承
    use_in_migrations = True
    #クラスをRunPython操作で利用できる

    def _create_user(self, username,email, password, **extra_fields):
        #与えられたユーザ名、電子メール、およびパスワードでユーザーを作成して保存する関数

        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username,email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username,email, password, **extra_fields)

    def create_superuser(self, username,email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
      alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'ユーザーネームはアルファベットか数字のみです。')

      user_id = models.UUIDField(default=uuid_lib.uuid4,
                              primary_key=True, editable=False)
      username = models.CharField(_('ユーザーネーム'), unique=True, max_length=50,validators=[alphanumeric],error_messages={
              'unique': _("A user with that username already exists."),
          },)
      email = models.EmailField(_('email address'), unique=True)


      is_staff = models.BooleanField(
          _('staff status'),
          default=False,
          help_text=_('Designates whether the user can log into this admin site.'),
      )
      is_active = models.BooleanField(
          _('active'),
          default=True,
          help_text=_(
              'Designates whether this user should be treated as active. '
              'Unselect this instead of deleting accounts.'
          ),
      )
      date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

      objects = UserManager()

      EMAIL_FIELD = 'email'
      USERNAME_FIELD = 'username'
      REQUIRED_FIELDS = ['email']

      class Meta:
          verbose_name = _('user')
          verbose_name_plural = _('users')


      def email_user(self, subject, message, from_email=None, **kwargs):
          """Send an email to this user."""
          send_mail(subject, message, from_email, [self.email], **kwargs)

      def user_name(self):
          """username属性のゲッター

                 他アプリケーションが、username属性にアクセスした場合に備えて定義
                 メールアドレスを返す
                 """
          return self.username





class UserProfile(models.Model):
      user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, )
      user_image = models.ImageField(upload_to=get_file_path,default='profile/default')
      first_name = models.CharField(_('first name'), max_length=30, blank=True,null=True)
      last_name = models.CharField(_('last name'), max_length=150, blank=True,null=True)
      birthday = models.DateField(_('生年月日'),blank=True,null=True)


      def get_full_name(self):
          """
          Return the first_name plus the last_name, with a space in between.
          """
          full_name = '%s %s' % (self.first_name, self.last_name)
          return full_name.strip()

      def get_short_name(self):
          """Return the short name for the user."""
          return self.first_name

      def __str__(self):
          return str(self.user)


class UserBelong(models.Model):
      user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_profile')
      group = models.ForeignKey(Group, on_delete=models.CASCADE)
      position = models.CharField(_('役職'), max_length=20, null=True, blank=True)
      sports_position = models.CharField(_('スポーツポジション'), max_length=20, null=True, blank=True)
      school_year = models.IntegerField(_('学年'), null=True, blank=True)
      approval = models.BooleanField(_('承認'), default=False)

      def __str__(self):
        return str(self.user)

@receiver(models.signals.post_delete, sender=UserProfile)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if not 'default' == instance.user_image:
        if os.path.isfile(instance.user_image.path):
            os.remove(instance.user_image.path)

@receiver(models.signals.pre_save, sender=UserProfile)
def auto_delete_file_on_change(sender, instance, **kwargs):
  """
  Deletes old file from filesystem
  when corresponding `MediaFile` object is updated
  with new file.
  """
  if not instance.pk:
    return False

  try:
    old_file = sender.objects.get(pk=instance.pk).user_image
  except sender.DoesNotExist:
    return False

  new_file = instance.user_image
  if not old_file == new_file:
     if not 'profile/default' == old_file:
      if os.path.isfile(old_file.path):
        os.remove(old_file.path)








