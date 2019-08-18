##!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Test.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django ."
            )
        raise
    execute_from_command_line([os.path.abspath(__file__),"runserver","0.0.0.0:1235","--noreload"])