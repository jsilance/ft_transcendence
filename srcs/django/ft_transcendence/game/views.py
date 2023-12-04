from django.shortcuts import render, redirect
from .models import Shape, MapSettings
from django.contrib.auth.decorators import login_required
from .generatemap import generatemap
import json
from .forms import PartyForm

def game(request, party_id):
	shapes = [{"type":int(x.type), "color":x.color, "posx":int(x.posx), "posy":int(x.posy)} for x in Shape.objects.all()]
	
	mapSetting = MapSettings.objects.get(id=party_id)
	map_json = json.dumps(mapSetting.to_json())

	user = request.user

	shape_json = json.dumps(shapes)
	context = {'shapes': shape_json, 'mapSetting': map_json}
	return render(request, 'game.html', context)

@login_required
def websocket_test(request, party_id):
	return render(request, 'chatbox.html')

@login_required
def lobby(request):
	parties = MapSettings.objects.all()
	user = request
	if request.method == 'POST':
		form = PartyForm(request.POST)
		if form.is_valid():
			page = form.save()
			return redirect('/game/' + str(page.id), page=page)
	else:
		form = PartyForm()
	return render(request, 'lobby.html', {'parties': parties, 'form': form, 'user': user})
