from django.http import JsonResponse
from django.views import View
from loguru import logger

class TestLoggingView(View):
    def get(self, request):
        logger.debug('this is a debug message')
        logger.info('this is a debug message')
        logger.warning('this is a debug message')
        logger.error('this is a debug message')
        logger.critical('this is a debug message')
        return JsonResponse({'status': 'success'})