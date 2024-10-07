import math

from admin_datta.views import UserLoginView, UserRegistrationView
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.shortcuts import render, redirect
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime, timedelta, date
from django.shortcuts import render
from django.core.paginator import Paginator
import random
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated

from adapters.redis_service import CachedPlan
from config import APPConfig, ADMIN_CONFIG
from home.models import Vps, Ticket

from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.views import View
import os

from services.invoice import get_now
from services.report import TopUpCounter, InvoicePaidCounter, OrderCounter, UnpaidOrderCounter
from utils import number


def calculate_diff(current, previous):
    if previous == current == 0:
        return 0
    if previous == 0:
        return 100
    return math.floor(100 * (1 + (current - previous) / previous))


def get_top_up_day_data(counter, now):
    current_value = counter.get(now)
    previous_value = counter.get(now - timedelta(days=1))
    diff = calculate_diff(current_value, previous_value)
    return {'current': number(current_value), 'diff': diff}


def get_top_up_range_data(counter, now, days):
    current_value = counter.total_in_range(now - timedelta(days=days), now)
    previous_value = counter.total_in_range(now - timedelta(days=2 * days), now - timedelta(days=days))
    diff = calculate_diff(current_value, previous_value)
    return {'current': number(current_value), 'diff': diff}


def get_ctv_balance():
    url = ADMIN_CONFIG.URL + '/api/account/profile/'
    headers = {
            'Content-Type': 'application/json',
            'x-api-key': ADMIN_CONFIG.API_KEY
        }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return 0
    try:
        return response.json().get('balance_amount', 0)
    except Exception as e:
        return 0


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def index(request):
    user = request.user
    data = {}
    if user.is_staff and APPConfig.APP_ROLE == 'admin':
        top_up_counter = TopUpCounter()
        invoice_paid_counter = InvoicePaidCounter()
        order_counter = OrderCounter()
        unpaid_order_counter = UnpaidOrderCounter()

        now = get_now()

        data = {
            'deposits': {
                'day': get_top_up_day_data(top_up_counter, now),
                'month': get_top_up_range_data(top_up_counter, now, 30),  # 30 days for month
                'year': get_top_up_range_data(top_up_counter, now, 365),  # 365 days for year
                'total': number(top_up_counter.total())
            },
            'revenue': {
                'day': get_top_up_day_data(invoice_paid_counter, now),
                'month': get_top_up_range_data(invoice_paid_counter, now, 30),  # 30 days for month
                'year': get_top_up_range_data(invoice_paid_counter, now, 365),  # 365 days for year
                'total': number(invoice_paid_counter.total())
            },
            'orders': {
                'day': get_top_up_day_data(order_counter, now),
                'month': get_top_up_range_data(order_counter, now, 30),  # 30 days for month
                'year': get_top_up_range_data(order_counter, now, 365),  # 365 days for year
                'total': number(order_counter.total())
            },
            'unpaid_orders': int(unpaid_order_counter.total_in_range(now - timedelta(days=7), now)),
            'tickets': Ticket.objects.filter(status='open').count()
        }
    elif user.is_staff:
        top_up_counter = TopUpCounter()
        invoice_paid_counter = InvoicePaidCounter()
        order_counter = OrderCounter()
        unpaid_order_counter = UnpaidOrderCounter()

        now = get_now()

        data = {
            'deposits': {
                'day': get_top_up_day_data(top_up_counter, now),
                'month': get_top_up_range_data(top_up_counter, now, 30),  # 30 days for month
                'year': get_top_up_range_data(top_up_counter, now, 365),  # 365 days for year
                'total': number(top_up_counter.total())
            },
            'revenue': {
                'day': get_top_up_day_data(invoice_paid_counter, now),
                'month': get_top_up_range_data(invoice_paid_counter, now, 30),  # 30 days for month
                'year': get_top_up_range_data(invoice_paid_counter, now, 365),  # 365 days for year
                'total': number(invoice_paid_counter.total())
            },
            'orders': {
                'day': get_top_up_day_data(order_counter, now),
                'month': get_top_up_range_data(order_counter, now, 30),  # 30 days for month
                'year': get_top_up_range_data(order_counter, now, 365),  # 365 days for year
                'total': number(order_counter.total())
            },
            'unpaid_orders': int(unpaid_order_counter.total_in_range(now - timedelta(days=7), now)),
            'tickets': Ticket.objects.filter(status='open').count(),
            'balance': get_ctv_balance()
        }
    else:
        list_vps = Vps.objects.filter(user=request.user).filter(~Q(_deleted=True)).all()
        monthly_fee = 0
        plans = CachedPlan().get()
        for vps in list_vps:
            plan = next((p for p in plans if p.get('id') == vps.plan_id), {'price': 0})
            monthly_fee += plan.get('price')

        data = {
            'balance': user.balance_amount,
            'tickets': Ticket.objects.filter(status='open', user=request.user).count(),
            'vps': len(list_vps),
            'monthly_fee': monthly_fee

        }

    context = {
        'data': data,
        'segment': 'index',
    }
    return render(request, "pages/index.html", context)


