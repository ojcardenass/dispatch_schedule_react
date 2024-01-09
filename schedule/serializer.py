from rest_framework import serializers
from .models import Worker, Role, Parameters, WorkerExperience, Constants, Executions, Schedule_Results


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class WorkerExperienceSerializer(serializers.ModelSerializer):
    worker_name = serializers.StringRelatedField(source='worker.name')
    role_name = serializers.StringRelatedField(source='role.name')
    # roles_exp = serializers.SerializerMethodField()
    class Meta:
        model = WorkerExperience
        fields = ('id','worker','role','worker_name','role_name','experience')

class WorkerExperienceListSerializer(serializers.ModelSerializer):
    role_name = serializers.StringRelatedField(source='role.name')
    class Meta:
        model = WorkerExperience
        fields = ('role_name','experience')

class WorkerSerializer(serializers.ModelSerializer):
    roles_exp = serializers.SerializerMethodField()
    class Meta:
        model = Worker
        fields = ('id','name', 'weight', 'roles_exp')
    
    def get_roles_exp(self, obj):
        roles_exp = {}
        for exp in obj.workerexperience_set.all():
            roles_exp[exp.role.name +"_"+ str(exp.id)] = exp.experience
        return roles_exp

class ParametersSerializer(serializers.ModelSerializer):
    role_name = serializers.StringRelatedField(source='role.name')
    class Meta:
        model = Parameters
        fields = '__all__'

class ConstantsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Constants
        fields = '__all__'

class ExecutionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Executions
        fields = '__all__'

class ScheduleResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule_Results
        fields = '__all__'