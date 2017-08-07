from django.core.management.base import BaseCommand
from simulation.models.diet_models import BreedDetails
"""
See:
http://eli.thegreenplace.net/2014/02/15/programmatically-populating-a-django-database
"""

class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'load default details for various breeds into the database'

    def _insert_default_data(self):
        # Fox et. al. 1998 Appendix Table 6. Breed maintenance requirement factors, birth weights, and peak milk production
        data = [
            BreedDetails(1,"Angus", 1, 1.2, 31.8, 6, 1.8, 2.3, 0.9, 0.9),
            BreedDetails(2,"Charolais", 1, 1.2, 36.6, 5, 3.6, 0.9, 0.2, 0),
            BreedDetails(3,"Chianina", 1, 1.2, 30.9, 4, 3.6, 0.9, 0, 1.4),
            BreedDetails(4,"Hereford", 1, 1.2, 34.1, 5, 2.3, 0.9, 0, 1.4),
            BreedDetails(5,"Limousin", 1, 1.2, 36.3, 4.5, 1.8, 2.3, 0.9, 0),
            BreedDetails(6,"Maine Anjou", 1, 1.2, 29.5, 6, 3.6, 2.3, 0.9, 1.4),
            BreedDetails(7,"Murray Grey", 1, 1.2, 29.5, 5, 3.6, 1.4, 0.9, 1.4),
            BreedDetails(8,"Simmental", 1.06, 1.2, 41, 11, 3.2, 2.3, 0.9, 1.4),
            BreedDetails(9,"South Devon", 1, 1.2, 31.8, 6, 3.6, 2.3, 0.9, 1.4),
            BreedDetails(10,"Tarentaise", 1, 1.2, 34.1, 5, 3.6, 2.3, 0.9, 1.4),
            BreedDetails(11,"Ayrshire", 1.12, 1.2, 31.8, 36, 3.6, 2.3, 0.9, 1.4),
            BreedDetails(12,"Brown Swiss", 1.12, 1.2, 38.6, 37, 3.6, 2.3, 0.9, 1.4),
            BreedDetails(13,"Friesian", 1.12, 1.2, 35, 37, 3.6, 2.3, 0.9, 1.4),
            BreedDetails(14,"Guernsey", 1.12, 1.2, 31.8, 35, 3.6, 2.3, 0.9, 1.4),
            BreedDetails(15,"Holstein", 1.12, 1, 40, 43, 3.6, 2.3, 0.9, 1.4),
            BreedDetails(16,"Jersey", 1.12, 1.2, 31.8, 34, 3.6, 2.3, 0.9, 1.4),
            BreedDetails(17,"Brahman", 0.89, 1.2, 31.8, 4, 3.6, 2.3, 0.9, 1.4)
        ]
        BreedDetails.objects.bulk_create(data)

    def handle(self, *args, **options):
        self._insert_default_data()