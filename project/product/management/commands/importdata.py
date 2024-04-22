from django.core.management.base import BaseCommand, CommandError
from django.apps import apps
import csv


"""
Custom Django command to import data from a CSV file into a specified model.


    This command imports data from a CSV file (comma-separated values) into a model defined
    in your Django application. It takes two arguments:

    * `file_path`: The path to the CSV file containing the data to be imported.
    * `model_name`: The name of the model you want to import data into (case-sensitive).

    **Example usage:**

    ```bash
    python manage.py importdata products.csv Product
"""


class Command(BaseCommand):
    help = "Import data from CSV file"

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the CSV file')
        parser.add_argument('model_name', type=str, help='Model name')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        model_name = kwargs['model_name'].capitalize()

        # Get the model or raise an error if not found
        model = self.get_model_or_raise(model_name)

        # Open the CSV file and create objects in the model
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                model.objects.create(**row)
            self.stdout.write(self.style.SUCCESS('Data imported successfully'))

    def get_model_or_raise(self, model_name):
        """Get the specified model or raise a CommandError if not found."""
        for app_config in apps.get_app_configs():
            try:
                return apps.get_model(app_config.label, model_name)
            except LookupError:
                continue
        raise CommandError(f'Model "{model_name}" not found')
