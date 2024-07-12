from django.shortcuts import render, redirect
from admin_datta.forms import RegistrationForm, LoginForm, UserPasswordChangeForm, UserPasswordResetForm, \
    UserSetPasswordForm
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetConfirmView, PasswordResetView
from django.views.generic import CreateView
from django.contrib.auth import logout

from django.contrib.auth.decorators import login_required

from .models import *


def index(request):
    context = {
        'segment': 'index',
        # 'products' : Product.objects.all()
    }
    return render(request, "pages/index.html", context)


def tables(request):
    context = {
        'segment': 'tables'
    }
    return render(request, "pages/dynamic-tables.html", context)


def instances(request):
    instances_data = [
        {
            "server_name": "Server 1",
            "location": "New York, USA",
            "ip_address": "192.168.1.1",
            "status": "Active"
        },
        {
            "server_name": "Server 2",
            "location": "London, UK",
            "ip_address": "192.168.1.2",
            "status": "Inactive"
        },
        {
            "server_name": "Server 3",
            "location": "Tokyo, Japan",
            "ip_address": "192.168.1.3",
            "status": "Active"
        },
        {
            "server_name": "Server 4",
            "location": "Sydney, Australia",
            "ip_address": "192.168.1.4",
            "status": "Inactive"
        },
        {
            "server_name": "Server 5",
            "location": "Berlin, Germany",
            "ip_address": "192.168.1.5",
            "status": "Active"
        }
    ]

    context = {
        'segment': 'instances',
        'instances': instances_data
    }
    return render(request, "pages/instances.html", context)


def home(request):
    context = {
        'segment': 'home'
    }
    return render(request, "pages/home.html", context)


def create_instances(request):
    context = {
        'segment': 'create_instances'
    }
    return render(request, "pages/create-instances.html", context)


def network(request):
    sample_data = [
        {
            "ip_address": "192.168.1.1",
            "instance_name": "Instance 1",
            "line_type": "Fiber",
            "location": "New York, USA"
        },
        {
            "ip_address": "192.168.1.2",
            "instance_name": "Instance 2",
            "line_type": "DSL",
            "location": "London, UK"
        },
        {
            "ip_address": "192.168.1.3",
            "instance_name": "Instance 3",
            "line_type": "Fiber",
            "location": "Tokyo, Japan"
        },
        {
            "ip_address": "192.168.1.4",
            "instance_name": "Instance 4",
            "line_type": "Cable",
            "location": "Sydney, Australia"
        },
        {
            "ip_address": "192.168.1.5",
            "instance_name": "Instance 5",
            "line_type": "Fiber",
            "location": "Berlin, Germany"
        }
    ]
    context = {
        'segment': 'network',
        'networks': sample_data
    }
    return render(request, "pages/network.html", context)


def block_storage(request):
    storage_data = [
        {
            "block_storage": "Storage 1",
            "size": "500 GB",
            "instance": "Instance 1",
            "location": "New York, USA",
            "datetime": "2024-07-10 14:30"
        },
        {
            "block_storage": "Storage 2",
            "size": "1 TB",
            "instance": "Instance 2",
            "location": "London, UK",
            "datetime": "2024-07-11 09:20"
        },
        {
            "block_storage": "Storage 3",
            "size": "250 GB",
            "instance": "Instance 3",
            "location": "Tokyo, Japan",
            "datetime": "2024-07-12 17:45"
        },
        {
            "block_storage": "Storage 4",
            "size": "750 GB",
            "instance": "Instance 4",
            "location": "Sydney, Australia",
            "datetime": "2024-07-13 12:15"
        },
        {
            "block_storage": "Storage 5",
            "size": "2 TB",
            "instance": "Instance 5",
            "location": "Berlin, Germany",
            "datetime": "2024-07-14 08:30"
        }
    ]

    context = {
        'segment': 'block_storage',
        'storages': storage_data
    }
    return render(request, "pages/block_storage.html", context)


