from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import F
from .models import User, Table, MenuItem, OrderItem, CheckCounter, CheckHistory

def login_view(request):
    if request.method == "POST":
        number_id = request.POST.get("number_id")
        try:
            user = User.objects.get(number_id=number_id)
            login(request, user)
            return redirect("dashboard")
        except User.DoesNotExist:
            return render(request, "users/login.html", {"error": "Invalid Number ID"})

    return render(request, "users/login.html")


@login_required
def dashboard(request):
    tables = Table.objects.filter(is_open=True)
    total_checks = CheckHistory.objects.count()  # ✅ Count total checks globally
    return render(request, "users/dashboard.html", {
        "tables": tables,
        "total_checks": total_checks
    })


@login_required
def open_table(request):
    if request.method == "POST":
        table_number = request.POST.get("table_number")
        table = Table.objects.filter(number=table_number).first()
        next_check = CheckCounter.next_check_number()  # Get next check number

        if table:
            table.is_open = True
            table.opened_by = request.user
            table.check_number = next_check
            table.save()
            table.orderitem_set.all().delete()  # Clear old items
        else:
            table = Table.objects.create(
                number=table_number,
                is_open=True,
                opened_by=request.user,
                check_number=next_check
            )

        # Log to Check History
        CheckHistory.objects.create(
            check_number=next_check,
            table_number=table_number,
            opened_by=request.user
        )

        return redirect('table_view', table_id=table.id)
    return render(request, "users/open_table.html")


@login_required
def table_view(request, table_id):
    table = get_object_or_404(Table, id=table_id)
    menu_items = MenuItem.objects.all()
    order_items = OrderItem.objects.filter(table=table)
    total = table.total_amount()
    return render(request, "users/table_view.html", {
        "table": table,
        "menu_items": menu_items,
        "order_items": order_items,
        "total": total
    })


@login_required
def add_item(request, table_id, item_id):
    table = get_object_or_404(Table, id=table_id)
    menu_item = get_object_or_404(MenuItem, id=item_id)
    OrderItem.objects.create(table=table, menu_item=menu_item, quantity=1)
    return redirect('table_view', table_id=table.id)


@login_required
def increase_quantity(request, table_id, item_id):
    item = get_object_or_404(OrderItem, id=item_id, table_id=table_id)
    item.quantity = F('quantity') + 1
    item.save()
    return redirect('table_view', table_id=table_id)


@login_required
def decrease_quantity(request, table_id, item_id):
    item = get_object_or_404(OrderItem, id=item_id, table_id=table_id)
    if item.quantity > 1:
        item.quantity = F('quantity') - 1
        item.save()
    else:
        item.delete()  # Remove item if quantity drops to 0
    return redirect('table_view', table_id=table_id)


@login_required
def payment_view(request, table_id):
    table = get_object_or_404(Table, id=table_id)
    if request.method == "POST":
        payment_method = request.POST.get("payment_method")
        table.is_open = False  # Close table
        table.save()
        return redirect('dashboard')
    total = table.total_amount()
    return render(request, "users/payment.html", {"table": table, "total": total})

@login_required
def check_history(request):
    history = CheckHistory.objects.all().order_by('-id')  # Show recent first
    return render(request, "users/check_history.html", {"history": history})


@login_required
def check_detail(request, check_id):
    check = get_object_or_404(CheckHistory, id=check_id)

    # You might want to fetch past order items if needed
    # For example, if CheckHistory has no items stored, you can relate by table/check number if possible

    return render(request, "users/check_detail.html", {"check": check})

@login_required
def reopen_check(request, check_id):
    check = get_object_or_404(CheckHistory, id=check_id)

    # Create new table
    table = Table.objects.create(
        number=check.table_number,
        is_open=True,
        opened_by=request.user,
        check_number=CheckCounter.next_check_number()
    )

    # Restore items
    if check.items_data:
        for item in check.items_data:
            menu_item = MenuItem.objects.get(id=item['menu_item_id'])
            OrderItem.objects.create(
                table=table,
                menu_item=menu_item,
                quantity=item['quantity']
            )

    return redirect('table_view', table_id=table.id)

