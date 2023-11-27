from django.shortcuts import render
from .models import Shape
from django.contrib.auth.decorators import login_required
import json

def game(request):
	shapes = [{"type":int(x.type), "color":x.color} for x in Shape.objects.all()]
	shape_json = json.dumps(shapes)
	context = {'shapes': shape_json}
	return render(request, 'game.html', context)

@login_required
def websocket_test(request):
    return render(request, 'chatbox.html')

