from django.core.management.base import BaseCommand
from apps.proyectos.models import Project
from apps.proyectos.serializers import ProjectDetailSerializer
import json


class Command(BaseCommand):
    help = 'Prueba el serializer de detalles del proyecto'

    def handle(self, *args, **options):
        project = Project.objects.first()
        if not project:
            self.stdout.write(self.style.ERROR('No hay proyectos en la base de datos'))
            return
            
        self.stdout.write(self.style.SUCCESS(f'\nProbando proyecto: {project.name}'))
        self.stdout.write(f'Slug: {project.slug}')
        self.stdout.write(f'Descripción en DB: {project.description[:100]}...\n')
        
        # Serializar el proyecto
        serializer = ProjectDetailSerializer(project)
        data = serializer.data
        
        # Mostrar campos relevantes
        self.stdout.write('Campos en el serializer:')
        self.stdout.write(f'- name: {data.get("name")}')
        self.stdout.write(f'- short_description: {data.get("short_description")}')
        self.stdout.write(f'- description: {data.get("description")}')
        self.stdout.write(f'- category: {data.get("category", {}).get("name") if data.get("category") else "None"}')
        
        # Mostrar JSON completo
        self.stdout.write('\nJSON completo:')
        self.stdout.write(json.dumps(data, indent=2, ensure_ascii=False))