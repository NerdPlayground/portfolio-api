import factory
from .models import Experience
from pocket.factories import AchievementFactory

class ExperiencesFactory(AchievementFactory):
    class Meta:
        model=Experience
    
    company=factory.Faker("sentence",nb_words=5)
    title=factory.Faker("sentence",nb_words=5)
    link=factory.LazyAttribute(lambda e: "http://127.0.0.1:8000/{}".format(e.company[:-1].lower().replace(' ','-')))