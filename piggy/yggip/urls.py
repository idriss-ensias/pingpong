from django.urls import path,include
from . import views

urlpatterns = [
    path('inscription/',views.inscriptionplayerview),
    path('main/',views.main_page),
    path('game/',views.game_page),
    path('pigpog/<int:gameid>',views.zkiko),
    path('end/<int:playerid>',views.endgame),
    path('detgam/<int:gameid>',views.game_det),
    path('newgame/<int:playerid>',views.new_game),
    path('custom/<int:playerid>',views.custoga),
    path('adhere/',views.tarmac),
    path('mediocrepingpong/<int:playerid>',views.ugg_acc),
    path('modifygame/<int:playerid>',views.modifygame),
    path('start/',views.frr),
    path('bond/<int:opid>',views.cellulik),
    path('uno/<int:playerid>',views.scatuno),
]