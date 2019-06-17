from rest_framework.routers import DefaultRouter
from api import viewsets


router = DefaultRouter()
router.include_root_view = False
router.register('records', viewsets.CallRecordViewSet)
router.register('bills', viewsets.BillRetrieveViewSet)
