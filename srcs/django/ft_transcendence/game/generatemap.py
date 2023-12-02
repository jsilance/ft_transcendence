from .models import MapSettings, Shape

def generatemap(party_id):
	mapSetting = MapSettings.objects.get(id=party_id)
	bordersCount = Shape.objects.filter(party_id=party_id, type="1").count()

	if bordersCount == 0:
		try:
			for i in range(int(mapSetting.nbPlayer)):
				new_shape = Shape(party_id=str(party_id), item_id=str(i), type="1", color='#ffffff', posx='0', posy='0')
				new_shape.save()
		except:
			print("****ERROR****")