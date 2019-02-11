from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
import psycopg2

from people.api_clients.google import Google
from people.models import Teammate

# WANADB_IMAGE_URL = "https://wanadb.s3-us-west-2.amazonaws.com/uploads/teammate/fun/"
WANADB_IMAGE_URL = "https://wanadb.s3-us-west-2.amazonaws.com/uploads/teammate/mugshot/"


class Command(BaseCommand):
    def handle(self, *args, **options):
        conn = psycopg2.connect(settings.WANADB_DATABASE_URL)
        cur = conn.cursor()
        cur.execute(
            "SELECT id, email, mugshot FROM teammates WHERE mugshot != '' AND deleted_at IS NULL"
        )

        teammates = {t.slack_email: t for t in Teammate.objects.all()}

        aliases = Google().get_all_user_aliases()

        def aliases_for(email):
            email = email.lower()
            for a in aliases:
                if email in a:
                    return a
            return []

        def get_teammate_from_email(email):
            if email in teammates:
                return teammates[email]

            try:
                return Teammate.objects.get(slack_email__in=aliases_for(email))
            except Teammate.DoesNotExist:
                return None

        imgs = []
        for id_, email, mug_uri in cur.fetchall():
            mugshot_url = WANADB_IMAGE_URL + str(id_) + "/" + mug_uri

            tm = get_teammate_from_email(email)
            if not tm:
                continue

            tm.image = mugshot_url
            tm.save()
