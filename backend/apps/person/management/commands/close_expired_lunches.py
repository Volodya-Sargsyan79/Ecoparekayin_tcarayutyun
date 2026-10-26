from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.person.models import LunchTime


class Command(BaseCommand):
    help = "Ավարտում է 80 րոպեն լրացած ընդմիջումները"

    def handle(self, *args, **options):
        current_datetime = timezone.now()

        expired_lunches = LunchTime.objects.filter(
            end_lanch__isnull=True,
            auto_end_at__isnull=False,
            auto_end_at__lte=current_datetime,
        )

        closed_count = 0

        for lunch in expired_lunches:
            end_datetime = timezone.localtime(lunch.auto_end_at)

            lunch.end_lanch = end_datetime.time().replace(
                microsecond=0
            )
            lunch.duration = 5
            lunch.ended_automatically = True

            lunch.save()

            closed_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Ավարտվել է {closed_count} ընդմիջում"
            )
        )
