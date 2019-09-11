from django.db import models
from accounts.models import User
from django.utils import timezone
from groups.models import Group
from django.utils.translation import gettext_lazy as _
import uuid
import os
from django.dispatch import receiver
from datetime import datetime

#RecordImageファイル名UUID変更関数
def get_file_path(instance, filename):
  if not 'records/default.jpg' == filename:
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('records/', filename)

class UserRecordTitle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_record_title = models.CharField(_('レコードタイトル'), max_length=30,)

    def __str__(self):
        return self.user_record_title


class UserRecordContent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
    user_record_title = models.ForeignKey(UserRecordTitle,on_delete=models.CASCADE,blank=True,null=True)
    user_record_image = models.ImageField(_('写真'),upload_to=get_file_path,blank=True,default='records/default.jpg')
    user_record_content = models.CharField(_('内容'), max_length=300)
    user_record_elapsed_time = models.DurationField(_('経過時間'))
    user_record_time = models.DateTimeField(_('記録時間'), default=timezone.now)
    def __str__(self):
        return self.user_record_content


@receiver(models.signals.post_delete, sender=UserRecordContent)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if not 'records/default.jpg' == instance.user_record_image:
        if os.path.isfile(instance.user_record_image.path):
            os.remove(instance.user_record_image.path)

@receiver(models.signals.pre_save, sender=UserRecordContent)
def auto_delete_file_on_change(sender, instance, **kwargs):
  """
  Deletes old file from filesystem
  when corresponding `MediaFile` object is updated
  with new file.
  """
  if not instance.pk:
    return False

  try:
    old_file = sender.objects.get(pk=instance.pk).user_record_image
  except sender.DoesNotExist:
    return False

  new_file = instance.user_record_image

  if not old_file == new_file:
     if not 'records/default.jpg' == old_file:
      if os.path.isfile(old_file.path):
        os.remove(old_file.path)



#
# #TODO:UserRecordとまとめた方がいいのか検証後実装
# class GroupRecordTitle(models.Model):
#     group = models.ForeignKey(Group, on_delete=models.CASCADE,null=True)
#     group_record_title = models.CharField(_('練習メニュー'), max_length=30,editable=True)
#     def __str__(self):
#         return self.group_record_title
# #TODO:GRoupRecordTitleと同じ
# class GroupRecordContent(models.Model):
#     group = models.ForeignKey(Group, on_delete=models.CASCADE)
#     group_record_title = models.ForeignKey(GroupRecordTitle,on_delete=models.CASCADE)
#     group_record_image = models.ImageField(upload_to=get_file_path, blank=True, default='records/default')
#     group_record_content= models.CharField(_('練習記録'), max_length=300)
#     group_record_elapsed_time = models.DateTimeField(_('経過時間'))
#     group_record_time = models.DateTimeField(_('記録時間'), default=timezone.now)
#
#     def __str__(self):
#         return self.group_record_content
