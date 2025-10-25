from rest_framework import viewsets
from .models import Skill, Project
from .serializers import SkillSerializer, ProjectSerializer

class SkillViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer