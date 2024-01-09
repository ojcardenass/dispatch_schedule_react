from django.contrib import admin
from .models import Worker, Role, WorkerExperience, Schedule_Results, Executions

# Register your models here.
admin.site.register(Worker)
admin.site.register(Schedule_Results)
admin.site.register(Role)
admin.site.register(WorkerExperience)
admin.site.register(Executions)