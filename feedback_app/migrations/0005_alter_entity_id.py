# Generated by Django 5.0.1 on 2024-02-19 21:22

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("feedback_app", "0004_alter_choice_question_textresponse"),
    ]

    operations = [
        migrations.AlterField(
            model_name="entity",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4, editable=False, primary_key=True, serialize=False
            ),
        ),
    ]
