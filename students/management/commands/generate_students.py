from django.core.management.base import BaseCommand, CommandError
from students.models import Student


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('students_id', nargs='+', type=int)

    def handle(self, *args, **options):
        for students_id in options['students_id']:
            Student.generate_instances(students_id)
            self.stdout.write(self.style.SUCCESS('Successfully added "%s" students' % students_id))
