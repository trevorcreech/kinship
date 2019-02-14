import datetime
from django.contrib.auth.signals import user_logged_in
from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
from preferences.models import Preferences
from social_django.models import UserSocialAuth


class Teammate(MPTTModel):
    user = models.OneToOneField(
        "auth.User", on_delete=models.CASCADE, null=True, blank=True
    )
    slack_uid = models.CharField(max_length=255, unique=True, null=True, blank=True)
    slack_display_name = models.CharField(max_length=255, blank=True)
    slack_email = models.EmailField(blank=True)
    name = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255)
    title = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=255, blank=True)
    image = models.URLField(blank=True)
    start_date = models.DateField(null=True, blank=True)
    bday_month = models.SmallIntegerField(null=True, blank=True)
    bday_day = models.SmallIntegerField(null=True, blank=True)
    manager_name = models.CharField(max_length=255, blank=True)
    team_name = models.CharField(max_length=255, blank=True)
    workday_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    okrs = models.TextField(blank=True)
    manager = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="direct_reports",
    )

    is_hidden = models.BooleanField(default=False)

    class MPTTMeta:
        order_insertion_by = ["name"]
        parent_attr = "manager"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("teammate-detail", args=(self.slack_uid,))

    @property
    def bday(self):
        if not self.bday_month or not self.bday_day:
            return None
        return datetime.date(month=self.bday_month, day=self.bday_day, year=1)

    @property
    def main_team(self):
        try:
            return Team.objects.get(name=self.team_name)
        except Team.DoesNotExist:
            return None


class Team(MPTTModel):
    name = models.CharField(max_length=255, unique=True)
    purpose = models.TextField(blank=True)
    details_url = models.URLField(blank=True)
    contact_block = models.TextField(blank=True)
    members = models.ManyToManyField(Teammate, limit_choices_to={"is_hidden": False})
    last_modified = models.DateField(auto_now=True)

    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, related_name="subteams"
    )

    class Meta:
        ordering = ["name"]

    class MPTTMeta:
        order_insertion_by = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/people/team/{self.id}"

    @property
    def subteam_members(self):
        subteam_members = []
        subteams = self.subteams.all()
        for subteam in subteams:
            subteam_members += subteam.subteam_members

        if not subteams:
            return self.members.all()

        return subteam_members[0:250]  # TODO: lift artificial limit


class TeamMetadata(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="metadata")
    label = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    url = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.label


class PropsMessage(models.Model):
    teammate_from = models.ForeignKey(
        Teammate, related_name="props_given", on_delete=models.PROTECT
    )
    teammates_to = models.ManyToManyField(Teammate, related_name="props_gotten")
    text = models.TextField()
    sent_on = models.DateTimeField()
    identifying_ts = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ("-sent_on",)

    def __str__(self):
        return f"<@{self.teammate_from_id}> {self.text}"


class PeoplePreferences(Preferences):
    enable_google = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "People Directory Preferences"


def associate_teammate_with_user(sender, user, request, **kwargs):
    try:
        slack_auth = user.social_auth.get(provider="slack")
    except UserSocialAuth.DoesNotExist:
        return

    try:
        teammate = Teammate.objects.get(slack_uid=slack_auth.uid)
    except Teammate.DoesNotExist:
        return

    if teammate.user != user:
        teammate.user = user
        teammate.save()


user_logged_in.connect(associate_teammate_with_user)
