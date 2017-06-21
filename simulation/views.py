from django.http import HttpResponse
from .simulation import Scenario

# Create your views here.
def index(request):
  scen = Scenario()
  scen.run()
  return HttpResponse("Hello, world. simulation run")
