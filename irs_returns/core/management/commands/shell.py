from django.core.management.commands import shell


class Command(shell.Command):
    """Overrides the default shell command to add more custom imports."""

    def get_auto_imports(self):
        return super().get_auto_imports() + [
            "organizations.parsers.handler.XMLParser",
        ]
