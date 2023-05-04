from django.db import models
from django.utils.translation import gettext as _
import uuid


class Secret(models.Model):
    DAYS_7 = '7 days'
    DAYS_3 = '3 days'
    DAY_1 = '1 day'
    HOURS_12 = '12 hours'
    HOURS_4 = '4 hours'
    HOUR_1 = '1 hour'
    MINUTES_30 = '30 minutes'
    MINUTES_5 = '5 minutes'

    LIFETIME = (
        (DAYS_7, '7 дней'),
        (DAYS_3, '3 дня'),
        (DAY_1, '1 день'),
        (HOURS_12, '12 часов'),
        (HOURS_4, '4 часа'),
        (HOUR_1, '1 час'),
        (MINUTES_30, '30 минут'),
        (MINUTES_5, '5 минут'),
    )

    key = models.CharField(max_length=100, verbose_name=_('Пароль'))
    phrases = models.TextField(_('Фраза'))
    lifetime = models.CharField(max_length=50, choices=LIFETIME, default=DAYS_7, verbose_name=_('Время хранения'))
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='UUID')
    delete_data = models.DateTimeField(verbose_name=_('Дата удаления'), blank=True, null=True)

    class Meta:
        verbose_name = _('Секрет')
        verbose_name_plural = _('Секреты')

    def __str__(self):
        return f'{self.uuid}'