from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("cms", "0042_merge_20250805_1544"),
        (
            "global_neighbor",
            "0016_document_author_document_category_document_source_and_more",
        ),
    ]

    operations = [
        migrations.RunPython(
            lambda apps, schema_editor: None,
            reverse_code=lambda apps, schema_editor: None,
        ),
    ]
