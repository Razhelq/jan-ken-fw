# Generated by Django 4.0.4 on 2022-07-22 05:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('rounds', models.SmallIntegerField(default=1, help_text='Number of rounds')),
                ('status', models.SmallIntegerField(choices=[(1, 'waiting for player'), (2, 'in progress'), (3, 'finished')], default=1, help_text='Status that represents a game state.')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GameRound',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('round_number', models.SmallIntegerField(default=1)),
                ('game', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='game_round', to='game.game')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('games_won', models.IntegerField(default=0, help_text='Total number of won games.')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Move',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('move', models.SmallIntegerField(choices=[(1, 'rock'), (2, 'paper'), (3, 'scissors'), (4, 'lizard'), (5, 'spock')], null=True)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.game')),
                ('game_round', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='game.gameround')),
                ('player', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='game.player')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='gameround',
            name='winner',
            field=models.ForeignKey(help_text='A winner of the round.', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='winner', to='game.player'),
        ),
        migrations.AddField(
            model_name='game',
            name='next_move',
            field=models.ForeignKey(help_text='A player who should do next move.', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='next_move', to='game.player'),
        ),
        migrations.AddField(
            model_name='game',
            name='player',
            field=models.ManyToManyField(blank=True, to='game.player'),
        ),
    ]
