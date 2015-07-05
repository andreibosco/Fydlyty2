from django.conf.urls import patterns, url

from Fydlyty2.game.views import confirm_basic_scenario, confirm_complex_scenario, create_basic_scenario, create_complex_scenario, debrief, game, get_dialogues, scenarios_list


urlpatterns = patterns('',

    url( r'^(?P<script_id>\d+)/$',
        game,
        {'template_name': 'game/game.html'},
        name = 'game' ),

    url( r'^scenario/basic/$',
        create_basic_scenario,
        {'template_name': 'game/create_basic_scenario.html'},
        name = 'create_basic_scenario' ),

    url( r'^scenario/complex/$',
        create_complex_scenario,
        {'template_name': 'game/create_complex_scenario.html'},
        name = 'create_complex_scenario' ),

    url( r'^scenario/basic/(?P<scenario_id>\d+)/confirm/$',
        confirm_basic_scenario,
        {'template_name': 'game/confirm_basic_scenario.html'},
        name = 'confirm_basic_scenario' ),

    url( r'^scenario/complex/(?P<scenario_id>\d+)/confirm/$',
        confirm_complex_scenario,
        {'template_name': 'game/confirm_complex_scenario.html'},
        name = 'confirm_complex_scenario' ),

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
