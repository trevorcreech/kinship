import datetime

import bleach
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
import googleapiclient.discovery
from google.oauth2 import service_account

from people.models import Teammate, Team


@login_required
def index(request):
    tm = Teammate.objects.filter(is_hidden=False).order_by("id")

    team_results = None
    name_search = request.GET.get("name_search", "").split(" ")

    if name_search != [""]:
        team_results = Team.objects.all()
        for token in name_search:
            tm = tm.filter(
                Q(name__icontains=token)
                | Q(slack_display_name__icontains=token)
                | Q(location__icontains=token)
                | Q(title__icontains=token)
            )
            team_results = team_results.filter(
                Q(name__icontains=token) | Q(purpose__icontains=token)
            )

    paginator = Paginator(tm, 24)  # 24 teammates per page
    tm_page = paginator.get_page(request.GET.get("page"))
    return render(
        request,
        "people/home.html",
        {
            "teammates_page": tm_page,
            "name_search": " ".join(name_search),
            "team_results": team_results,
        },
    )


@login_required
def person(request, slack_uid, template="people/employee.html", context={}):
    teammate = get_object_or_404(
        Teammate.objects.select_related("manager").prefetch_related(
            "props_gotten", "props_gotten__teammate_from"
        ),
        slack_uid=slack_uid,
    )
    return render(request, template, {**{"teammate": teammate}, **context})


@login_required
def team(request, team_id):
    team = get_object_or_404(
        Team.objects.select_related("parent")
        .prefetch_related("subteams")
        .prefetch_related("subteams__subteams")
        .prefetch_related("subteams__members")
        .prefetch_related("subteams__subteams__members"),
        id=team_id,
    )
    return render(request, "people/team.html", {"team": team})


@login_required
def is_free(request, slack_uid):
    teammate = get_object_or_404(Teammate, slack_uid=slack_uid)

    SCOPES = ["https://www.googleapis.com/auth/calendar"]
    credentials = service_account.Credentials.from_service_account_info(
        settings.GOOGLE_SERVICE_ACCOUNT_INFO, scopes=SCOPES
    )
    delegated_credentials = credentials.with_subject(teammate.slack_email)

    gcal = googleapiclient.discovery.build(
        "calendar", "v3", credentials=delegated_credentials
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
    events = events_result.get("items", [])

    if not events:
        current_meeting = {"is_free": True}
        return JsonResponse(current_meeting)

    current_meeting = {"is_free": False}
    return JsonResponse(current_meeting)


@login_required
def okrs(request, slack_uid):
    just_saved = False
    if request.method == "POST":
        allowed_tags = [
            "a",
            "abbr",
            "acronym",
            "b",
            "br",
            "blockquote",
            "code",
            "em",
            "h1",
            "h2",
            "h3",
            "i",
            "li",
            "ol",
            "p",
            "strong",
            "u",
            "ul",
        ]
        request.user.teammate.okrs = bleach.clean(
            request.POST["okr_html"], tags=allowed_tags
        )
        request.user.teammate.save()
        just_saved = True

    return person(
        request,
        slack_uid,
        template="people/personal_okrs.html",
        context={"just_saved": just_saved},
    )


def _render_node(node, has_sibs):
    parent = "0" if node.is_root_node() else "1"
    sibs = "1" if has_sibs else "0"
    childs = "0" if node.is_leaf_node() else "1"

    if node.name == "Eric Wu":
        # all root nodes are considered siblings of each other, so we have to special case Eric,
        # who is supposed to be the only root node in this org
        sibs = "0"

    return {
        "id": node.slack_uid,
        "name": node.name,
        "title": node.title,
        "relationship": parent + sibs + childs,
    }


@login_required
def org_chart(request, slack_uid):
    return person(request, slack_uid, template="people/org_chart.html")


@login_required
def children_json(request, slack_uid):
    tm = Teammate.objects.get(slack_uid=slack_uid)
    children = tm.get_children().filter(is_hidden=False)
    out = {
        "children": [
            _render_node(child, has_sibs=(len(children) > 1)) for child in children
        ]
    }
    return JsonResponse(out)


@login_required
def parent_json(request, slack_uid):
    tm = Teammate.objects.get(slack_uid=slack_uid)
    if not tm.manager:
        return JsonResponse({})

    return JsonResponse(
        _render_node(tm.manager, has_sibs=tm.manager.get_siblings().count())
    )


@login_required
def sibs_json(request, slack_uid):
    tm = Teammate.objects.get(slack_uid=slack_uid)
    sibs = tm.get_siblings().filter(is_hidden=False)
    out = {"siblings": [_render_node(sib, has_sibs=True) for sib in sibs]}
    return JsonResponse(out)


@login_required
def family_json(request, slack_uid):
    node = Teammate.objects.get(slack_uid=slack_uid)

    target = _render_node(
        node, has_sibs=node.get_siblings().filter(is_hidden=False).count()
    )
    direct_reports = node.get_children().filter(is_hidden=False)
    target["children"] = [
        _render_node(report, has_sibs=(len(direct_reports) > 1))
        for report in direct_reports
    ]

    if request.GET.get("target_mgr") and node.manager:
        manager = _render_node(
            node.manager,
            has_sibs=node.manager.get_siblings().filter(is_hidden=False).count(),
        )

        if not request.GET.get("exclude_me"):
            manager["children"] = [target]
        else:
            manager["children"] = [
                _render_node(mgr_sib, has_sibs=True)
                for mgr_sib in node.get_siblings().filter(is_hidden=False)
            ]

        target = manager

    return JsonResponse(target)


@login_required
def team_list(request):
    teams = Team.objects.all()
    return render(request, "people/team_list.html", {"teams": teams})
