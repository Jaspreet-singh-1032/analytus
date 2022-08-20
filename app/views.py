import logging
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

# utils
from analytus.utils import MongoDBHandler

# tasks
from .tasks import capture

logger = logging.getLogger()
db = MongoDBHandler()


class AnalyticsViewSet(viewsets.GenericViewSet):
    lookup_url_kwarg = "collection"

    @action(detail=True, methods=["post"])
    def capture(self, request, collection):
        data = request.data
        data["created"] = timezone.localtime()
        capture.delay(collection, data)
        return Response({"success": "done"}, status=status.HTTP_200_OK)        

    @action(detail=True, methods=["get"])
    def query(self, request, collection):
        results = db.query(collection, request.data)
        return Response({"results": results})
