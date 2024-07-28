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
            "id": 1,
            "server_name": "Server 1",
            "location": "New York, USA",
            "ip_address": "192.168.1.1",
            "status": "Active"
        },
        {
            "id": 2,
            "server_name": "Server 2",
            "location": "London, UK",
            "ip_address": "192.168.1.2",
            "status": "Inactive"
        },
        {
            "id": 3,
            "server_name": "Server 3",
            "location": "Tokyo, Japan",
            "ip_address": "192.168.1.3",
            "status": "Active"
        },
        {
            "id": 4,
            "server_name": "Server 4",
            "location": "Sydney, Australia",
            "ip_address": "192.168.1.4",
            "status": "Inactive"
        },
        {
            "id": 5,
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
    plans = [
        {
            "name": "VPS VN-1",
            "vcpu": "1 vCPU",
            "ram": "1GB RAM",
            "bandwidth": "1TB băng thông",
            "storage": "20GB SSD Enterprise",
            "price": "60,000 đ",
            "backup": "NO BACKUP",
            "link": "#"
        },
        {
            "name": "VPS VN-2",
            "vcpu": "1 vCPU",
            "ram": "2GB RAM",
            "bandwidth": "3TB băng thông",
            "storage": "20GB SSD Enterprise",
            "price": "120,000 đ",
            "backup": "NO BACKUP",
            "link": "#"
        },
        {
            "name": "VPS VN-3",
            "vcpu": "2 vCPU",
            "ram": "2GB RAM",
            "bandwidth": "3TB băng thông",
            "storage": "20GB SSD Enterprise",
            "price": "140,000 đ",
            "backup": "",
            "link": "#"
        },
        {
            "name": "VPS VN-4",
            "vcpu": "2 vCPU",
            "ram": "4GB RAM",
            "bandwidth": "5TB băng thông",
            "storage": "30GB SSD Enterprise",
            "price": "200,000 đ",
            "backup": "",
            "link": "#"
        },
        {
            "name": "VPS VN-6",
            "vcpu": "3 vCPU",
            "ram": "6GB RAM",
            "bandwidth": "5TB băng thông",
            "storage": "40GB SSD Enterprise",
            "price": "300,000 đ",
            "backup": "",
            "link": "#"
        },
        {
            "name": "VPS VN-8",
            "vcpu": "4 vCPU",
            "ram": "8GB RAM",
            "bandwidth": "10TB băng thông",
            "storage": "50GB SSD Enterprise",
            "price": "400,000 đ",
            "backup": "số lượng lớn ib giảm tới 10%",
            "link": "#"
        }
    ]
    ipv4_options = ["1 IPv4", "2 IPv4", "5 IPv4"]
    bandwidth_options = ["Default", "+ 5TB", "+ 10TB"]
    ram_options = ["Default", "+ 3GB", "+ 6GB"]
    ssd_options = ["Default", "+ 50GB", "+ 100GB"]

    # country
    regions = [
        "Asia", "North America", "Europe", "South America", "Africa", "Oceania", "Middle East", "ALL"
    ]

    locations = [
        {"name": "Washington", "country": "USA", "region": "North America"},
        {"name": "Silicon Valley", "country": "USA", "region": "North America"},
        {"name": "Toronto", "country": "Canada", "region": "North America"},
        {"name": "Vancouver", "country": "Canada", "region": "North America"},
        {"name": "Frankfurt", "country": "Germany", "region": "Europe"},
        {"name": "London", "country": "UK", "region": "Europe"},
        {"name": "Paris", "country": "France", "region": "Europe"},
        {"name": "Amsterdam", "country": "Netherlands", "region": "Europe"},
        {"name": "Jakarta", "country": "Indonesia", "region": "Asia"},
        {"name": "Singapore", "country": "Singapore", "region": "Asia"},
        {"name": "Tokyo", "country": "Japan", "region": "Asia"},
        {"name": "Seoul", "country": "South Korea", "region": "Asia"},
        {"name": "São Paulo", "country": "Brazil", "region": "South America"},
        {"name": "Buenos Aires", "country": "Argentina", "region": "South America"},
        {"name": "Cape Town", "country": "South Africa", "region": "Africa"},
        {"name": "Nairobi", "country": "Kenya", "region": "Africa"},
        {"name": "Sydney", "country": "Australia", "region": "Oceania"},
        {"name": "Melbourne", "country": "Australia", "region": "Oceania"},
        {"name": "Dubai", "country": "UAE", "region": "Middle East"},
        {"name": "Riyadh", "country": "Saudi Arabia", "region": "Middle East"},
    ]
    # Fetch flags using restcountries.com API
    # for location in locations:
    #     response = requests.get(f"https://restcountries.com/v3.1/name/{location['country']}?fields=flags")
    #     if response.status_code == 200:
    #         location_data = response.json()
    #         if location_data:
    #             location['flag'] = location_data[0]['flags']['png']
    #     else:
    #         location['flag'] = "https://via.placeholder.com/30"  # Fallback image

    # OS
    categories = ["ALL", "System Image"]
    images = [
        {"name": "Ubuntu", "versions": ["18.04", "19.04", "20.04", "22.04"], "category": "System Image",
         "image_url": "https://via.placeholder.com/50"},
        {"name": "Debian", "versions": ["9", "10", "11"], "category": "System Image",
         "image_url": "https://via.placeholder.com/50"},
        {"name": "AlmaLinux", "versions": ["8.4", "8.5", "8.6"], "category": "System Image",
         "image_url": "https://via.placeholder.com/50"},
        {"name": "Arch Linux", "versions": ["2020.05", "2021.06", "2022.07"], "category": "System Image",
         "image_url": "https://via.placeholder.com/50"},
        {"name": "CentOS", "versions": ["7", "8"], "category": "System Image",
         "image_url": "https://via.placeholder.com/50"},
        {"name": "FreeBSD", "versions": ["11", "12", "13"], "category": "System Image",
         "image_url": "https://via.placeholder.com/50"},
        {"name": "Rocky Linux", "versions": ["8.4", "8.5", "8.6"], "category": "System Image",
         "image_url": "https://via.placeholder.com/50"},
        {"name": "Windows", "versions": ["10", "Server 2016", "Server 2019"], "category": "System Image",
         "image_url": "https://via.placeholder.com/50"},
    ]
    context = {
        'segment': 'create_instances',
        'plans': plans,
        'ipv4_options': ipv4_options,
        'bandwidth_options': bandwidth_options,
        'ram_options': ram_options,
        'ssd_options': ssd_options,
        'regions': regions,
        'locations': locations,
        'categories': categories,
        'images': images,
    }
    return render(request, "pages/instances/create/create-instances.html", context)


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
    context = {
        'segment': 'ticket',
        'tickets': tickets
    }
    return render(request, "pages/supports/ticket.html", context)


def your_tickets(request):
    context = {
        'segment': 'ticket',
        'tickets': tickets
    }
    return render(request, "pages/supports/your_tickets.html", context)


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
                    'role': 'Support'
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


def instance_detail(request, instance_id):
    instance = {
        'id': 123,
        'server_name': 'Server-01',
        'ip_address': '192.168.1.1',
        'location': 'New York',
        'os': 'Ubuntu 20.04 LTS',
        'created_at': '2024-07-20 12:34:56',
        'last_modified': '2024-07-20 12:34:56',
        'detailed_location': 'Seoul',
        'country': 'South Korea',
        'image': 'AlmaLinux 8.4',
        'instance_type': 'VPS VN-3',
        'vcpu': '2 vCPU',
        'ram': '2GB RAM',
        'network': '3TB băng thông',
        'storage': '20GB SSD Enterprise',
        'additional_ipv4': '1 IPv4',
        'additional_ram': '+ 3GB',
        'additional_ssd': '+ 50GB',
        'bandwidth': '',
        'hostname': '2024071001535329714',
        'login': 'root',
        'password': 'password123'
    }

    os_options = ['Ubuntu 20.04 LTS', 'AlmaLinux 8.4', 'CentOS 7', 'Debian 10']
    instance_types = [
        {'name': 'VPS VN-3', 'vcpu': '2 vCPU', 'ram': '2GB RAM'},
        {'name': 'VPS VN-4', 'vcpu': '4 vCPU', 'ram': '4GB RAM'},
        {'name': 'VPS VN-5', 'vcpu': '8 vCPU', 'ram': '8GB RAM'},
    ]

    context = {
        'instance': instance,
        'os_options': os_options,
        'instance_types': instance_types,
    }

    return render(request, 'pages/instances/detail.html', context)


@csrf_exempt
def vps_calculator(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        # Extract configuration
        plan = data.get('plan', {})
        additional_ipv4 = data.get('ipv4', 'None')
        additional_ram = data.get('ram', 'None')
        additional_ssd = data.get('ssd', 'None')
        bandwidth = data.get('bandwidth', 'None')

        # Calculate total cost (example logic)
        total_cost = float(plan.get('price', 0))
        if additional_ipv4 != 'None':
            total_cost += 2.00  # Example cost for additional IPv4
        if additional_ram != 'None':
            total_cost += 5.00  # Example cost for additional RAM
        if additional_ssd != 'None':
            total_cost += 10.00  # Example cost for additional SSD
        if bandwidth != 'None':
            total_cost += 3.00  # Example cost for additional bandwidth

        return JsonResponse({'total_cost': total_cost})

    return JsonResponse({'error': 'Invalid request'}, status=400)


@csrf_exempt
def create_vps(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        # Extract configuration
        location = data.get('location', {})
        image = data.get('image', {})
        plan = data.get('plan', {})
        ipv4 = data.get('ipv4', 'None')
        bandwidth = data.get('bandwidth', 'None')
        ram = data.get('ram', 'None')
        ssd = data.get('ssd', 'None')
        login = data.get('login', {})

        # Here you would add the logic to actually create the VPS.
        # This might involve interacting with a VPS provider's API.

        # For now, we'll just return the received configuration for demo purposes
        response_data = {
            'status': 'success',
            'message': 'VPS created successfully',
            'vpsConfiguration': data
        }
        return JsonResponse(response_data)

    return JsonResponse({'error': 'Invalid request'}, status=400)


@csrf_exempt
def user_profile(request):
    if request.method == 'GET':
        # Fetch user profile data from the database
        profile = {
            'email': 'ngohongqui@gmail.com',
            'first_name': 'Ngô',
            'last_name': 'Quí',
            'address': 'Số 60 ngách 52/25 phú mỹ mỹ đình từ liêm hà nội',
            'city': 'Hà Nội',
            'country_region': 'Hong Kong (China)',
            'zip_code': '100000',
            'company_name': '',
            'phone_country': 'Vietnam(84)',
            'phone_number': '365046569',
            'subscribe_email': True
        }
        return JsonResponse(profile)

    elif request.method == 'PUT':
        data = json.loads(request.body)
        # Update the user profile in the database with the data received
        # For demonstration, we just print the data to the console
        print('Updated profile data:', data)
        return JsonResponse({'status': 'success', 'message': 'Profile updated successfully'})

    return JsonResponse({'error': 'Invalid request'}, status=400)


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


@csrf_exempt
def delete_token(request, token_id):
    global tokens
    tokens = [token for token in tokens if token['token'] != token_id]
    return JsonResponse({'status': 'success', 'message': 'Token deleted successfully'})


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
def tickets_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            ticket_id = len(tickets) + 1
            ticket = {
                'ticket_id': ticket_id,
                'subject': data['subject'],
                'ticket_type': data['ticket_type'],
                'description': data['description'],
                'submission_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'status': 'Open',
                'operation': 'View'
            }
            tickets.append(ticket)
            return JsonResponse({'success': True, 'ticket': ticket})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    elif request.method == 'GET':
        return JsonResponse({'tickets': tickets})


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


def invoices_view(request):
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    sort_order = request.GET.get('sort', 'created')
    items_per_page = int(request.GET.get('items', 10))

    invoices = invoices_data

    if search_query:
        invoices = [invoice for invoice in invoices if search_query.lower() in invoice['code'].lower()]

    if status_filter:
        invoices = [invoice for invoice in invoices if invoice['status'] == status_filter]

    if sort_order.startswith('-'):
        invoices = sorted(invoices, key=lambda x: x[sort_order[1:]], reverse=True)
    else:
        invoices = sorted(invoices, key=lambda x: x[sort_order])

    paginator = Paginator(invoices, items_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'pages/invoices.html', {'invoices': page_obj, 'items_per_page': items_per_page})


def vps_history(request):
    context = {
        'logs': []
    }
    return render(request, 'pages/instances/history/history.html', context)


def get_vps_logs(request):
    filterable_fields = ['instance_name']
    page = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 10)
    sort_by = request.GET.get('sort_by', '-datetime')
    filters = {field: request.GET.get(field) for field in filterable_fields if request.GET.get(field)}

    logs = [
        {
            "id": 1,
            "instance_name": "VPS-001",
            "action": "Create",
            "status": "Success",
            "performed_by": "user@example.com",
            "datetime": "2024-07-21 14:30:00",
            "details": "VPS created successfully."
        },
        {
            "id": 2,
            "instance_name": "VPS-002",
            "action": "Delete",
            "status": "Failed",
            "performed_by": "user@example.com",
            "datetime": "2024-07-22 10:15:00",
            "details": "Failed to delete VPS due to insufficient permissions."
        },
        {
            "id": 3,
            "instance_name": "VPS-003",
            "action": "Suspend",
            "status": "Success",
            "performed_by": "admin@example.com",
            "datetime": "2024-07-23 08:45:00",
            "details": "VPS suspended due to non-payment."
        },
        {
            "id": 4,
            "instance_name": "VPS-004",
            "action": "Upgrade",
            "status": "Success",
            "performed_by": "user@example.com",
            "datetime": "2024-07-24 12:30:00",
            "details": "VPS upgraded to a higher plan."
        },
        {
            "id": 1,
            "instance_name": "VPS-001",
            "action": "Create",
            "status": "Success",
            "performed_by": "user@example.com",
            "datetime": "2024-07-21 14:30:00",
            "details": "VPS created successfully."
        },
        {
            "id": 2,
            "instance_name": "VPS-002",
            "action": "Delete",
            "status": "Failed",
            "performed_by": "user@example.com",
            "datetime": "2024-07-22 10:15:00",
            "details": "Failed to delete VPS due to insufficient permissions."
        },
        {
            "id": 3,
            "instance_name": "VPS-003",
            "action": "Suspend",
            "status": "Success",
            "performed_by": "admin@example.com",
            "datetime": "2024-07-23 08:45:00",
            "details": "VPS suspended due to non-payment."
        },
        {
            "id": 4,
            "instance_name": "VPS-004",
            "action": "Upgrade",
            "status": "Success",
            "performed_by": "user@example.com",
            "datetime": "2024-07-24 12:30:00",
            "details": "VPS upgraded to a higher plan."
        },
        {
            "id": 1,
            "instance_name": "VPS-001",
            "action": "Create",
            "status": "Success",
            "performed_by": "user@example.com",
            "datetime": "2024-07-21 14:30:00",
            "details": "VPS created successfully."
        },
        {
            "id": 2,
            "instance_name": "VPS-002",
            "action": "Delete",
            "status": "Failed",
            "performed_by": "user@example.com",
            "datetime": "2024-07-22 10:15:00",
            "details": "Failed to delete VPS due to insufficient permissions."
        },
        {
            "id": 3,
            "instance_name": "VPS-003",
            "action": "Suspend",
            "status": "Success",
            "performed_by": "admin@example.com",
            "datetime": "2024-07-23 08:45:00",
            "details": "VPS suspended due to non-payment."
        },
        {
            "id": 4,
            "instance_name": "VPS-004",
            "action": "Upgrade",
            "status": "Success",
            "performed_by": "user@example.com",
            "datetime": "2024-07-24 12:30:00",
            "details": "VPS upgraded to a higher plan."
        },
        {
            "id": 1,
            "instance_name": "VPS-001",
            "action": "Create",
            "status": "Success",
            "performed_by": "user@example.com",
            "datetime": "2024-07-21 14:30:00",
            "details": "VPS created successfully."
        },
        {
            "id": 2,
            "instance_name": "VPS-002",
            "action": "Delete",
            "status": "Failed",
            "performed_by": "user@example.com",
            "datetime": "2024-07-22 10:15:00",
            "details": "Failed to delete VPS due to insufficient permissions."
        },
        {
            "id": 3,
            "instance_name": "VPS-003",
            "action": "Suspend",
            "status": "Success",
            "performed_by": "admin@example.com",
            "datetime": "2024-07-23 08:45:00",
            "details": "VPS suspended due to non-payment."
        },
        {
            "id": 4,
            "instance_name": "VPS-004",
            "action": "Upgrade",
            "status": "Success",
            "performed_by": "user@example.com",
            "datetime": "2024-07-24 12:30:00",
            "details": "VPS upgraded to a higher plan."
        },
        {
            "id": 1,
            "instance_name": "VPS-001",
            "action": "Create",
            "status": "Success",
            "performed_by": "user@example.com",
            "datetime": "2024-07-21 14:30:00",
            "details": "VPS created successfully."
        },
        {
            "id": 2,
            "instance_name": "VPS-002",
            "action": "Delete",
            "status": "Failed",
            "performed_by": "user@example.com",
            "datetime": "2024-07-22 10:15:00",
            "details": "Failed to delete VPS due to insufficient permissions."
        },
        {
            "id": 3,
            "instance_name": "VPS-003",
            "action": "Suspend",
            "status": "Success",
            "performed_by": "admin@example.com",
            "datetime": "2024-07-23 08:45:00",
            "details": "VPS suspended due to non-payment."
        },
        {
            "id": 4,
            "instance_name": "VPS-004",
            "action": "Upgrade",
            "status": "Success",
            "performed_by": "user@example.com",
            "datetime": "2024-07-24 12:30:00",
            "details": "VPS upgraded to a higher plan."
        },
        {
            "id": 1,
            "instance_name": "VPS-001",
            "action": "Create",
            "status": "Success",
            "performed_by": "user@example.com",
            "datetime": "2024-07-21 14:30:00",
            "details": "VPS created successfully."
        },
        {
            "id": 2,
            "instance_name": "VPS-002",
            "action": "Delete",
            "status": "Failed",
            "performed_by": "user@example.com",
            "datetime": "2024-07-22 10:15:00",
            "details": "Failed to delete VPS due to insufficient permissions."
        },
        {
            "id": 3,
            "instance_name": "VPS-003",
            "action": "Suspend",
            "status": "Success",
            "performed_by": "admin@example.com",
            "datetime": "2024-07-23 08:45:00",
            "details": "VPS suspended due to non-payment."
        },
        {
            "id": 4,
            "instance_name": "VPS-004",
            "action": "Upgrade",
            "status": "Success",
            "performed_by": "user@example.com",
            "datetime": "2024-07-24 12:30:00",
            "details": "VPS upgraded to a higher plan."
        },
        {
            "id": 1,
            "instance_name": "VPS-001",
            "action": "Create",
            "status": "Success",
            "performed_by": "user@example.com",
            "datetime": "2024-07-21 14:30:00",
            "details": "VPS created successfully."
        },
        {
            "id": 2,
            "instance_name": "VPS-002",
            "action": "Delete",
            "status": "Failed",
            "performed_by": "user@example.com",
            "datetime": "2024-07-22 10:15:00",
            "details": "Failed to delete VPS due to insufficient permissions."
        },
        {
            "id": 3,
            "instance_name": "VPS-003",
            "action": "Suspend",
            "status": "Success",
            "performed_by": "admin@example.com",
            "datetime": "2024-07-23 08:45:00",
            "details": "VPS suspended due to non-payment."
        },
        {
            "id": 4,
            "instance_name": "VPS-004",
            "action": "Upgrade",
            "status": "Success",
            "performed_by": "user@example.com",
            "datetime": "2024-07-24 12:30:00",
            "details": "VPS upgraded to a higher plan."
        }
    ]

    paginator = Paginator(logs, page_size)
    page_obj = paginator.get_page(page)

    logs_data = [data for data in page_obj]
    # logs_data = [
    #     {
    #         'id': log.id,
    #         'instance_name': log.instance_name,
    #         'action': log.action,
    #         'status': log.status,
    #         'performed_by': log.performed_by,
    #         'datetime': log.datetime,
    #         'details': log.details,
    #     }
    #     for log in page_obj
    # ]

    return JsonResponse({
        'logs': logs_data,
        'total_pages': paginator.num_pages,
        'current_page': page_obj.number,
        'has_next': page_obj.has_next(),
        'has_previous': page_obj.has_previous(),
    })


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
