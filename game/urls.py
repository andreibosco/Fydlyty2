from django.conf.urls import patterns, url

from Fydlyty2.game.views import confirm_scenario, create_scenario, debrief, game, get_dialogues, scenarios_list


urlpatterns = patterns('',

    url( r'^(?P<script_id>\d+)/$',
        game,
        {'template_name': 'game/game.html'},
        name = 'game' ),

    url( r'^scenario/$',
        create_scenario,
        {'template_name': 'game/create_scenario.html'},
        name = 'create_scenario' ),

    url( r'^scenario/(?P<scenario_id>\d+)/confirm/$',
        confirm_scenario,
        {'template_name': 'game/confirm_scenario.html'},
        name = 'confirm_scenario' ),

    url( r'^list/$',
        scenarios_list,
        {'template_name': 'game/scenarios_list.html'},
        name = 'scenarios_list' ),

    url( r'^$',
        get_dialogues,
        name = 'get_dialogues' ),

    url( r'^debrief/(?P<script_id>\d+)/$',
        debrief,
        {'template_name': 'game/debrief.html'},
        name = 'debrief' ),

)
