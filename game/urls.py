from django.conf.urls import patterns, url

from Fydlyty2.game.views import create_scenario, game


urlpatterns = patterns('',

    url( r'^$',
        game,
        {'template_name': 'game/game.html'},
        name = 'game' ),

    url( r'^scenario/$',
        create_scenario,
        {'template_name': 'game/create_scenario.html'},
        name = 'create_scenario' ),
)
