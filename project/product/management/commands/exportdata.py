import csv
from django.core.management.base import BaseCommand, CommandError
from django.apps import apps
import datetime
import os

"""
A custom Django management command to export data from a specified model to a CSV file.

This command exports all data from the given model to a CSV file. It takes two arguments:

* `model_name`: The name of the model you want to export data from (case-sensitive).
* `--file_path` (optional): The path to the output CSV file. 
    - If not provided, a default filename will be generated in the current directory.

**Example usage:**

using docker: 
docker-compose run --rm project sh -c "python manage.py exportdata ProductType --file_path=/vol/web/"
```bash
python manage.py exportdata ProductType --file_path=/vol/web/exports/
"""


class Command(BaseCommand):
    help = 'Export data from the database to a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('model_name', type=str, help='Model name')
        parser.add_argument('--file_path', type=str,
                            help='Path to the output CSV file (default: Exported_data.csv)')

    def handle(self, *args, **kwargs):
        # file_path = kwargs['file_path']
        model_name = kwargs['model_name']
        file_path = kwargs['file_path']

        # Get the model or raise an error if not found
        models = self.get_model_or_raise(model_name)

        model = models.objects.all()

        timestamp = datetime.datetime.now().strftime('%d-%m-%Y-%H-%M-%S')
        filename = f'Exported_{model_name.lower()}_data_{timestamp}.csv'

        if not os.path.exists(file_path):
            raise CommandError(f'Invalid path: {file_path}')

        if file_path:
            file_path = os.path.join(file_path, filename)
        else:
            file_path = filename

        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)

            # Write column headers based on model fields
            writer.writerow(
                [field.name for field in model.model._meta.fields])

            # Write data rows
            for obj in model:
                writer.writerow([getattr(obj, field.name)
                                for field in model.model._meta.fields])

        self.stdout.write(self.style.SUCCESS('Data exported successfully!'))

    def get_model_or_raise(self, model_name):
        """Get the specified model or raise a CommandError if not found."""
        for app_config in apps.get_app_configs():
            try:
                return apps.get_model(app_config.label, model_name)
            except LookupError:
                continue
        raise CommandError(f'Model "{model_name}" not found')
