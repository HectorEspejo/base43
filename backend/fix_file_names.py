import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.repositorio.models import RepositoryFile

# Fix existing files without extension in name
for file in RepositoryFile.objects.all():
    if file.file and not os.path.splitext(file.name)[1]:
        # Get the original filename from the file field
        original_name = os.path.basename(file.file.name)
        print(f"Updating {file.name} to {original_name}")
        file.name = original_name
        file.save()
        
print("Done!")