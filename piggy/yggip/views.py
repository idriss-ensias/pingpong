from django.shortcuts import render
from .models import Player, Game, Momo
from django.contrib.auth.models import User
from .serializers import PlayerInscriptionSerializer, DetGamSerializer, GameIdSerializer, GameSerializer
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.contrib.auth.decorators import login_required

# Create your views here.
@csrf_exempt
def inscriptionplayerview(request) :
    if request.method == "POST" :
        data = JSONParser().parse(request)
        serializer = PlayerInscriptionSerializer(data=data)
        if serializer.is_valid() :
            player = Player()
            user = User.objects.create_user(serializer.validated_data["nom"], '', serializer.validated_data["password"])
            user.save()
            player.userplayer = user
            player.rank = player.rank_player()
            player.save()
            return HttpResponse(status=200)
        else :
            return HttpResponse(status=404)
    else : 
        return render(request,"yggip/inscriptionplayer.html")
@csrf_exempt
@login_required
def custoga(request, playerid) :
    if request.method == "POST":
        data = JSONParser().parse(request)
        serializer = GameSerializer(data=data)
        if serializer.is_valid() :
            ggg = Game(color = serializer.validated_data["color"], canvasheight = serializer.validated_data["canvasheight"], canvaswidth = serializer.validated_data["canvaswidth"], boardwidth = serializer.validated_data["boardwidth"], boardheight = serializer.validated_data["boardheight"], boardposition = serializer.validated_data["boardposition"], boardspeed = serializer.validated_data["boardspeed"], boardrightkey = serializer.validated_data["boardrightkey"], boardleftkey = serializer.validated_data["boardleftkey"], gamecolor = serializer.validated_data["gamecolor"], dividergradient = serializer.validated_data["dividergradient"], textcolor = serializer.validated_data["textcolor"], basespeed = serializer.validated_data["basespeed"], speedboost = serializer.validated_data["speedboost"], timelimit = serializer.validated_data["timelimit"], ballradius = serializer.validated_data["ballradius"], startballkey = serializer.validated_data["startballkey"], usernamesize = serializer.validated_data["usernamesize"], scoresize = serializer.validated_data["scoresize"], timesize = serializer.validated_data["timesize"], turnlimitwidth = serializer.validated_data["turnlimitwidth"], timelimitwidth = serializer.validated_data["timelimitwidth"], font = serializer.validated_data["font"], turnradius = serializer.validated_data["turnradius"], timeradius = serializer.validated_data["timeradius"], boardtime = serializer.validated_data["boardtime"], turntime = serializer.validated_data["turntime"])
            pipi = Player.objects.get(pk=playerid)
            ggg.save()
            ggg.player.add(pipi)
            ggg.save()
            siri = GameIdSerializer(ggg)
            return JsonResponse(siri.data)
@csrf_exempt
@login_required
def frr(request):
    curr_p = Player.objects.filter(userplayer=User.objects.filter(username=request.user.username)[0])[0]
    return render(request,"yggip/login_redirect.html",{"player":curr_p})
@csrf_exempt
@login_required
def main_page(request) :
    curr_p = Player.objects.filter(userplayer=User.objects.filter(username=request.user.username)[0])[0]
    if curr_p.state == 0 :
        curr_p.state = 1
    curr_p.save()
    return render(request,"yggip/main.html",{"player":curr_p})
@csrf_exempt
@login_required
def zkiko(request,gameid):
    player = Player.objects.filter(userplayer=User.objects.filter(username=request.user.username)[0])[0]
    player.state = 2
    player.save()
    game = Game.objects.filter(pk=gameid)[0]
    return render(request,"yggip/zkik.html",{'player':player,'game':game})
