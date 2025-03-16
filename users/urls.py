from typing import Any
from django.urls import path
from users.views import (
    dashboard, open_table, table_view, add_item, login_view,
    increase_quantity, decrease_quantity, payment_view, check_history, check_detail, reopen_check
)

urlpatterns: list[Any] = [
    path('login/', login_view, name='login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('open_table/', open_table, name='open_table'),
    path('table/<int:table_id>/', table_view, name='table_view'),
    path('add_item/<int:table_id>/<int:item_id>/', add_item, name='add_item'),
    path('increase_item/<int:table_id>/<int:item_id>/', increase_quantity, name='increase_item'),
    path('decrease_item/<int:table_id>/<int:item_id>/', decrease_quantity, name='decrease_item'),
    path('payment/<int:table_id>/', payment_view, name='payment'),
    path('check_history/', check_history, name='check_history'),
    path('check_history/<int:check_id>/', check_detail, name='check_detail'),
    path('reopen_check/<int:check_id>/', reopen_check, name='reopen_check'),
]
