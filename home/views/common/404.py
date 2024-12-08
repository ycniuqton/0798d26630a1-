from django.shortcuts import render


def custom_404(request, exception):
    return render(request, 'pages/common/404.html', {}, status=404)
