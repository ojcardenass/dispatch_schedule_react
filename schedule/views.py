from django.shortcuts import render
from rest_framework import viewsets
from .serializer import *
from .models import *
from modelopt import model, params
from django.http import JsonResponse
import json
# Create your views here.
class WorkerView(viewsets.ModelViewSet):
    serializer_class = WorkerSerializer
    queryset = Worker.objects.all()

class RoleView(viewsets.ModelViewSet):
    serializer_class = RoleSerializer
    queryset = Role.objects.all()

class ParameterView(viewsets.ModelViewSet):
    serializer_class = ParametersSerializer
    queryset = Parameters.objects.all()

class WorkerExperienceView(viewsets.ModelViewSet):
    serializer_class = WorkerExperienceSerializer
    queryset = WorkerExperience.objects.all()

class ConstantsView(viewsets.ModelViewSet):
    serializer_class = ConstantsSerializer
    queryset = Constants.objects.all()

class ExecutionsView(viewsets.ModelViewSet):
    serializer_class = ExecutionsSerializer
    queryset = Executions.objects.all()    

class ResultsView(viewsets.ModelViewSet):
    serializer_class = ScheduleResultsSerializer
    queryset = Schedule_Results.objects.all()

def run_optimization(request):

    if request.method == 'POST':
        raw_data = request.body
        body_unicode = raw_data.decode('utf-8')
        body = json.loads(body_unicode)
        print(body)

        # data2DBStatus, solver_messages, dfdic = model.executemodel(model_params, solver_opt)
        solver_messages = "hi"
    # Return the result as JSON
        return JsonResponse({'result': solver_messages})    