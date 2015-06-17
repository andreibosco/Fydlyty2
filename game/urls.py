from django.conf.urls import patterns, url

from Fydlyty2.game.views import confirm_scenario, create_scenario, game, scenarios_list


urlpatterns = patterns('',

    url( r'^$',
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
)