def tables(request):
    context = {
        'segment': 'tables'
    }
    return render(request, "pages/dynamic-tables.html", context)


def home(request):
    context = {
        'segment': 'home'
    }
    return render(request, "pages/home.html", context)


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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def support(request):
    context = {
        'segment': 'support'
    }
    return render(request, "pages/dynamic-tables.html", context)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ticket(request):
    context = {
        'segment': 'ticket',
        'tickets': tickets
    }
    return render(request, "pages/supports/ticket.html", context)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def your_tickets(request):
    context = {
        'segment': 'ticket',
        'tickets': tickets
    }
    return render(request, "pages/supports/your_tickets.html", context)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_your_tickets(request):
    # tickets = Ticket.objects.all()
    #
    # search_query = request.GET.get('search', '')
    # if search_query:
    #     tickets = tickets.filter(subject__icontains(search_query))
    #
    # action_filter = request.GET.get('subject', '')
    # if action_filter:
    #     tickets = tickets.filter(subject=action_filter)
    #
    # sort_by = request.GET.get('sort_by', '-submission_time')
    # tickets = tickets.order_by(sort_by)

    paginator = Paginator(tickets, 1)  # 10 tickets per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    ticket_list = list(
        page_obj.object_list)

    data = {
        'tickets': ticket_list,
        'total_pages': paginator.num_pages,
        'current_page': page_obj.number
    }

    return JsonResponse(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ticket_detail_view(request, ticket_id):
    # ticket = get_object_or_404(Ticket, pk=ticket_id)
    # replies = TicketReply.objects.filter(ticket=ticket).order_by('created_at')

    # Sample data
    ticket = {
        'id': 1,
        'subject': 'Sample Ticket Subject',
        'ticket_type': 'Issue',
        'submission_time': '2024-07-28 12:34:56',
        'status': 'Open',
        'description': 'This is a sample description of the ticket.',
        'user': {
            'profile': {
                'avatar': {'url': '/media/avatars/sample_avatar.png'},
                'role': 'Admin'
            },
            'username': 'sampleuser'
        }
    }
    replies = [
        {
            'user': {
                'profile': {
                    'avatar': {'url': '/media/avatars/reply_avatar1.png'},
                    'role': 'support'
                },
                'username': 'supportuser1'
            },
            'created_at': '2024-07-28 13:45:00',
            'message': 'This is a sample reply message 1.'
        },
        {
            'user': {
                'profile': {
                    'avatar': {'url': '/media/avatars/reply_avatar2.png'},
                    'role': 'User'
                },
                'username': 'sampleuser'
            },
            'created_at': '2024-07-28 14:00:00',
            'message': 'This is a sample reply message 2.'
        }
    ]

    ticket_data = {
        'ticket_id': ticket['id'],
        'subject': ticket['subject'],
        'ticket_type': ticket['ticket_type'],
        'submission_time': ticket['submission_time'],
        'status': ticket['status'],
        'description': ticket['description'],
        'user_avatar': ticket['user']['profile']['avatar']['url'] if ticket['user']['profile']['avatar'] else '',
        'username': ticket['user']['username'],
        'user_role': ticket['user']['profile']['role'],
        'replies': [
            {
                'username': reply['user']['username'],
                'user_avatar': reply['user']['profile']['avatar']['url'] if reply['user']['profile']['avatar'] else '',
                'user_role': reply['user']['profile']['role'],
                'date': reply['created_at'],
                'message': reply['message'],
            }
            for reply in replies
        ]
    }
    return JsonResponse(ticket_data)


def affiliate(request):
    context = {
        'segment': 'affiliate'
    }
    return render(request, "pages/dynamic-tables.html", context)


def your_introducer(request):
    context = {
        'segment': 'your_introducer'
    }
    return render(request, "pages/your_introducer.html", context)


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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def account(request):
    context = {
        'segment': 'account'
    }
    return render(request, "pages/dynamic-tables.html", context)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    context = {
        'segment': 'profile'
    }
    return render(request, "pages/profile.html", context)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
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


# In-memory storage for tokens (for demonstration purposes)
tokens = []


@csrf_exempt
def manage_tokens(request):
    if request.method == 'GET':
        # List all tokens
        return JsonResponse(tokens, safe=False)

    elif request.method == 'POST':
        # Generate a new token
        data = json.loads(request.body)
        ttl = int(data['ttl'])
        expiry_time = 'Never' if ttl == -1 else (datetime.now() + timedelta(minutes=ttl)).isoformat()
        token = {
            'token': 'token-' + str(len(tokens) + 1),  # Simple token generation for demonstration
            'description': data['description'],
            'create_time': datetime.now().isoformat(),
            'expiry_time': expiry_time,
            'status': 'active'
        }
        tokens.append(token)
        return JsonResponse(token)

    return JsonResponse({'error': 'Invalid request'}, status=400)


# In-memory storage for demo purposes
introducer_email_storage = {}


def current_introducer(request):
    user_id = request.user.id
    introducer_email = introducer_email_storage.get(user_id, None)
    return JsonResponse({'introducer_email': introducer_email})


@csrf_exempt
def set_introducer(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        introducer_email = data.get('introducer_email')
        user_id = request.user.id

        if introducer_email:
            introducer_email_storage[user_id] = introducer_email
            return JsonResponse({'success': True})
    return JsonResponse({'success': False})


# In-memory storage for tickets and FAQs
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
faq_data = [
    {"question": "How does LightNode turn on the machine?",
     "answer": "Newly registered users can get up to $20 as a bonus for the first recharge. They only need to complete three steps: register, fill in basic information, and recharge the platform, and then they can activate the host that needs to be configured as needed.<br><br>PS: As long as the account balance is sufficient, you can always use the machine, no need to renew."},
    {"question": "What is the first charge of LightNode?",
     "answer": "The first charge of LightNode is the initial payment you make to start using the services."},
    {"question": "Does the LightNode system disk need to be selected separately?",
     "answer": "Yes, you need to select the system disk separately according to your requirements."},
    {"question": "What resource nodes does LightNode have?",
     "answer": "LightNode has resource nodes in various global locations including North America, Europe, Asia, and more."},
    {"question": "What operating systems does LightNode support?",
     "answer": "LightNode supports a variety of operating systems including Windows, Linux distributions like Ubuntu, Debian, CentOS, and more."},
    {"question": "What are the billing rules for LightNode?",
     "answer": "LightNode follows a pay-as-you-go billing model where you are billed based on the resources you use."}
]


@csrf_exempt
def faqs_view(request):
    if request.method == 'GET':
        return JsonResponse({'faqs': faq_data})


statuses = ['paid', 'unpaid', 'overdue']
invoices_data = [
    {
        'code': f'INV{str(i).zfill(3)}',
        'created': (date(2024, 1, 1) + timedelta(days=i)).isoformat(),
        'due_date': (date(2024, 1, 10) + timedelta(days=i)).isoformat(),
        'status': random.choice(statuses),
        'total': round(random.uniform(50, 500), 2)
    } for i in range(1, 51)
]


def get_vnc_link(request, instance_id):
    # Fetch the instance to ensure it exists

    # Sample data for VNC link (you should replace this with actual logic)
    vnc_link = {
        "link": f"https://vnc.example.com/{instance_id}"
    }

    return JsonResponse(vnc_link)


def get_snapshots(request, instance_id):
    # Fetch the instance to ensure it exists

    # Sample data for snapshots (you should replace this with actual logic)
    snapshots = [
        {"id": 1, "name": "Snapshot 1"},
        {"id": 2, "name": "Snapshot 2"},
        {"id": 3, "name": "Snapshot 3"}
    ]

    return JsonResponse({"snapshots": snapshots})
