# Generated by Django 3.2 on 2023-05-04 09:12

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Secret',
            fields=[
                ('key', models.CharField(max_length=100, verbose_name='Пароль')),
                ('phrases', models.TextField(verbose_name='Фраза')),
                ('lifetime', models.CharField(choices=[('7 days', '7 дней'), ('3 days', '3 дня'), ('1 day', '1 день'), ('12 hours', '12 часов'), ('4 hours', '4 часа'), ('1 hour', '1 час'), ('30 minutes', '30 минут'), ('5 minutes', '5 минут')], default='7 days', max_length=50, verbose_name='Время хранения')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='UUID')),
                ('delete_data', models.DateTimeField(blank=True, null=True, verbose_name='Дата удаления')),
            ],
            options={
                'verbose_name': 'Секрет',
                'verbose_name_plural': 'Секреты',
            },
        ),
    ]
