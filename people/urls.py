from django.urls import include, path

import people.views as people_views

urlpatterns = [
    path("", people_views.index, name="people-index"),
    path("teams", people_views.team_list, name="team-list"),
    path("team/<int:team_id>", people_views.team),
    path("<slack_uid>", people_views.person, name="teammate-detail"),
    path("<slack_uid>/is_free", people_views.is_free),
    path("<slack_uid>/okrs", people_views.okrs),
    path("<slack_uid>/org", people_views.org_chart),
    path("<slack_uid>/children.json", people_views.children_json),
    path("<slack_uid>/parent.json", people_views.parent_json),
    path("<slack_uid>/sibs.json", people_views.sibs_json),
    path("<slack_uid>/family.json", people_views.family_json),
]