@csrf_exempt
@login_required
def tarmac(request):
    if Player.objects.filter(state=2).count() != 0:
        available_player = Player.objects.filter(state=2)[0]
        game = Game.objects.filter(player=available_player,end=1)[0]
        available_player.state = 3
        available_player.save()
        player = Player.objects.filter(userplayer=User.objects.filter(username=request.user.username)[0])[0]
        player.state = 3
        player.save()
        game.player.add(player)
        game.save()
        return render(request, "yggip/zkik.html",{'player':player,'opponent':available_player,'game':game})
    else :
        return HttpResponse(status=404)
@csrf_exempt
@login_required
def cellulik(request,opid) :
    pipi = Player.objects.get(pk=opid)
    game = Game.objects.filter(player=pipi.id,end=1)[0]
    player = Player.objects.filter(userplayer=User.objects.filter(username=request.user.username)[0])[0]
    pipi.state = 3
    pipi.save()
    player.state = 3
    player.save()
    game.player.add(player)
    game.save()
    return render(request, "yggip/zkik.html",{'player':player,'opponent':pipi,'game':game})
@csrf_exempt
@login_required
def new_game(request,playerid) :
    newgame = Game()
    pipi = Player.objects.get(pk=playerid)
    newgame.save()
    newgame.player.add(pipi)
    newgame.save()
    siri = GameIdSerializer(newgame)
    return JsonResponse(siri.data)
@csrf_exempt
@login_required
def game_page(request) :
    curr_p = Player.objects.filter(userplayer=User.objects.filter(username=request.user.username)[0])[0]
    print("ID : "+str(curr_p.id))
    if Player.objects.filter(state=2).count() > 0 :
        op_p =  Player.objects.filter(state=2)[0]
        l_g = Game.objects.filter(player=op_p)
        curr_g = None
        for i in l_g:
            if i.player.count() == 1:
                curr_g = i
        print(curr_g)
        curr_g.player.add(curr_p)
        curr_g.save()
        op_p.state = 3
        op_p.save()
        print("ok1 : "+str(op_p.state)+" : "+str(op_p.id))
        curr_p.state = 3
        curr_p.save()
        print("ok2 : "+str(curr_p.state)+" : "+str(curr_p.id))
        return render(request,"yggip/gamepage.html",{'game':curr_g,'player':curr_p,'turn':'1'})
    else :
        curr_p.state = 2
        curr_p.save()
        curr_g = Game()
        curr_g.save()
        curr_g.player.add(curr_p)
        curr_g.save()
        return render(request,"yggip/gamepage.html",{'game':curr_g,'player':curr_p,'turn':'0'})
    return HttpResponse(status=404)  
@csrf_exempt
@login_required
def endgame(request,playerid) : 
    pipi = Player.objects.get(pk=playerid)
    pipi.state = 0
    pipi.save()
    return HttpResponse(status=200)
@csrf_exempt
@login_required
def game_det(request, gameid) :
    gego = Game.objects.get(pk=gameid)
    pinono = str(Momo.objects.filter(game=gego.id)[0].player.id)+":"+Momo.objects.filter(game=gego.id)[0].player.userplayer.username
    pinona = str(Momo.objects.filter(game=gego.id)[1].player.id)+":"+Momo.objects.filter(game=gego.id)[1].player.userplayer.username
    kato = {"id_one":pinono,"id_two":pinona}
    return JsonResponse(DetGamSerializer(kato).data,status=200)
@csrf_exempt
@login_required
def ugg_acc(request, playerid) :
    player = Player.objects.get(pk=playerid)
    player.rank = player.rank_player()
    player.save()
    winners = Player.objects.all().order_by("-score")[:10]
    roomies = Player.objects.all().order_by("userplayer__username")
    for i in winners :
        i.rank = i.rank_player()
        i.save()
    return render(request,"yggip/ugg.html",{'player':player,'winners':winners,'roomies':roomies})
@csrf_exempt
@login_required
def modifygame(request, playerid) :
    player = Player.objects.get(pk=playerid)
    return render(request,"yggip/customize_game.html",{"player":player})
@csrf_exempt
@login_required
def scatuno(request, playerid) :
    player = Player.objects.get(pk=playerid)
    return render(request,"yggip/brickbreaker.html",{"player":player})
