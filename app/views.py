import logging
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from analytus.utils import db

logger = logging.getLogger()


class AnalyticsViewSet(viewsets.GenericViewSet):
    lookup_url_kwarg = "collection"

    @action(detail=True, methods=["post"])
    def capture(self, request, collection):
        data = request.data
        data["created"] = timezone.localtime()
        try:
            db.insert_one(collection, data)
            return Response({"success": True}, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(e)
            return Response({"success": False}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["get"])
    def query(self, request, collection):
        query = request.query_params
        results = db.query(collection, query)
        return Response({"results": results})
