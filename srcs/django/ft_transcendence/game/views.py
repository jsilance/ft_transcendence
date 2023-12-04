from django.shortcuts import render, redirect, get_object_or_404
from .models import Shape, MapSettings
from django.contrib.auth.decorators import login_required
from .generatemap import generatemap
import json
from .forms import PartyForm

def game(request, party_id):
	user = request.user.username

	shapes = [{"type":int(x.type), "color":x.color, "posx":int(x.posx), "posy":int(x.posy)} for x in Shape.objects.all()]
	shape_json = json.dumps(shapes)
	
	mapSetting = MapSettings.objects.get(id=party_id)
	
	try:
		user_infos = json.loads(mapSetting.listOfPlayer)
		if not isinstance(user_infos, list):
			raise ValueError("listOfPlayer is not a list")
	except (json.JSONDecodeError, ValueError):
		user_infos = [{"user": user, "is_ready": False}]
		mapSetting.listOfPlayer = json.dumps(user_infos)
		mapSetting.save()

	founded = any(user_info["user"] == user for user_info in user_infos)

	if not founded and user != "/":
		user_infos.append({"user": user, "is_ready": False})
		mapSetting.listOfPlayer = json.dumps(user_infos)
		mapSetting.save()

	map_json = json.dumps(mapSetting.to_json())
	generatemap(party_id)

	context = {'shapes': shape_json, 'mapSetting': map_json, 'usern': user}
	return render(request, 'game.html', context)

@login_required
def websocket_test(request, party_id):
	return render(request, 'chatbox.html')

@login_required
def lobby(request):
	parties = MapSettings.objects.all()
	user = request.user.username

	if request.method == 'POST':
		form = PartyForm(request.POST)
		if form.is_valid():
			page = form.save()
			
			player_list = [{"user": str(user), "is_ready": False}]
			
			MapSettings.objects.filter(id=page.id).update(listOfPlayer=json.dumps(player_list))

			return redirect('/game/' + str(page.id))
	else:
		form = PartyForm()

	return render(request, 'lobby.html', {'parties': parties, 'form': form, 'user': user})
