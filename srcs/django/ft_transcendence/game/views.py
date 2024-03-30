from django.shortcuts import render, redirect, get_object_or_404
from .models import MapSettings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import json
from .forms import PartyForm

def game(request, party_id):
	user = request.user.username

	mapSetting = MapSettings.objects.get(id=party_id)
	
	# chope la partie sinon la cree
	try:
		user_infos = json.loads(mapSetting.listOfPlayer)
	except (json.JSONDecodeError, ValueError):
		user_infos = [{"user": user, "is_ready": False}]
		mapSetting.listOfPlayer = user_infos
		mapSetting.save()
	# ----------------------------- 

	founded = any(user_info["user"] == user for user_info in user_infos)

	if not founded and user != "/":

		user_infos.append({"user": user, "is_ready": False})
		mapSetting.listOfPlayer = json.dumps(user_infos)
		mapSetting.save()

	map_data = json.loads(json.dumps(mapSetting.to_json()))
	map_data["listOfPlayer"] = user_infos
	map_data = json.dumps(map_data)

	context = {'mapSetting': map_data, 'user': user, 'party_id': party_id}
	return render(request, 'game.html', context)

@login_required(login_url='/accounts/login/')
def websocket_test(request, party_id):
	return render(request, 'chatbox.html')

@login_required(login_url='/accounts/login/')
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
