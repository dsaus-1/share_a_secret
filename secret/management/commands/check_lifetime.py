from django.core.management import BaseCommand
from django_celery_beat.models import PeriodicTask, IntervalSchedule



class Command(BaseCommand):
    """
    Creates a periodic task to check the lifetime
    """

    def handle(self, *args, **options):
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=5,
            period=IntervalSchedule.MINUTES,
        )


        PeriodicTask.objects.create(
            interval=schedule,  # we created this above.
            name='Check lifetime',  # simply describes this periodic task.
            task='secret.tasks.delete_after_lifetime',  # name of task.
        )