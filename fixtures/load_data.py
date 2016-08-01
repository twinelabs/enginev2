from django.contrib.auth.models import User
from enginev1.apps.welcome.models import Client
from enginev1.apps.dataset.models import Alpha
from enginev1.apps.dataset.models import Beta

from enginev1.apps.dataset.utils import *

# ====
# CREATE USERS
# ====

# users: username, password, superuser, staff
users = [
    ['twineadmin', 'twineadmin', True, True],
    ['nike', 'nikepassword', False, False],
    ['ibm', 'ibmpassword', False, False],
    ['wharton', 'whartonpassword', False, False],
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
    { 'user_id': 1, 'name': 'Twine Team', 'display_name': 'Twine Team Internal', 'domain_prefix': 'twineteam', 'alpha_label': 'Test A', 'beta_label': 'Test B' },
    { 'user_id': 2, 'name': 'Nike', 'display_name': 'Nike People Analytics', 'domain_prefix': 'nike', 'alpha_label': 'Employees' },
    { 'user_id': 3, 'name': 'IBM', 'display_name': 'IBM Sales NYC', 'domain_prefix': 'ibm', 'alpha_label': 'Employees', 'beta_label': 'Internal Roles'},
    { 'user_id': 4, 'name': 'Wharton', 'display_name': 'Wharton Admissions', 'domain_prefix': 'wharton', 'alpha_label': 'Admits', 'beta_label': 'Alumni'},
]

for client_args in clients:
    c = Client(**client_args)
    c.save()

# ====
# CREATE ALPHAS
# ====

alphas_ibm= [
    { 'client_id': 3, 'data': {'name': 'Edward Smith', 'gender': 'M', 'age': '67', 'department': 'HR', 'favorite_music': 'Rap'} },
    { 'client_id': 3, 'data': {'name': 'Janet Jacobs', 'gender': 'F', 'age': '34', 'department': 'Talent', 'favorite_music': 'R&B'} },
    { 'client_id': 3, 'data': {'name': 'Eric Samuels', 'gender': 'M', 'age': '17', 'department': 'Recruiting', 'favorite_music': 'Classical'} },
]

alphas_wharton = [
    { 'client_id': 4, 'data': {'name': 'Edward Smith', 'gender': 'M', 'location': 'NYC', 'GPA': '4.0', 'major': 'Entrepreneurship'} },
    { 'client_id': 4, 'data': {'name': 'Janet Jacobs', 'gender': 'F', 'location': 'SF', 'GPA': '3.5', 'major': 'Marketing'} },
    { 'client_id': 4, 'data': {'name': 'Eric Samuels', 'gender': 'M', 'location': 'Bangkok', 'GPA': '2.8', 'major': 'Real Estate'} },
]

alphas = alphas_ibm + alphas_wharton

for alpha_args in alphas:
    a = Alpha(**alpha_args)
    a.save()

# ====
# CREATE BETAS
# ====

betas_wharton = [
    { 'client_id': 4, 'data': {'name': 'Vincent Smith', 'gender': 'M', 'location': 'London', 'industry': 'Consulting', 'grad_year': '1996'} },
    { 'client_id': 4, 'data': {'name': 'Mary Edwards', 'gender': 'F', 'location': 'Tokyo', 'industry': 'Real Estate', 'grad_year': '2003'} },
    { 'client_id': 4, 'data': {'name': 'Bill Cummings', 'gender': 'M', 'location': 'LA', 'industry': 'Social Impact', 'grad_year': '2005'} },
]

betas = betas_wharton

for beta_args in betas:
    b = Beta(**beta_args)
    b.save()

# ===
# FULL SET
# ===

csv_file = './fixtures/demo_data.csv'
client = Client.objects.filter(name = 'Nike')[0]
import_csv_as_dataset(client, 'alpha', csv_file)
