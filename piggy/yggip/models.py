from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.related import ManyToManyField
from datetime import datetime
# Create your models here.
class Player(models.Model):
    userplayer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    state = models.IntegerField(default=0) # 0 disconnected, 1 connected, 2 waiting, 3 ingame
    total_wins = models.IntegerField(default=0)
    total_losses = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    last_seen = models.CharField(max_length=200, default=str(datetime.now()))
    score = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)
    @staticmethod
    def global_e():
        globalist = ""
        for i in Player.objects.all():
            globalist += str(i.state)+"%"+i.userplayer.username
            globalist += ";;"
        return globalist[:len(globalist)-2]
    def rank_player(self):
        upers = Player.objects.filter(score__gt = self.score)
        ina = 0
        for j in upers:
            if j == self:
                ina = 1
        if ina == 1:
            return upers.count()
        else :
            return upers.count()+1
    def logoff(self):
        self.last_seen = str(datetime.now())
        self.save()
    @staticmethod
    def waiting() :
        jiji = ""
        for i in Player.objects.filter(state=2):
            jiji = jiji+i.userplayer.username+"."
        return jiji[:len(jiji)-1]
    @staticmethod
    def playing() :
        jiji = ""
        for i in Player.objects.filter(state=3):
            jiji = jiji+i.userplayer.username+"."
        return jiji[:len(jiji)-1]
    @staticmethod
    def loggedin() :
        jiji = ""
        for i in Player.objects.filter(state=1):
            jiji = jiji+i.userplayer.username+"."
        return jiji[:len(jiji)-1]
    @staticmethod
    def loggedoff() :
        jiji = ""
        for i in Player.objects.filter(state=0):
            jiji = jiji+i.userplayer.username+"."
        return jiji[:len(jiji)-1]

class Game(models.Model):
    player = models.ManyToManyField(Player, through="Momo")
    end = models.IntegerField(default=1)
    timeup = models.IntegerField(default=0)
    color = models.CharField(max_length=200,default="black")
    canvasheight = models.IntegerField(default=600)
    canvaswidth = models.IntegerField(default=700)
    boardwidth = models.IntegerField(default=100)
    boardheight = models.IntegerField(default=10)
    boardposition = models.IntegerField(default=30)
    boardspeed = models.IntegerField(default=10)
    boardrightkey = models.IntegerField(default=39)
    boardleftkey = models.IntegerField(default=37)
    gamecolor = models.CharField(max_length=200,default="white")
    dividergradient = models.IntegerField(default=1)
    textcolor = models.CharField(max_length=200,default="#e35ee6")
    basespeed = models.IntegerField(default=6)
    speedboost = models.IntegerField(default=5)
    timelimit = models.IntegerField(default=1)
    ballradius = models.IntegerField(default=10)
    startballkey = models.IntegerField(default=32)
    usernamesize = models.IntegerField(default=50)
    scoresize = models.IntegerField(default=50)
    timesize = models.IntegerField(default=20)
    turnlimitwidth = models.IntegerField(default=4)
    timelimitwidth = models.IntegerField(default=4)
    font = models.CharField(max_length=200,default="Arial")
    turnradius = models.IntegerField(default=20)
    timeradius = models.IntegerField(default=40)
    boardtime = models.IntegerField(default=20)
    turntime = models.IntegerField(default=100)
    def bye(self):
        self.end = 0
        self.save()
        for i in Player.objects.filter(game=self):
            i.state = 0
            i.save()
    def nother(self, pik):
        for i in Momo.objects.filter(game=self) :
            if i.player.id != pik:
                return i.player

class Momo(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    def goal(self) :
        self.score = self.score + 1
        self.save()
