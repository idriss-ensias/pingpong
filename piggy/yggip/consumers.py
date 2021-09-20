import json
from .models import Game, Player, Momo
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.layers import get_channel_layer

class PlayerConsumer(WebsocketConsumer):
    def connect(self):
        self.player = self.scope['url_route']['kwargs']['game']
        self.player_group_name = 'chat_%s' % self.player

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.player_group_name,
            self.channel_name
        )
        
        self.accept()
        self.receive('{"message":"0,'+Player.loggedoff()+'/'+Player.loggedin()+'/'+Player.waiting()+'/'+Player.playing()+'"}')

    def disconnect(self, close_code):
        gg = Game.objects.get(pk=int(self.scope['url_route']['kwargs']['game']))
        if gg.end == 1:
            gg.bye()
            print("tttteeeesssstttt-+-+-+-+")
            jq = Momo.objects.filter(game=gg) 
            if (jq.count() == 2):
                print("chopapimonanyo  wins "+str(jq[0].player.total_wins)+" losses  "+str(jq[0].player.total_losses)+" draws  "+str(jq[0].player.draws))
                siso = Player.objects.get(pk=jq[0].player.id)
                sisa = Player.objects.get(pk=jq[1].player.id)
                if (jq[0].score > jq[1].score) :
                    print("friw")
                    siso.total_wins += 1 
                    siso.save()
                    sisa.total_losses += 1 
                    sisa.save()
                elif (jq[0].score < jq[1].score) :
                    print("kriw")
                    siso.total_losses += 1 
                    siso.save()
                    sisa.total_wins += 1 
                    sisa.save()
                else : 
                    print("hriw")
                    siso.draws += 1 
                    siso.save()
                    sisa.draws += 1 
                    sisa.save()
        self.receive('{"message" : "8"}')
        async_to_sync(self.channel_layer.group_discard)(
            self.player_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        if message.split(",")[0] == "6":
            zazo = Player.objects.get(pk=Player.objects.get(pk=int(message.split(",")[1])).id)
            nano = Game.objects.get(pk=int(self.scope['url_route']['kwargs']['game']))
            fliflo = Momo.objects.filter(game=nano,player=zazo)[0]
            fliflo.goal()

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.player_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))
class NinoConsumer(WebsocketConsumer):
    def connect(self):
        self.nino = 10
        self.piko = self.scope['url_route']['kwargs']['nino']
        self.nino_group_name = 'chat_%s' % self.nino

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.nino_group_name,
            self.channel_name
        )
        pipi = Player.objects.get(pk=self.piko)
        pipi.state = 1
        pipi.save()
        self.accept()
        self.receive('{"message":"0,'+Player.loggedoff()+'/'+Player.loggedin()+'/'+Player.waiting()+'/'+Player.playing()+'"}')

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.nino_group_name,
            self.channel_name
        )
        pipi = Player.objects.get(pk=self.piko)
        if pipi.state == 1 :
            pipi.state = 0
            pipi.save()
        self.receive('{"message":"0,'+Player.loggedoff()+'/'+Player.loggedin()+'/'+Player.waiting()+'/'+Player.playing()+'"}')
    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.nino_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))
