from rest_framework import serializers
from .models import Player, Game

class PlayerInscriptionSerializer(serializers.Serializer) :
    password = serializers.CharField()
    nom = serializers.CharField()
    class Meta:
        model = Player
        fields = ["nom","password"]

class DetGamSerializer(serializers.Serializer) : 
    id_one = serializers.CharField()
    id_two = serializers.CharField()

class GameIdSerializer(serializers.ModelSerializer) :
    id = serializers.IntegerField()
    class Meta:
        model = Game
        fields = ["id"]

class GameSerializer(serializers.ModelSerializer) : 
    class Meta:
        model = Game
        fields = ["color", "canvasheight", "canvaswidth", "boardwidth", "boardheight", "boardposition", "boardspeed", "boardrightkey", "boardleftkey", "gamecolor", "dividergradient", "textcolor", "basespeed", "speedboost", "timelimit", "ballradius", "startballkey", "usernamesize", "scoresize", "timesize", "turnlimitwidth", "timelimitwidth", "font", "turnradius", "timeradius", "boardtime", "turntime"]    