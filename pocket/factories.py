import factory
from datetime import date

class AchievementFactory(factory.django.DjangoModelFactory):
    class Meta:
        abstract=True
    
    ongoing=False
    link=factory.LazyAttribute(lambda e: "http://127.0.0.1:8000/{}".format(e.name[:-1].lower().replace(' ','-')))
    start_date=factory.Faker("date_between_dates",date_start=date(2020,1,1),date_end=date(2024,1,1))
    end_date=factory.Faker("date_between_dates",date_start=factory.SelfAttribute('..start_date'),date_end=date(2024,1,1))
    description=factory.Faker("paragraph",nb_sentences=5)
    objectives=factory.Faker("sentences",nb=5)
    tools=factory.List(["Python","Django","Django REST Framework"])