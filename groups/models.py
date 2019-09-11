from django.db import models
import uuid as uuid_lib
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator
import os
import uuid

#GroupImageのファイル名UUIDにする関数
def get_file_path(instance, filename):
  ext = filename.split('.')[-1]
  filename = "%s.%s" % (uuid.uuid4(), ext)
  return os.path.join('groups/', filename)

#
# class Prefecture(models.Model):
#     #TODO:APIの検討後実装
#     prefecture_name = models.CharField(_('prefecture_name'),max_length=20)
#
#     def __str__(self):
#         return self.prefecture_name
#
#
#
# class School(models.Model):
#   # TODO:APIの検討後実装
#     school_system = [
#         ('PS', '小学校'),
#         ('JS', '中学校'),
#         ('HS', '高校'),
#         ('UN', '大学'),
#     ]
#     school_name = models.CharField(_('学校名'), max_length=40)
#     prefecture = models.ForeignKey(Prefecture,on_delete=models.CASCADE)
#     school_system_name = models.CharField(_('school_system_name'), max_length=10,choices=school_system)
#
#     def __str__(self):
#         return self.school_name

class Group(models.Model):
    group_idvalidator = UnicodeUsernameValidator()
    group_id = models.CharField(_('グループID'), unique=True, max_length=50, validators=[group_idvalidator],
                                error_messages={
                                  'unique': _("A user with that username already exists."),
                                },)
    group_image = models.ImageField(upload_to=get_file_path, default='groups/default.jpg', blank=True)
    group_name = models.CharField(_('グループ名'), max_length=30)
    # school_name = models.ForeignKey(School,on_delete=models.CASCADE,blank=True,null=True)
    # prefecture = models.ForeignKey(Prefecture,on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self):
        return self.group_id




