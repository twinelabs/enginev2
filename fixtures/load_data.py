import json

from django.contrib.auth.models import User
from enginev1.apps.welcome.models import Client
from enginev1.apps.dataset.models import DataTable
from enginev1.apps.match.models import Match, MatchDataTable

from enginev1.apps.dataset.utils import import_csv_as_data_table

# ====
# CREATE USERS
# ====

# username, password, superuser, staff
users = [
    ['twineadmin', 'twineadmin', True, True],
    ['demo', 'demo', False, False],
    ['demo_nielsen', 'demo_nielsen', False, False]
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
    { 'user_id': 3, 'company_name': 'Nielsen', 'first_name': 'Chris', 'last_name': 'Louie' },
]

for client_args in clients:
    c = Client(**client_args)
    c.save()


company_name = 'Demo'

# CREATE DATA SETS
# ====
client = Client.objects.filter(company_name = company_name)[0]

csv_roles = './fixtures/roles.csv'
dt_roles_id = import_csv_as_data_table(client, 'Open Roles', csv_roles)
dt_roles = DataTable.objects.get(pk=dt_roles_id)

csv_employees = './fixtures/employees.csv'
dt_employees_id = import_csv_as_data_table(client, 'Employees', csv_employees)
dt_employees = DataTable.objects.get(pk=dt_employees_id)

# CREATE MATCH (ASSIGN)
# ====
assign_name = 'Internal Mobility'

with open('./fixtures/match_cfg_assign.json') as f:
    assign_cfg = json.load(f, strict=False)

assign_match = Match(client=client, task="assign", name=assign_name, config=assign_cfg)
assign_match.save()

MatchDataTable.objects.create(match=assign_match, data_table=dt_employees, data_table_order=1)
MatchDataTable.objects.create(match=assign_match, data_table=dt_roles, data_table_order=2)


# CREATE MATCH (GROUP)
# ====

group_name = 'Diverse Employee Teams'

with open('./fixtures/match_cfg_group.json') as f:
    group_cfg = json.load(f, strict=False)

group_match = Match(client=client, task="group",  name=group_name, config=group_cfg)
group_match.save()

MatchDataTable.objects.create(match=group_match, data_table=dt_employees, data_table_order=1)
