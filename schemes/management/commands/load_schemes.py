import csv
import numpy as np
import pandas as pd
from django.core.management import BaseCommand
from ...models import Schemes
from django.utils.timezone import make_aware
from datetime import datetime

class Command(BaseCommand):
    help = 'Load a schemes from csv file into the database'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        # Remove any existing data
        print("Clean old movie data")
        Schemes.objects.all().delete()
        path = kwargs['path']
        # Read the movie csv file as a dataframe
        movie_df = pd.read_csv(path)
        movie_df.fillna("",inplace = True)
        # Iterate each row in the dataframe
        for index, row in movie_df.iterrows():
            print(row["openDate"],row["closeDate"])
            Schemes.objects.create(
            # Populate Movie object for each row
            # scheme = Schemes(
                title = row["title"],
                            name = row["name"],
                            openDate = make_aware(datetime.strptime(row["openDate"],"%Y-%m-%d")) if row["openDate"]!="" else None,
                            closeDate = make_aware(datetime.strptime(row["closeDate"],"%Y-%m-%d")) if row["closeDate"]!="" else None,
                            nodalMinistry = row["nodalMinistry"],
                            nodalDepartment = row["nodalDepartment"],
                            brief = row["brief"],
                            details = row["details"],
                            eligibility = row["eligibility"],
                            tags = row['tags'],
                            category = row['category'],
                            subcategory = row['subcategory'],
                            references = row['references'],
                            slug = row['title'])
            # Save movie object
            # scheme.save()
            try:
                new_scheme = Schemes.objects.get(slug=row['slug'])
                tags = row['tags'].split(", ")
                cat = row['category'].split(", ")
                subcat = row['subcategory'].split(", ")
                for genre in tags:
                    new_scheme.tags.add(genre)
                
                for genre in cat:
                    new_scheme.cat.add(genre)

                for genre in subcat:
                    new_scheme.subcat.add(genre)
            except:
                pass
            print(f"scheme no: {index} saved...")

# python manage.py load_movies --path movies.csv