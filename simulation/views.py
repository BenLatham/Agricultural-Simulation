from django.http import HttpResponse
from .simulation import Scenario
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

scenarios = {}
# Create your views here.
@login_required
def index(request):
  scen = Scenario(request.user)
  simulation =scen.scenario.id
  scenarios[simulation]=Scenario(request.user)
  return HttpResponse(render(request, 'simulation/response.html', {'id':simulation}))

@login_required
def run_process(request, simulation):
    simulation = int(simulation)
    try:
        scenarios[simulation].run()
    except:
        return HttpResponse("Simulation failed to run correctly")
    finally: del scenarios[simulation]
    # TODO: make a template for the message rather than just as a string, and load with javascript rather than an iframe
    return HttpResponse('Simulation complete: <a href="report/'+str(simulation)+'" target="_parent">See the results here</a>')



@login_required
def report(request, simulation):
    return HttpResponse('sorry, this feature has not yet been implemented')