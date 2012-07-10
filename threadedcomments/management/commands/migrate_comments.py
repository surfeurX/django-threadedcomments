from django.core.management.base import NoArgsCommand
from django.db import transaction, connection
from django.conf import settings

PATH_DIGITS = getattr(settings, 'COMMENT_PATH_DIGITS', 10)

SQL = """
INSERT INTO threadedcomments_comment 
SELECT id as comment_ptr_id,
       '' as title,
       null as parent_id, 
       null as last_child_id, 
       LPAD(id, %s,'0') AS tree_path
FROM django_comments;
""" % PATH_DIGITS

class Command(NoArgsCommand):
    help = "Migrates from django.contrib.comments to django-threadedcomments"

    def handle(self, *args, **options):
        transaction.commit_unless_managed()
        transaction.enter_transaction_management()
        transaction.managed(True)

        cursor = connection.cursor()

        cursor.execute(SQL)

        transaction.commit()
        transaction.leave_transaction_management()
