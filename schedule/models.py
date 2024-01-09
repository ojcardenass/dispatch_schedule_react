from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Worker(models.Model):
    name = models.CharField(max_length=200)
    weight = models.IntegerField(validators=[MinValueValidator(0)])

    def __str__(self):
        return self.name
    
    # @property
    # def get_roles_exp(self):
    #     roles_exp = {}
    #     for exp in self.workerexperience_set.all():
    #         roles_exp[exp.role.name] = exp.experience
    #     return roles_exp
    
    # Metodo para obtener la experiencia en un rol del trabajador
    # def get_roles_and_experiences(self):
    #     experiences = WorkerExperience.objects.filter(worker=self)
    #     roles_and_experiences = {exp.role.name: exp.experience for exp in experiences}
    #     return roles_and_experiences
    
class Role(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class WorkerExperience(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    experience = models.IntegerField(validators=[MinValueValidator(0)])

    def __str__(self):
        return self.role
    
class Parameters(models.Model):
    id = models.AutoField(primary_key=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    parameter = models.TextField()
    value = models.IntegerField(validators=[MinValueValidator(0)])

    def __str__(self):
        return self.name

    
class Constants(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    value = models.IntegerField(validators=[MinValueValidator(0)])

    def __str__(self):
        return self.name

## TODO Crear vista en la que se guarde la date now, con watchdogs.
class Executions(models.Model):
    id = models.AutoField(primary_key=True)
    startDate = models.DateField()
    endDate = models.DateField()

    def __str__(self):
        return self.id


class Schedule_Results(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, default=0)
    daydate = models.DateField()
    rol = models.CharField(max_length=100, default='')
    value = models.IntegerField(validators=[MinValueValidator(0)])
    class Meta:
        unique_together = (('worker','daydate','rol'))

    def __str__(self):
        return self.worker