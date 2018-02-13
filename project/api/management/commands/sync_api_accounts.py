# Django
from django.core.management.base import BaseCommand

# First-Party
from api.models import User
from api.tasks import get_accounts
from api.tasks import update_or_create_account_from_user
from api.tasks import delete_account


class Command(BaseCommand):
    help = "Command to sync database with Auth0."

    def handle(self, *args, **options):
        # Get the accounts
        self.stdout.write("Getting Auth0 accounts...")
        accounts = get_accounts()
        # Delete orphaned Auth0 accounts
        self.stdout.write("Deleting orphaned accounts...")
        users = User.objects.filter(account_id__isnull=False)
        user_accounts = users.values_list('account_id', flat=True).distinct()
        clean_accounts = []
        i = 0
        total = len(accounts)
        for account in accounts:
            i += 1
            self.stdout.write("{0}/{1}".format(i, total), ending='\r')
            self.stdout.flush()
            if account['account_id'] not in user_accounts:
                response = delete_account(account['account_id'])
                self.stdout.write("DELETED: {0}".format(response))
            else:
                clean_accounts.append(account)
        accounts = clean_accounts
        # Get active User Accounts with existing Auth0
        users = User.objects.filter(
            status=User.STATUS.active,
        )
        # Update each Active User account
        self.stdout.write("Updating existing accounts...")
        i = 0
        total = users.count()
        for user in users:
            i += 1
            self.stdout.write("{0}/{1}".format(i, total), ending='\r')
            self.stdout.flush()
            # Find user in accounts, or none
            match = next((a for a in accounts if a['account_id'] == str(user.account_id)), None)
            if match:
                # If user is in accounts
                # Check to see if the data matches
                user_dict = {
                    'name': user.name,
                    'email': user.email,
                    'account_id': user.account_id,
                    'barberscore_id': str(user.id),
                }
                if user_dict != match:
                    # If it doesn't, update it
                    update_or_create_account_from_user.delay(user)
                    self.stdout.write("UPDATED: {0}".format(user))
                # Otherwise skip
            else:
                # If user isn't in accounts, create.
                update_or_create_account_from_user.delay(user)
                self.stdout.write("CREATED: {0}".format(user))
        self.stdout.write("Complete.")