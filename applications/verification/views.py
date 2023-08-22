from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView, CreateAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from applications.verification.models import CommonListPost, CheckList, ListPost, TrialCheck
from applications.verification.permissions import IsEmployeePermission
from applications.verification.serializer import \
    CommonListPostSerializer, CheckSerializer, CheckListSerializer, CheckDetailSerializer, TrialCheckSerializer
from .pagination import StandardResultSetPagination
from ..services.verification_services import CheckService, CheckListService, create_or_update_trial_checks


class CheckCreationView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsEmployeePermission]
    serializer_class = CheckSerializer

    def create(self, request, *args, **kwargs):
        establishment_pk = request.data.get('establishment_id')
        representative_name = request.data.get('representative_name')

        check = CheckService.create_check(establishment_pk, representative_name, self.request.user)
        return Response({'message': 'Check created successfully', 'check_id': check.id}, status=status.HTTP_201_CREATED)


class CheckListView(ListAPIView):
    serializer_class = CheckListSerializer
    permission_classes = [IsAuthenticated, IsEmployeePermission]

    def get_queryset(self):
        user = self.request.user
        return CheckListService.get_checklists_for_user(user)


class CheckItemListView(ListAPIView):
    queryset = CommonListPost.objects.all()
    serializer_class = CommonListPostSerializer
    pagination_class = StandardResultSetPagination
    permission_classes = [IsAuthenticated, IsEmployeePermission]

    def get_queryset(self, *args, **kwargs):
        checklist_pk = self.kwargs.get('check_pk')
        return CheckListService.get_common_list_posts_for_checklist(checklist_pk)


class CheckDetailView(RetrieveUpdateAPIView):
    queryset = CheckList.objects.all()
    serializer_class = CheckDetailSerializer
    permission_classes = [IsAuthenticated, IsEmployeePermission]

    def get_object(self):
        check_pk = self.kwargs.get('check_pk')
        return CheckListService.get_check_by_pk(check_pk)


class CheckItemDetailView(RetrieveUpdateAPIView):
    queryset = CommonListPost.objects.all()
    serializer_class = CommonListPostSerializer
    permission_classes = [IsAuthenticated, IsEmployeePermission]
    lookup_url_kwarg = 'item_pk'

    def get_queryset(self):
        check_pk = self.kwargs.get('check_pk')
        item_pk = self.kwargs.get('item_pk')
        return CommonListPost.objects.filter(pk=item_pk, check_list_id=check_pk)

    def perform_update(self, serializer):
        serializer.save()


class TrialCheckView(ListCreateAPIView):
    queryset = TrialCheck.objects.all()
    serializer_class = TrialCheckSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        check_points = ListPost.objects.all()

        create_or_update_trial_checks(check_points, request.data)

        self.queryset = TrialCheck.objects.all()

        approved_count = self.queryset.filter(is_approved=True).count()
        total_points = self.queryset.count()

        if total_points > 0:
            pass_percentage = (approved_count / total_points) * 100
        else:
            pass_percentage = 0

        result = "Прошел" if pass_percentage >= 60 else "Не прошел"
        non_approved_points = list(self.queryset.filter(is_approved=False))

        response_data = {
            "result": result,
            "pass_percentage": pass_percentage,
            "non_approved_points": TrialCheckSerializer(non_approved_points, many=True).data
        }

        return Response(response_data)
