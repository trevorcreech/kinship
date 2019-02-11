import pytest
from people.api_clients.google import Google
from people.api_clients.slack import Slack
from people.api_clients.workday import Workday
from people.models import Teammate
from people.tests.mock_data import SLACK_RESPONSE, WORKDAY_RESPONSE


@pytest.fixture
def mock_slack(mocker):
    mocker.patch.object(
        Slack, "fetch_user_list", autospec=True, return_value=SLACK_RESPONSE
    )


@pytest.fixture
def mock_google_directory(mocker):
    mocker.patch.object(
        Google,
        "get_all_user_aliases",
        autospec=True,
        return_value=[["cookie@opendoor.com", "cookie.monster@opendoor.com"]],
    )


@pytest.fixture
def mock_workday(mocker, mock_google_directory):
    mocker.patch.object(
        Workday, "fetch_records", autospec=True, return_value=WORKDAY_RESPONSE
    )


@pytest.mark.django_db
class TestTeammateSync:
    def test_slack(self, mock_slack):
        slack = Slack()
        slack.sync_teammates()

        assert Teammate.objects.count() == 2

        bird = Teammate.objects.get(slack_email="bigbird@opendoor.com")
        cookie = Teammate.objects.get(slack_email="cookie.monster@opendoor.com")

        assert bird.name == "Big Bird"
        assert bird.title == "Silly Title On Slack"
        assert bird.slack_display_name == "bigbird"
        assert cookie.name == "Cookie Monster (Slack Name With Garbage)"
        assert cookie.title == "Chief of Cookie"
        assert cookie.slack_display_name == "Cookie Monster"

    def test_workday_after_slack(self, mock_slack, mock_workday):
        slack = Slack()
        slack.sync_teammates()

        workday = Workday()
        workday.sync_teammates()

        assert Teammate.objects.count() == 2
        bird = Teammate.objects.get(slack_email="bigbird@opendoor.com")
        cookie = Teammate.objects.get(slack_email="cookie.monster@opendoor.com")

        assert bird.name == "Big Bird"
        assert bird.title == "Overridden Title From Workday"  # overridden by Workday

        assert cookie.manager == bird
        assert bird.manager == None

    def test_workday_sync_overrides_slack_with_aliases(self, mock_slack, mock_workday):
        # Cookie Monster has the email cookie.monster@opendoor.com in SLACK_RESPONSE but
        # cookie@opendoor.com in WORKDAY_RESPONSE. the two are joined by a Google aliases
        # search, mocked out.
        slack = Slack()
        slack.sync_teammates()

        workday = Workday()
        workday.sync_teammates()

        assert Teammate.objects.count() == 2
        cookie = Teammate.objects.get(slack_email="cookie.monster@opendoor.com")

        assert cookie.name == "Cookie Monster (Workday)"  # overridden by Workday
        assert cookie.title == "Chief of Cookie"
