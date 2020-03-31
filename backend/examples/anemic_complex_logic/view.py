from rest_framework.viewsets import ModelViewSet

from examples.anemic_complex_logic.model import Pause
from examples.anemic_complex_logic.serializer import PauseSerializer


class PauseViewSet(ModelViewSet):
    queryset = Pause.objects.all()
    serializer_class = PauseSerializer
