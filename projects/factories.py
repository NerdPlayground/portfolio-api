import factory
from .models import Project
from pocket.factories import AchievementFactory

class ProjectsFactory(AchievementFactory):
    class Meta:
        model=Project
    
    name=factory.Faker("sentence",nb_words=5)