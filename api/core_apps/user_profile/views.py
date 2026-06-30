from django.http import JsonResponse
from django.views import  View
from loguru import logger

class Test(View):
    def get(self, request):
        logger.debug('debug')
        logger.info('info')
        logger.warning('warning')
        logger.critical('critical')
        logger.error('error')
        return JsonResponse({"message": "OK"})

