import json
import datetime

from django.http    import JsonResponse
from django.views   import View

from users.models   import User
from records.models import Record
class MyPageView(View):
    # @login_confirm
    def get(self, request, user_type_id):
        # 멘토 페이지 만들면 연결시키고 활성화
        if user_type_id == 1:
            return JsonResponse({'message': 'WE_NEED_MORE_TIME..!'}, status = 200)

        if user_type_id == 2:
            # user = request.user
            user     = User.objects.get(id=1)
            user     = User.objects.select_related('user_type', 'batch', 'position').get(id=user.id)
            now      = datetime.datetime.now()
            time_gap = datetime.timedelta(seconds=32406)
            kor_time = now + time_gap
            today    = kor_time.date()

            records     = Record.objects.filter(user_id=user.id)
            start_sum   = 0
            start_count = 0
            end_sum     = 0
            end_count   = 0

            for record in records:
                if record.start_at:
                    standard_time = record.start_at.replace(hour=0, minute=0, second=0, microsecond=0)
                    total         = (record.start_at-standard_time).total_seconds()
                    start_sum    += total
                    start_count  += 1
                if record.end_at:
                    standard_time = record.end_at.replace(hour=0, minute=0, second=0, microsecond=0)
                    total         = (record.end_at-standard_time).total_seconds()
                    end_sum      += total
                    end_count    += 1

            DATES_ON_GRAPH = 7
            if len(records) <= 7:
                week_records = records
            week_records = records[-DATES_ON_GRAPH:]
            
            weekly_record_result = {}
            for week_record in week_records:
                weekly_record_result['MON'] = week_record.oneday_time if week_record.start_at.weekday() == 0 else None
                weekly_record_result['TUE'] = week_record.oneday_time if week_record.start_at.weekday() == 1 else None
                weekly_record_result['WED'] = week_record.oneday_time if week_record.start_at.weekday() == 2 else None
                weekly_record_result['THU'] = week_record.oneday_time if week_record.start_at.weekday() == 3 else None
                weekly_record_result['FRI'] = week_record.oneday_time if week_record.start_at.weekday() == 4 else None
                weekly_record_result['SAT'] = week_record.oneday_time if week_record.start_at.weekday() == 5 else None
                weekly_record_result['SUN'] = week_record.oneday_time if week_record.start_at.weekday() == 6 else None

            total_accumulate_record_result = []
            oneday_time_sum = 0
            for record in records:
                oneday_time_sum += record.oneday_time
                total_accumulate_record_result.append(oneday_time_sum)

            result = [
                {
                    'user_information' : {
                                'user_id'                : user.id,
                                'user_name'              : user.name,
                                'user_profile_image_url' : user.profile_image_url,                                    'user_total_time'        : user.total_time
                    },
                    'record_information' : {
                                'weekly_record'           : weekly_record_result,
                                'total_accumulate_record' : total_accumulate_record_result,
                                'average_start_time'      : str(datetime.timedelta(seconds=start_sum//start_count)),
                                'average_end_time'        : str(datetime.timedelta(seconds=end_sum//end_count)),
                                'wecode_d_day'            : (today-user.batch.start_day).days

                    }
                }
            ]

            return JsonResponse({'result': result}, status = 200)