from django.conf import settings
import googleapiclient.discovery
from google.oauth2 import service_account


class Google:
    def __init__(self):
        scopes = [
            "https://www.googleapis.com/auth/admin.directory.user",
            "https://www.googleapis.com/auth/calendar",
        ]
        self.credentials = service_account.Credentials.from_service_account_info(
            settings.GOOGLE_SERVICE_ACCOUNT_INFO, scopes=scopes
        )

    def get_latest_event_for(self, email):
        delegated_creds = self.credentials.with_subject(email)

        gcal = googleapiclient.discovery.build(
            "calendar", "v3", credentials=delegated_creds
        )

        now = datetime.datetime.utcnow()
        events_result = (
            gcal.events()
            .list(
                calendarId="primary",
                timeMin=now.isoformat() + "Z",
                timeMax=(now + datetime.timedelta(seconds=1)).isoformat() + "Z",
                maxResults=5,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )

    def get_all_user_aliases(self):
        delegated_creds = self.credentials.with_subject(settings.GOOGLE_ADMIN_EMAIL)
        gdir = googleapiclient.discovery.build(
            "admin", "directory_v1", credentials=delegated_creds
        )

        users = []
        next_page_token = None
        while True:
            results = (
                gdir.users()
                .list(domain="opendoor.com", maxResults=500, pageToken=next_page_token)
                .execute()
            )
            users += results["users"]

            next_page_token = results.get("nextPageToken")
            if not next_page_token:
                break

        return [
            [u["primaryEmail"].lower()]
            + [a.lower() for a in u.get("aliases", []) if a.endswith("@opendoor.com")]
            for u in users
        ]
