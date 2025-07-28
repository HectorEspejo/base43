from django.core.management.base import BaseCommand
from apps.proyectos.models import ProjectCategory


class Command(BaseCommand):
    help = 'Crea categorías de proyecto de ejemplo'

    def handle(self, *args, **options):
        categories = [
            {
                'name': 'Cohousing',
                'description': 'Proyectos de vivienda colaborativa y cohousing',
                'icon': 'home-group',
                'order': 1
            },
            {
                'name': 'Cooperativas',
                'description': 'Cooperativas de vivienda en cesión de uso',
                'icon': 'building-cooperative',
                'order': 2
            },
            {
                'name': 'Centros de menores',
                'description': 'Centros de protección y acogida de menores',
                'icon': 'child-care',
                'order': 3
            },
            {
                'name': 'Vivienda social',
                'description': 'Proyectos de vivienda social y asequible',
                'icon': 'home-heart',
                'order': 4
            }
        ]

        for cat_data in categories:
            category, created = ProjectCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Categoría creada: {category.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Categoría ya existe: {category.name}')
                )