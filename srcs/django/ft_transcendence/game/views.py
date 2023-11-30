from django.shortcuts import render
from .models import Shape, MapSettings
from django.contrib.auth.decorators import login_required
from .generatemap import generatemap
import json

def game(request, party_id):
	shapes = [{"type":int(x.type), "color":x.color, "posx":int(x.posx), "posy":int(x.posy)} for x in Shape.objects.all()]
	
	# mapSetting = [{"nbPlayer": int(x.nbPlayer), "listOfPlayer": x.listOfPlayer} for x in MapSettings.objects.all()]
	# map_json = json.dumps(mapSetting)
	# generatemap(party_id)

	shape_json = json.dumps(shapes)
	context = {'shapes': shape_json}
	return render(request, 'game.html', context)

@login_required
def websocket_test(request, party_id):
    return render(request, 'chatbox.html')

def lobby(request):
	return render(request, 'lobby.html')