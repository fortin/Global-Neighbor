import uuid

from django.db import migrations, models


def generate_tokens(apps, schema_editor):
    """Assign a unique verification token to each existing user."""
    User = apps.get_model("global_neighbor", "User")
    for user in User.objects.filter(verification_token__isnull=True):
        user.verification_token = uuid.uuid4()
        user.save()


class Migration(migrations.Migration):
    dependencies = [
        (
            "global_neighbor",
            "0002_user_is_verified_user_otp_code_and_more",
        ),  # Update with the latest migration name
    ]

    operations = [
        migrations.RunPython(
            generate_tokens
        ),  # Populate existing users with unique tokens
        migrations.AlterField(
            model_name="user",
            name="verification_token",
            field=models.UUIDField(
                default=uuid.uuid4, unique=True
            ),  # Remove null=True, blank=True
        ),
    ]
