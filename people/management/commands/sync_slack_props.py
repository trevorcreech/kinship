import re
from datetime import datetime
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from pytz import timezone
from slackclient import SlackClient
from people.models import Teammate, PropsMessage

PROPS_CHANNEL_ID = "C0CFF4R6F"


class Command(BaseCommand):
    def handle(self, *args, **options):
        sc = SlackClient(settings.SLACK_OAUTH_ACCESS_TOKEN)

        latest = None
        props_msgs = []
        while True:
            response = sc.api_call(
                "channels.history", channel=PROPS_CHANNEL_ID, count=1000, latest=latest
            )
            if not response["ok"]:
                raise CommandError("Bad response from slack on history: %s" % response)

            for msg in response["messages"]:
                latest = msg["ts"]
                if (
                    msg["type"] != "message"
                    or "subtype" in msg
                    or "parent_user_id" in msg
                ):
                    continue
                props_msgs.append(msg)
            if not response["has_more"]:
                break

        print("fetched %s props messages from slack." % len(props_msgs))

        existing_props_ts = PropsMessage.objects.values_list(
            "identifying_ts", flat=True
        )

        teammates = {f"<@{t.slack_uid}>": t for t in Teammate.objects.all()}

        at_mention_pattern = re.compile(r"<@(.*?)>")
        tz = timezone(settings.TIME_ZONE)

        for msg in props_msgs:
            if msg["ts"] in existing_props_ts:  # we've already saved this in the db
                continue

            if not self.eligible(msg):
                continue

            mentioned_teammates = [
                teammates[f"<@{uid}>"]
                for uid in re.findall(at_mention_pattern, msg["text"])
            ]
            parsed_text = re.sub(
                r"<@(.*?)>",
                lambda match: "@" + teammates[match.group(0)].name,
                msg["text"],
            )

            props = PropsMessage()
            props.teammate_from = teammates[f"<@{msg['user']}>"]
            props.text = parsed_text
            props.sent_on = tz.localize(datetime.fromtimestamp(float(msg["ts"])))
            props.identifying_ts = msg["ts"]
            props.save()

            props.teammates_to.set(mentioned_teammates)

    @classmethod
    def eligible(cls, msg):
        return not cls.is_invite_message(msg)

    @classmethod
    def is_invite_message(cls, msg):
        # one or more mentions separated by whitespace
        invites_pattern = re.compile(r"^(<@(\w+)>\s*)+$")
        return re.match(invites_pattern, msg['text'].strip()) and not msg.get('files') and not msg.get('attachments')
