from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import datetime
# Create your models here.

class schedule(models.Model):
    summary = models.CharField(_('件名'),max_length=50)
    description = models.TextField('詳細な説明', blank=True)
    start_time = models.DateTimeField('開始時間', default=datetime.time(7, 0, 0))
    end_time = models.DateTimeField('終了時間', default=datetime.time(7, 0, 0))
    created_at = models.DateTimeField('作成日', default=timezone.now)