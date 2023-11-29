from .models import MapSettings, Shape

def generatemap(id):
	try:
		for i in MapSettings[id].nbPlayer:
			new_shape = Shape(type='border', color='#ffffff', posx=id, posy='0')
			new_shape.save()
	except:
		print("****ERROR****")