from django.core.management.base import BaseCommand, CommandError
from people.api_clients.slack import Slack


class Command(BaseCommand):
    def handle(self, *args, **options):
        slack = Slack()
        slack.sync_teammates()
