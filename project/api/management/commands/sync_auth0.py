# Django
from django.core.management.base import BaseCommand

# First-Party
from api.models import User

from api.tasks import (
    get_auth0_accounts,
    delete_auth0_account_orphan,
    update_auth0_account_from_user,
    create_auth0_account_from_user,
)


class Command(BaseCommand):
    help = "Command to sync database with Auth0."

    def handle(self, *args, **options):
        # Get the accounts
        self.stdout.write("Getting Auth0 accounts...")
        accounts = get_auth0_accounts()
        # Delete orphaned Auth0 accounts
        self.stdout.write("Deleting orphaned accounts...")
        users = User.objects.filter(auth0_id__isnull=False)
        user_auth0s = users.values_list('auth0_id', flat=True).distinct()
        clean_accounts = []
        i = 0
        total = len(accounts)
        for account in accounts:
            i += 1
            self.stdout.write("{0}/{1}".format(i, total), ending='\r')
            self.stdout.flush()
            if account['auth0_id'] not in user_auth0s:
                response = delete_auth0_account_orphan(account['auth0_id'])
                self.stdout.write("DELETED: {0}".format(response))
            else:
                clean_accounts.append(account)
        accounts = clean_accounts
        # Get User Accounts with existing Auth0
        users = User.objects.filter(auth0_id__isnull=False, is_active=True)
        # Update each Active User account
        self.stdout.write("Updating existing accounts...")
        i = 0
        total = users.count()
        for user in users:
            # Find user in accounts, or none
            i += 1
            self.stdout.write("{0}/{1}".format(i, total), ending='\r')
            self.stdout.flush()
            match = next((a for a in accounts if a['auth0_id'] == str(user.auth0_id)), None)
            if match:
                user_dict = {
                    'name': user.name,
                    'email': user.email,
                    'auth0_id': user.auth0_id,
                    'barberscore_id': str(user.id),
                }
                if user_dict != match:
                    user = update_auth0_account_from_user.delay(user)
                    self.stdout.write("UPDATED: {0}".format(user))
            else:
                user = create_auth0_account_from_user.delay(user)
                self.stdout.write("RESET: {0}".format(user))
        # Create new accounts for new Active users
        # Create new Auth0 Accounts
        self.stdout.write("Creating new accounts...")
        users = User.objects.filter(auth0_id__isnull=True, is_active=True)
        i = 0
        total = users.count()
        for user in users:
            i += 1
            self.stdout.write("{0}/{1}".format(i, total), ending='\r')
            self.stdout.flush()
            user = create_auth0_account_from_user.delay(user)
            self.stdout.write("CREATED: {0}".format(user))
        self.stdout.write("Complete.")
