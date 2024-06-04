import factory
from .models import Project
from pocket.factories import AchievementFactory

class ProjectsFactory(AchievementFactory):
    class Meta:
        model=Project
    
    name=factory.Faker("sentence",nb_words=5)
    link=factory.LazyAttribute(lambda e: "http://127.0.0.1:8000/{}".format(e.name[:-1].lower().replace(' ','-')))