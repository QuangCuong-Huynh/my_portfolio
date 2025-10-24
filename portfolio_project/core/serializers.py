from rest_framework import serializers
from .models import Skill, Project, Experience

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'