from datetime import datetime

from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.viewsets import GenericViewSet

from web_tracker.journal.models import Visit
from web_tracker.journal.serializers import LinksSerialazer


class DomainsViewSet(ListModelMixin, GenericViewSet):

    def get_queryset(self):
        time_range = {"from": datetime.min, "to": datetime.max}
        for k, v in self.request.query_params.items():
            if k not in time_range:
                continue
            time_range[k] = datetime.fromtimestamp(int(v))
        return Visit.objects.filter(
            time__gt=time_range["from"], time__lt=time_range["to"]
        ).distinct()

    def list(self, request):
        visits = self.get_queryset()
        return Response(
            {
                "domains": visits.values_list("domain", flat=True),
                "status": ("ok", "no entries")[not visits],
            }
        )


class LinksViewSet(CreateModelMixin, GenericViewSet):
    serializer_class = LinksSerialazer

    def create(self, request):
        data = request.data.get("links", request.data)
        serializer = self.serializer_class(data=data, many=isinstance(data, list))
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"status": "ok"})
