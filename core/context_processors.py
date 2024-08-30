# myapp/context_processors.py

from config import APPConfig


def my_constants(request):
    """
    A context processor that adds the MY_CONSTANT setting to the context.
    """
    return {
        'APP_ROLE': APPConfig.APP_ROLE,
    }