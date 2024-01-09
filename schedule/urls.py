from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework import routers
from schedule import views

router = routers.DefaultRouter()
router.register(r'workers', views.WorkerView, 'workers')
router.register(r'roles', views.RoleView, 'roles')
router.register(r'parameters', views.ParameterView, 'parameters')
router.register(r'experience', views.WorkerExperienceView, 'experience')
router.register(r'constants', views.ConstantsView, 'constants')
router.register(r'executions', views.ExecutionsView, 'executions')
router.register(r'results', views.ResultsView, 'results')

urlpatterns = [
    path("", include(router.urls)),
    path('docs/', include_docs_urls(title="Dispatch Schedule")),
    path('run/', views.run_optimization, name="run")
]
