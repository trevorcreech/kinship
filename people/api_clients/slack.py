from django.conf import settings
from social_django.models import UserSocialAuth
from slackclient import SlackClient
from people.models import Teammate


class Slack:
    def fetch_user_list(self):
        sc = SlackClient(settings.SLACK_OAUTH_ACCESS_TOKEN)

        members = []
        cursor = None
        while True:
            response = sc.api_call("users.list", limit=1000, cursor=cursor)
            if not response["ok"]:
                raise CommandError("Bad response from slack on users: %s" % response)
            members += response["members"]
            cursor = response["response_metadata"]["next_cursor"]
            if not cursor:
                break
        return members

    def sync_teammates(self):
        members = self.fetch_user_list()
        returned_uids = [u["id"] for u in members]

        existing_teammates = {
            t.slack_uid: t for t in Teammate.objects.filter(slack_uid__in=returned_uids)
        }
        existing_users = {
            soc.uid: soc.user
            for soc in UserSocialAuth.objects.filter(provider="slack").select_related(
                "user"
            )
        }

        for s in members:
            if s["is_bot"] or s["id"] == "USLACKBOT":  # we don't want bots
                continue

            prof = s.get("profile", {})

            tm = existing_teammates.get(s["id"], Teammate())  # update or create new
            tm.slack_uid = s["id"]
            tm.slack_display_name = (
                prof.get("display_name")
                or prof.get("real_name")
                or s.get("real_name")
                or ""
            )
            tm.slack_email = prof.get("email", "")
            tm.name = (
                s.get("real_name")
                or prof.get("real_name")
                or prof.get("display_name")
                or ""
            )
            tm.title = prof.get("title", "")
            tm.phone = prof.get("phone", "")
            tm.image = prof.get("image_original") if prof.get("is_custom_image") else ""
            tm.is_hidden = (
                s.get("deleted")
                or s.get("is_restricted")
                or s.get("is_ultra_restricted")
            )
            if not tm.is_hidden and not tm.user and tm.slack_uid in existing_users:
                tm.user = existing_users[tm.slack_uid]

            try:
                tm.save()
            except Exception as ex:
                # make sure a single teammate failing to save doesn't cause the script to fail
                print(f"Failed to save {tm}")
                print(f"> {ex}\n"

        disappeared_users = Teammate.objects.exclude(
            slack_uid__in=returned_uids
        ).update(is_hidden=True)