class TheConsumer(WebsocketConsumer):
    def connect(self):
        self.game = self.scope['url_route']['kwargs']['game']
        self.game_group_name = 'chat_%s' % self.game

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.game_group_name,
            self.channel_name
        )
        
        self.accept()
        gg = Game.objects.get(pk=int(self.scope['url_route']['kwargs']['game']))
        if Momo.objects.filter(game=gg.id).count() == 2 :
            self.receive('{"message":"0,'+str(Player.objects.filter(game=gg.id)[0].id)+','+Player.objects.filter(game=gg.id)[0].userplayer.username+','+str(Player.objects.filter(game=gg.id)[1].id)+','+Player.objects.filter(game=gg.id)[1].userplayer.username+'"}')

    def disconnect(self, close_code):
        gg = Game.objects.get(pk=int(self.scope['url_route']['kwargs']['game']))
        gg.end = 0
        gg.save()
        if gg.timeup == 1 : 
            tara = Player.objects.get(pk=Momo.objects.filter(game=gg.id)[0].player.id)
            tari = Player.objects.get(pk=Momo.objects.filter(game=gg.id)[1].player.id)
            khakha = 0
            if tara.state + tari.state == 0 :
                for i in Momo.objects.filter(game=gg.id):
                    khakha += i.score
                if Momo.objects.filter(game=gg.id,player=tara.id)[0].score < Momo.objects.filter(game=gg.id,player=tari.id)[0].score :
                    tara.total_losses += 1
                    if tara.score > 0 :
                        tara.score -= 1
                    tara.save()
                    if tara.score > 0 :
                        tara.rank = tara.rank_player()
                    tara.save()
                    tari.total_wins += 1
                    tari.score += khakha + 1
                    tari.save()
                    tari.rank = tari.rank_player()
                    tari.save()
                elif Momo.objects.filter(game=gg.id,player=tara.id)[0].score > Momo.objects.filter(game=gg.id,player=tari.id)[0].score :
                    tara.total_wins += 1
                    tara.score += khakha + 1
                    tara.save()
                    tara.rank = tara.rank_player()
                    tara.save()
                    tari.total_losses += 1
                    if tari.score > 0 :
                        tari.score -= 1
                    tari.save()
                    if tari.score > 0 :
                        tari.rank = tari.rank_player()
                    tari.save()
                elif Momo.objects.filter(game=gg.id,player=tara.id)[0].score == Momo.objects.filter(game=gg.id,player=tari.id)[0].score :
                    tara.draws += 1
                    tara.save()
                    tari.draws += 1
                    tari.save() 
        for i in Momo.objects.filter(game=gg.id):
            piy = Player.objects.get(pk=i.player.id)
            piy.state = 0
            piy.save()
        self.receive('{"message":"1"}')
        async_to_sync(self.channel_layer.group_discard)(
            self.game_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        if message.split(",")[0] == "2":
            print("hihi")
            winp = Player.objects.get(pk=int(message.split(",")[1]))
            print(winp.userplayer.username)
            winp.total_wins += 1
            winp.score += 1
            winp.save()
            winp.rank = winp.rank_player()
            winp.save()
            ggg = Game.objects.get(pk=int(message.split(",")[2]))
            losp = Player.objects.filter(game=ggg.id).exclude(pk=winp.id)[0]
            print(losp.userplayer.username)
            losp.total_losses += 1
            if losp.score > 0 :
                losp.score -= 1
            losp.save()
            if losp.score > 0 :
                losp.rank = losp.rank_player()
            losp.save()
            print(winp)
            print(ggg)
            print(losp)
        if message.split(",")[0] == "8":
            gg = Game.objects.get(pk=int(self.scope['url_route']['kwargs']['game']))
            gg.timeup = 1
            gg.save()
        if message.split(",")[0] == "7":
            gg = Game.objects.get(pk=int(self.scope['url_route']['kwargs']['game']))
            nono = Momo.objects.filter(game=gg.id,player=int(message.split(",")[1]))[0]
            if nono.score < int(message.split(",")[2]) : 
                nono.score = int(message.split(",")[2])
                nono.save()
            cholo =  Momo.objects.filter(game=gg.id).exclude(player=int(message.split(",")[1]))[0]
            if cholo.score < int(message.split(",")[3]) : 
                cholo.score = int(message.split(",")[3])
                cholo.save()
        if message.split(",")[0] == "14":
            zara = Momo.objects.filter(game=int(message.split(",")[1]),player=int(message.split(",")[2]))[0]
            zara.score = int(message.split(",")[4])
            zara.save()
            zari = Momo.objects.filter(game=int(message.split(",")[1]),player=int(message.split(",")[3]))[0]
            zari.score = int(message.split(",")[5])
            zari.save()
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.game_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))
class PageConsumer(WebsocketConsumer):
    def connect(self):
        self.player = 11
        self.player_group_name = 'chat_%s' % self.player

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.player_group_name,
            self.channel_name
        )
        
        self.accept()
        niko = str(self.scope['url_route']['kwargs']['player'])
        moko = str(self.scope['url_route']['kwargs']['mode'])
        flang = Player.objects.get(pk=int(niko))
        flang.state = int(moko)
        flang.save()
        self.receive('{"message":"12,'+niko+','+moko+'"}')

    def disconnect(self, close_code):
        niko = str(self.scope['url_route']['kwargs']['player'])
        flang = Player.objects.get(pk=int(niko))
        flang.state = 0
        flang.save()
        self.receive('{"message":"12,'+niko+',0"}')
        async_to_sync(self.channel_layer.group_discard)(
            self.player_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        if message.split(",")[0] == "27":
            tassa = Player.objects.get(pk=int(message.split(",")[1]))
            tassi = Player.objects.get(pk=int(message.split(",")[2]))
            tassa.state = 3
            tassa.save()
            self.receive('{"message":"12,'+str(tassa.id)+',3"}')
            tassi.state = 3
            tassi.save()
            self.receive('{"message":"12,'+str(tassi.id)+',3"}')
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.player_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))