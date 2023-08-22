from rest_framework.generics import get_object_or_404

from ..establishment.models import Establishment
from ..verification.models import CommonListPost, CheckList, ListPost, TrialCheck


class CheckService:
    @staticmethod
    def create_check(establishment_pk, representative_name, user):
        establishment = get_object_or_404(Establishment, pk=establishment_pk)

        check = CheckList.objects.create(
            establishment=establishment,
            user=user,
            representative_name=representative_name
        )

        CheckService._create_common_list_posts(check)
        return check

    @staticmethod
    def _create_common_list_posts(check):
        list_posts = ListPost.objects.all()
        check_list_posts = [
            CommonListPost(check_points=list_post, check_list=check)
            for list_post in list_posts
        ]
        CommonListPost.objects.bulk_create(check_list_posts)


class CheckListService:
    @staticmethod
    def get_checklists_for_user(user):
        return CheckList.objects.filter(user=user)

    @staticmethod
    def get_check_by_pk(check_pk):
        return get_object_or_404(CheckList, pk=check_pk)

    @staticmethod
    def get_common_list_posts_for_checklist(checklist_pk):
        return CommonListPost.objects.filter(check_list_id=checklist_pk)


def create_or_update_trial_checks(check_points, data):
    for check_point in check_points:
        is_approved = data.get(f'check_point_{check_point.id}', False)
        trial_check, created = TrialCheck.objects.get_or_create(check_point=check_point)
        trial_check.is_approved = is_approved
        trial_check.save()
