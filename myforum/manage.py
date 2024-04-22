#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import webbrowser
from threading import Timer


def open_browser():
    """Open the browser to the Django server URL."""
    webbrowser.open_new("http://localhost:8000/")


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myforum.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Automatically open web browser if running the development server
    # if len(sys.argv) >= 2 and sys.argv[1] == "runserver":
    #     Timer(1.5, open_browser).start()  # Adjust the delay as necessary

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
