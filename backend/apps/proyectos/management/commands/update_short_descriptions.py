from django.core.management.base import BaseCommand
from apps.proyectos.models import Project


class Command(BaseCommand):
    help = 'Actualiza las descripciones cortas vacías con un extracto de la descripción completa'

    def handle(self, *args, **options):
        projects = Project.objects.filter(short_description='')
        updated = 0
        
        for project in projects:
            if project.description:
                if len(project.description) > 297:
                    project.short_description = project.description[:297] + '...'
                else:
                    project.short_description = project.description
                project.save()
                updated += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Actualizado: {project.name}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'\nTotal de proyectos actualizados: {updated}')
        )