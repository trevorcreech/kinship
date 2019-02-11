from django.core.management.base import BaseCommand, CommandError

from people.api_clients.workday import Workday


class Command(BaseCommand):
    def handle(self, *args, **options):
        Workday().sync_teammates()
