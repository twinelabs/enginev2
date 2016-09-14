import json

from django.contrib.auth.models import User
from enginev1.apps.welcome.models import Client
from enginev1.apps.dataset.models import DataTable
from enginev1.apps.match.models import Match

from enginev1.apps.dataset.utils import import_csv_as_data_table

# ====
# CREATE USERS
# ====

# username, password, superuser, staff
users = [
    ['twineadmin', 'twineadmin', True, True],
    ['demo', 'demo', False, False]
]

for username, pw, superuser, staff in users:
    u = User(username=username)
    u.set_password(pw)
    u.is_superuser = superuser
    u.is_staff = staff
    u.save()


# ====
# CREATE CLIENTS
# ====

clients = [
    { 'user_id': 1, 'company_name': 'Twine Admin', 'first_name': 'Twine', 'last_name': 'Admin' },
    { 'user_id': 2, 'company_name': 'Demo', 'first_name': 'User', 'last_name': 'User' },
]

for client_args in clients:
    c = Client(**client_args)
    c.save()


# ====
# CREATE DATA SETS
# ====

client = Client.objects.filter(company_name = 'Demo')[0]

csv_employees = './fixtures/employees.csv'
dt_employees_id = import_csv_as_data_table(client, 'Employees', csv_employees)
dt_employees = DataTable.objects.get(pk=dt_employees_id)

csv_roles = './fixtures/roles.csv'
dt_roles_id = import_csv_as_data_table(client, 'Roles', csv_roles)
dt_roles = DataTable.objects.get(pk=dt_roles_id)


# ====
# CREATE MATCH (GROUP)
# ====

group_name = 'Diverse Employee Teams'
group_cfg = json.loads('./fixtures/match_cfg_group.json')
group_match = Match(client=client, name=group_name, config=group_cfg)
group_match.save()

group_match.data_tables.add(dt_employees)
group_match.save()


# ====
# CREATE MATCH (ASSIGN)
# ====

assign_name = 'Internal Mobility'
assign_cfg = json.loads('./fixtures/match_cfg_assign.json')
assign_match = Match(client=client, name=assign_name, config=assign_cfg)
assign_match.save()

assign_match.data_tables.add(dt_employees)
assign_match.data_tables.add(dt_roles)
assign_match.save()
