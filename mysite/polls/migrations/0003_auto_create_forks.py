from django.db import migrations

def create_forks(apps, schema_editor):
    Fork = apps.get_model('polls', 'Fork')
    # Create 5 forks
    for _ in range(5):
        Fork.objects.create()

class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_fork_alter_philosopher_state_philosopher_left_fork_and_more'),
    ]

    operations = [
        migrations.RunPython(create_forks),
    ]
