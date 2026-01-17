from datetime import date

from django.core.management.base import BaseCommand
from faker import Faker

from organizations.models import Organization, OrganizationReturnInformation
from users.models import User


class Command(BaseCommand):
    help = "Load sample fixtures for User and Organization models"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fake = Faker()

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing data before loading fixtures",
        )
        parser.add_argument(
            "--users",
            type=int,
            default=5,
            help="Number of users to create (default: 5)",
        )
        parser.add_argument(
            "--organizations",
            type=int,
            default=10,
            help="Number of organizations to create (default: 10)",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            self.stdout.write(self.style.WARNING("Clearing existing data..."))
            OrganizationReturnInformation.objects.all().delete()
            Organization.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()
            self.stdout.write(self.style.SUCCESS("Existing data cleared."))

        # Create sample users
        self.stdout.write(f"Creating {options['users']} sample users...")
        users = self._create_users(options["users"])
        self.stdout.write(self.style.SUCCESS(f"Created {len(users)} users."))

        # Create sample organizations
        self.stdout.write(f"Creating {options['organizations']} sample organizations...")
        organizations = self._create_organizations(options["organizations"])
        self.stdout.write(self.style.SUCCESS(f"Created {len(organizations)} organizations."))

        # Create sample organization returns
        self.stdout.write("Creating sample organization returns...")
        returns = self._create_organization_returns(organizations)
        self.stdout.write(self.style.SUCCESS(f"Created {len(returns)} organization returns."))

        self.stdout.write(self.style.SUCCESS("\nFixtures loaded successfully!"))

    def _create_users(self, count):
        """Create sample user accounts using Faker."""
        created_users = []

        # Always create an admin user
        admin_user, created = User.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@example.com",
                "first_name": "Admin",
                "last_name": "User",
                "is_staff": True,
                "is_superuser": True,
            },
        )
        if created:
            admin_user.set_password("password123")
            admin_user.save()
            created_users.append(admin_user)
        else:
            self.stdout.write(
                self.style.WARNING("User 'admin' already exists, skipping."),
            )

        # Create additional users with Faker
        for _ in range(count - 1):
            first_name = self.fake.first_name()
            last_name = self.fake.last_name()
            username = self.fake.user_name()
            email = self.fake.email()

            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "email": email,
                    "first_name": first_name,
                    "last_name": last_name,
                    "is_staff": False,
                    "is_superuser": False,
                },
            )
            if created:
                user.set_password("password123")
                user.save()
                created_users.append(user)
            else:
                self.stdout.write(
                    self.style.WARNING(f"User '{username}' already exists, skipping."),
                )

        return created_users

    def _create_organizations(self, count):
        """Create sample organizations using Faker."""
        created_organizations = []

        # Organization type suffixes for variety
        org_types = [
            "Foundation",
            "Alliance",
            "Initiative",
            "Society",
            "Network",
            "Coalition",
            "Association",
            "Council",
            "Institute",
            "Center",
        ]

        for _ in range(count):
            # Generate organization name
            org_name = f"{self.fake.company()} {self.fake.random_element(org_types)}"
            # Ensure unique name
            while Organization.objects.filter(name=org_name).exists():
                org_name = f"{self.fake.company()} {self.fake.random_element(org_types)}"

            # Generate website URL
            domain = self.fake.domain_name()
            website_url = f"https://{domain}"

            # Generate mission description
            mission = self.fake.text(max_nb_chars=200)
            # Make it sound more like a mission statement
            mission = mission.capitalize()
            if not mission.endswith("."):
                mission += "."

            org, created = Organization.objects.get_or_create(
                name=org_name,
                defaults={
                    "website_url": website_url,
                    "mission_description": mission,
                },
            )
            if created:
                created_organizations.append(org)
            else:
                self.stdout.write(
                    self.style.WARNING(f"Organization '{org.name}' already exists, skipping."),
                )

        return created_organizations

    def _create_organization_returns(self, organizations):
        """Create sample organization return information using Faker."""
        created_returns = []
        current_year = date.today().year

        for org in organizations:
            # Create returns for the last 3 years
            for year_offset in range(3):
                tax_year = current_year - year_offset
                tax_period_start = date(tax_year, 1, 1)
                tax_period_end = date(tax_year, 12, 31)

                # Generate random filed date between April and June of next year
                filed_on = self.fake.date_between(
                    start_date=date(tax_year + 1, 4, 1),
                    end_date=date(tax_year + 1, 6, 30),
                )

                # Generate realistic financial data using Faker
                # Base revenue varies by organization size (simulated)
                base_revenue = self.fake.random_int(min=100000, max=2000000)
                revenue_multiplier = 1.0 + (year_offset * self.fake.random.uniform(0.05, 0.15))
                total_revenue = base_revenue * revenue_multiplier

                # Expenses are typically 75-90% of revenue
                expense_ratio = self.fake.random.uniform(0.75, 0.90)
                total_expenses = total_revenue * expense_ratio

                # Assets are typically 1.5-3.5x revenue
                asset_multiplier = self.fake.random.uniform(1.5, 3.5)
                total_assets = total_revenue * asset_multiplier

                # Employee count correlates with revenue
                employee_count = self.fake.random_int(
                    min=max(5, int(total_revenue / 50000)),
                    max=min(200, int(total_revenue / 20000)),
                )

                return_data = {
                    "organization": org,
                    "filed_on": filed_on,
                    "tax_period_start_date": tax_period_start,
                    "tax_period_end_date": tax_period_end,
                    "employee_count": employee_count,
                    "total_revenue": round(total_revenue, 2),
                    "total_expenses": round(total_expenses, 2),
                    "total_assets": round(total_assets, 2),
                }

                # Check if return already exists for this organization and tax period
                existing_return = OrganizationReturnInformation.objects.filter(
                    organization=org,
                    tax_period_start_date=tax_period_start,
                    tax_period_end_date=tax_period_end,
                ).first()

                if not existing_return:
                    return_obj = OrganizationReturnInformation.objects.create(**return_data)
                    created_returns.append(return_obj)
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f"Return for {org.name} ({tax_year}) already exists, skipping.",
                        ),
                    )

        return created_returns
