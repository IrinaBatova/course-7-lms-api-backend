# from tokenize import group
# from venv import create

from django.contrib.auth.models import Group
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = "Создание группы Модераторы в базе данных"

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name="Модераторы")

        if created:
            self.stdout.write(
                self.style.SUCCESS('Группа "Модераторы" успешно создана!')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Группа "Модераторы" уже существует в базе данных.')
            )
