import json
from collections import defaultdict
from dateutil.parser import parse
from django.conf import settings
import mptt, requests

from people.api_clients.google import Google
from people.models import Teammate, Team

WORKDAY_URL = "https://wd5-services1.myworkday.com/ccx/service/customreport2/opendoor/ISU_Opendoor+Intranet/Opendoor_Intranet_Report?format=json"


class Workday:
    def fetch_records(self):
        response = requests.get(WORKDAY_URL, auth=settings.WORKDAY_AUTH)
        response.raise_for_status()
        try:
            records = response.json()
        except ValueError:
            raise CommandError(f"Workday returned bad JSON:\n{workday_json}")

        if "Report_Entry" not in records:
            raise CommandError(f"No report in Workday response:\n{workday_json}")

        print(f"Got {len(records['Report_Entry'])} records from Workday.")
        return records

    def sync_teammates(self):
        records = self.fetch_records()

        teammates = {t.slack_email: t for t in Teammate.objects.all()}

        teams = {t.name: t for t in Team.objects.all()}
        teams["All Opendoor"], _ = Team.objects.get_or_create(name="Opendoor")
        team_teammembers = defaultdict(list)

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

        for r in records["Report_Entry"]:
            if "primaryWorkEmail1" not in r:
                continue

            tm = get_teammate_from_email(r["primaryWorkEmail1"])
            if not tm:
                continue

            if tm.slack_email.endswith("openlistings.com"):
                # temporary workaround for a bug where OL/OD ppl are considered two diff ppl.
                # e.g. sarah signed up for her slack account using
                # sarah@openlistings.com and then again using sarah.chung@opendoor.com.
                # the slack account w/ OL email is disabled but her workday email is that.
                # so sync_slack_users thinks these are two different people.
                # TODO: fix this bug
                continue

            tm.workday_id = r["Employee_ID"]

            tm.name = r["Preferred_Name"]
            tm.title = r["businessTitle"]
            tm.location = r["location"]

            tm.start_date = parse(r["Hire_Date"])
            tm.manager_name = r["Team_Member_s_Manager"]
            if "Date_of_Birth_without_Year" in r and r["Date_of_Birth_without_Year"]:
                tm.bday_month, tm.bday_day = (
                    int(d) for d in r["Date_of_Birth_without_Year"].split("/")
                )

            team_name = None
            try:
                team_name = r["Cost_Center_Hierarchy_group"][0]["Level_03_from_the_Top"]
                tm.team_name = team_name
            except (IndexError, KeyError):
                pass

            tm.save()

            # set teams
            if (
                r.get("Team_Member_Type") != "Employee"
                or r.get("Worker_Status") != "Active"
                or "Cost_Center_Hierarchy_group" not in r
            ):
                continue
            grp = r["Cost_Center_Hierarchy_group"][0]
            level1 = grp["Level_01_from_the_Top"]  # "All Opendoor"
            level2 = grp["Level_02_from_the_Top"]
            level3 = grp["Level_03_from_the_Top"]
            level4 = grp["Level_04_from_the_Top"]
            level5 = r["Cost_Center_-_Name"]

            if level2 not in teams:
                teams[level2], _ = Team.objects.get_or_create(
                    name=level2, parent=teams[level1]
                )
            if level3 not in teams:
                teams[level3], _ = Team.objects.get_or_create(
                    name=level3, parent=teams[level2]
                )
            if level4 not in teams:
                teams[level4], _ = Team.objects.get_or_create(
                    name=level4, parent=teams[level3]
                )
            if level5 not in teams:
                teams[level5], _ = Team.objects.get_or_create(
                    name=level5, parent=teams[level4]
                )

            team_teammembers[level5].append(tm)

        # save team teammbers
        for team_name, teammember_list in team_teammembers.items():
            teams[team_name].members.set(teammember_list)

        workday_tms = {
            t.workday_id: t for t in Teammate.objects.exclude(workday_id=None)
        }
        # second pass to set manager foreignkey
        for r in records["Report_Entry"]:
            if "primaryWorkEmail1" not in r:
                continue

            tm = get_teammate_from_email(r["primaryWorkEmail1"])
            if not tm:
                continue

            mgr_workday_id = r["Team_Member_s_Manager_group"][0]["Employee_ID1"]
            if mgr_workday_id not in workday_tms:
                continue

            tm.manager = workday_tms[mgr_workday_id]

            try:
                tm.save()
            except mptt.exceptions.InvalidMove as ex:
                print(f"Failed to save {tm.name}'s manager, {tm.manager.name}")
                print(f"> {ex}\n")

        Teammate.objects.rebuild()
        Team.objects.rebuild()