def snapshot(request):
    snapshots_data = [
        {
            "snapshot_name": "Snapshot 1",
            "type": "Full",
            "size": "50 GB",
            "location": "New York, USA",
            "datetime": "2024-07-10 14:30"
        },
        {
            "snapshot_name": "Snapshot 2",
            "type": "Incremental",
            "size": "25 GB",
            "location": "London, UK",
            "datetime": "2024-07-11 09:20"
        },
        {
            "snapshot_name": "Snapshot 3",
            "type": "Full",
            "size": "75 GB",
            "location": "Tokyo, Japan",
            "datetime": "2024-07-12 17:45"
        },
        {
            "snapshot_name": "Snapshot 4",
            "type": "Incremental",
            "size": "20 GB",
            "location": "Sydney, Australia",
            "datetime": "2024-07-13 12:15"
        },
        {
            "snapshot_name": "Snapshot 5",
            "type": "Full",
            "size": "100 GB",
            "location": "Berlin, Germany",
            "datetime": "2024-07-14 08:30"
        }
    ]
    context = {
        'segment': 'snapshot',
        'snapshots': snapshots_data
    }
    return render(request, "pages/snapshot.html", context)


def firewall(request):
    firewall_groups_data = [
        {
            "firewall_group": "Group 1",
            "location": "New York, USA",
            "rules": "5 Rules",
            "instances": "Instance 1, Instance 2",
            "description": "This is a description for Group 1.",
            "date_created": "2024-07-10"
        },
        {
            "firewall_group": "Group 2",
            "location": "London, UK",
            "rules": "3 Rules",
            "instances": "Instance 3",
            "description": "This is a description for Group 2.",
            "date_created": "2024-07-11"
        },
        {
            "firewall_group": "Group 3",
            "location": "Tokyo, Japan",
            "rules": "8 Rules",
            "instances": "Instance 4, Instance 5",
            "description": "This is a description for Group 3.",
            "date_created": "2024-07-12"
        },
        {
            "firewall_group": "Group 4",
            "location": "Sydney, Australia",
            "rules": "2 Rules",
            "instances": "Instance 6",
            "description": "This is a description for Group 4.",
            "date_created": "2024-07-13"
        },
        {
            "firewall_group": "Group 5",
            "location": "Berlin, Germany",
            "rules": "4 Rules",
            "instances": "Instance 7, Instance 8",
            "description": "This is a description for Group 5.",
            "date_created": "2024-07-14"
        }
    ]

    context = {
        'segment': 'firewall',
        'firewall_groups': firewall_groups_data
    }
    return render(request, "pages/firewall.html", context)


def image(request):
    images_data = [
        {
            "image": "Image 1",
            "location": "New York, USA",
            "os": "Ubuntu 20.04",
            "description": "This is a description for Image 1.",
            "datetime": "2024-07-10 14:30"
        },
        {
            "image": "Image 2",
            "location": "London, UK",
            "os": "CentOS 7",
            "description": "This is a description for Image 2.",
            "datetime": "2024-07-11 09:20"
        },
        {
            "image": "Image 3",
            "location": "Tokyo, Japan",
            "os": "Windows Server 2019",
            "description": "This is a description for Image 3.",
            "datetime": "2024-07-12 17:45"
        },
        {
            "image": "Image 4",
            "location": "Sydney, Australia",
            "os": "Debian 10",
            "description": "This is a description for Image 4.",
            "datetime": "2024-07-13 12:15"
        },
        {
            "image": "Image 5",
            "location": "Berlin, Germany",
            "os": "Fedora 32",
            "description": "This is a description for Image 5.",
            "datetime": "2024-07-14 08:30"
        }
    ]

    context = {
        'segment': 'image',
        'images': images_data
    }
    return render(request, "pages/image.html", context)


def monitoring(request):
    alert_rules_data = [
        {
            "rule_name": "Rule 1",
            "status": "Active",
            "date_created": "2024-07-10"
        },
        {
            "rule_name": "Rule 2",
            "status": "Inactive",
            "date_created": "2024-07-11"
        },
        {
            "rule_name": "Rule 3",
            "status": "Active",
            "date_created": "2024-07-12"
        },
        {
            "rule_name": "Rule 4",
            "status": "Inactive",
            "date_created": "2024-07-13"
        },
        {
            "rule_name": "Rule 5",
            "status": "Active",
            "date_created": "2024-07-14"
        }
    ]

    context = {
        'segment': 'monitoring',
        'alert_rules': alert_rules_data
    }
    return render(request, "pages/monitoring.html", context)


def payment(request):
    balance_records = [
        {
            "payment_account": "Account 1",
            "payment_type": "Type 1",
            "payment_method": "Credit Card",
            "time": "2024-07-15 14:30",
            "recharge_amount": "$100.00",
            "operation": "View"
        },
        {
            "payment_account": "Account 2",
            "payment_type": "Type 2",
            "payment_method": "PayPal",
            "time": "2024-07-14 10:20",
            "recharge_amount": "$50.00",
            "operation": "View"
        },
        {
            "payment_account": "Account 3",
            "payment_type": "Type 3",
            "payment_method": "Alipay",
            "time": "2024-07-13 08:45",
            "recharge_amount": "$200.00",
            "operation": "View"
        }
    ]
    context = {
        'segment': 'payment',
        'balance_records': balance_records
    }
    return render(request, "pages/payment.html", context)


def resource_record(request):
    sample_data = [
        {
            "record_id": "Record 1",
            "location": "New York, USA",
            "configuration": "Config 1",
            "record_type": "Type A",
            "status": "Active",
            "record_time": "2024-07-10 14:30"
        },
        {
            "record_id": "Record 2",
            "location": "London, UK",
            "configuration": "Config 2",
            "record_type": "Type B",
            "status": "Inactive",
            "record_time": "2024-07-11 09:20"
        },
        {
            "record_id": "Record 3",
            "location": "Tokyo, Japan",
            "configuration": "Config 3",
            "record_type": "Type C",
            "status": "Active",
            "record_time": "2024-07-12 17:45"
        },
        {
            "record_id": "Record 4",
            "location": "Sydney, Australia",
            "configuration": "Config 4",
            "record_type": "Type D",
            "status": "Inactive",
            "record_time": "2024-07-13 12:15"
        },
        {
            "record_id": "Record 5",
            "location": "Berlin, Germany",
            "configuration": "Config 5",
            "record_type": "Type E",
            "status": "Active",
            "record_time": "2024-07-14 08:30"
        }
    ]

    context = {
        'segment': 'resource_record',
        'records': sample_data
    }
    return render(request, "pages/resource_record.html", context)


def billing(request):
    billing_records = [
        {
            "date": "2024-07-01",
            "billing_amount": "$100.00",
            "operation": "View"
        },
        {
            "date": "2024-07-02",
            "billing_amount": "$150.00",
            "operation": "View"
        },
        {
            "date": "2024-07-03",
            "billing_amount": "$200.00",
            "operation": "View"
        }
    ]

    billing_summary = {
        "expenses": 100,
        "charges_this_month": 500,
        "charges_last_hour": 50,
    }

    context = {
        'segment': 'billing',
        'billing_records': billing_records,
        'billing_summary': billing_summary
    }
    return render(request, "pages/billing.html", context)


def financial(request):
    context = {
        'segment': 'financial'
    }
    return render(request, "pages/dynamic-tables.html", context)


def support(request):
    context = {
        'segment': 'support'
    }
    return render(request, "pages/dynamic-tables.html", context)


def ticket(request):
    tickets = [
        {
            "ticket_id": "TICKET001",
            "subject": "Issue with login",
            "ticket_type": "Technical",
            "submission_time": "2024-07-01 14:30",
            "status": "Open",
            "operation": "View"
        },
        {
            "ticket_id": "TICKET002",
            "subject": "Billing discrepancy",
            "ticket_type": "Billing",
            "submission_time": "2024-07-02 09:20",
            "status": "Closed",
            "operation": "View"
        },
        {
            "ticket_id": "TICKET003",
            "subject": "Feature request",
            "ticket_type": "General",
            "submission_time": "2024-07-03 17:45",
            "status": "In Progress",
            "operation": "View"
        }
    ]

    context = {
        'segment': 'ticket',
        'tickets': tickets
    }
    return render(request, "pages/ticket.html", context)


def affiliate(request):
    context = {
        'segment': 'affiliate'
    }
    return render(request, "pages/dynamic-tables.html", context)


def link_code(request):
    context = {
        'segment': 'link_code'
    }
    return render(request, "pages/link_code.html", context)


def affiliate_stats(request):
    promotion_stats = {
        "referred_visitors": 100,
        "referred_signups": 50,
        "conversion_rate": "50%"
    }

    commission_stats = {
        "total_commission": 500,
        "commission_last_month": 100
    }
    context = {
        'segment': 'affiliate_stats',
        'promotion_stats': promotion_stats,
        'commission_stats': commission_stats
    }
    return render(request, "pages/affiliate_stats.html", context)


def account(request):
    context = {
        'segment': 'account'
    }
    return render(request, "pages/dynamic-tables.html", context)


def profile(request):
    context = {
        'segment': 'profile'
    }
    return render(request, "pages/profile.html", context)


def authentication(request):
    context = {
        'segment': 'authentication'
    }
    return render(request, "pages/authentication.html", context)


def notifications(request):
    context = {
        'segment': 'notifications'
    }
    return render(request, "pages/notifications.html", context)
