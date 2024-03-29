import os
import re
import xlsxwriter

from django.db import transaction, IntegrityError
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password

from submission.models import Submission
from utils.api import APIView, validate_serializer
from utils.shortcuts import rand_str
from options.options import SysOptions
from django.utils.timezone import now
from django.template.loader import render_to_string
from utils.shortcuts import send_email
import smtplib
from datetime import timedelta

from ..decorators import super_admin_required, admin_role_required
from ..models import AdminType, ProblemPermission, User, UserProfile, ManagedUserList
from ..serializers import EditUserSerializer, UserAdminSerializer, GenerateUserSerializer
from ..serializers import ImportUserSeralizer,AllManagedUserListSerializer, ManagedUserListSerializer, CreateManagedUserListSerializer, GETManagedUserListSerializer, SendEmailForUsersAPISerializer

class SendEmailForUsersAPI(APIView):
    @validate_serializer(SendEmailForUsersAPISerializer)
    @admin_role_required
    def post(self, request):
        if not request.user.is_authenticated:
            return self.error("잘못 된 접근입니다.")
        if not SysOptions.smtp_config:
            return self.error("SMTP 설정이 되어있지 않습니다")
        data = request.data
        title = data["title"]
        content = data["content"]
        user_ids = data["user_ids"]

        excepted_user_list = []
        for user_id in user_ids:
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist: # 유저 존재 유무
                excepted_user_list.append(user_id)
                continue
            if not user.email: #이메일 존재하지 않을경우 except
                excepted_user_list.append(user_id)
                continue
            render_data = {
              "website_name": SysOptions.website_name,
              "content" : content
            }
            try:
                email_html = render_to_string("send_mail_default_form.html", render_data)
                send_email(smtp_config=SysOptions.smtp_config,
                           from_name=SysOptions.website_name_shortcut,
                           to_name=user.username,
                           to_email=user.email,
                           subject="[" + SysOptions.website_name_shortcut + "] " + title,
                           content=email_html)
            except smtplib.SMTPResponseException as e:
                # guess error message encoding
                msg = "이메일 전송에 실패했습니다"
                try:
                    msg = e.smtp_error
                    # qq mail
                    msg = msg.decode("gbk")
                except Exception:
                    msg = msg.decode("utf-8", "ignore")
                return self.error(msg)
            except Exception as e:
                msg = str(e)
                return self.error(msg)

        return self.success(excepted_user_list)

class AllManagedUserList(APIView):
    @admin_role_required
    def get(self, request):
        myself = request.GET.get("myself", None) # 자기 자신의 관리 리스트만 확인하기 위한 데이터
        search = request.GET.get("search",None)
        searchtype = request.GET.get("searchtype", None)
        userlists = ManagedUserList.objects.all()

        if (myself and myself == "1"):
            userlists = userlists.filter(writer=request.user.username)

        if search:
            if (searchtype == "0"): # 전체 검색
                userlists = userlists.filter(Q (title__icontains=search) | Q (content__icontains=search) | Q (writer__icontains=search) | Q(users__username__icontains=search)).distinct()
            elif (searchtype == "1"): # 제목에서 검색
                userlists = userlists.filter(title__icontains=search)
            elif (searchtype == "2"): # 내용에서 검색
                userlists = userlists.filter(content__icontains=search)
            elif (searchtype == "3"): # 작성자명에서 검색
                userlists = userlists.filter(writer__icontains=search)
            elif (searchtype == "4"): # 특정 유저명에서 검색
                userlists = userlists.filter(users__username__icontains=search)
        
        data = self.paginate_data(request, userlists) # 페이징
        data["results"] = AllManagedUserListSerializer(data["results"], many=True).data
        return self.success(data)

class ManagedUserListAPI(APIView):
    @admin_role_required
    def get(self, request):
        list_id = request.GET.get("id") # 파라미터로 전송된 ID값을 통해 유저리스트 출력
        try:
            userlist = ManagedUserList.objects.get(id = list_id)
        except:
            return self.error("존재하지 않는 관리리스트 입니다.")
        
        return self.success(GETManagedUserListSerializer(userlist).data)

    @admin_role_required
    @validate_serializer(ManagedUserListSerializer)
    def put(self, request):
        data = request.data
        list_id = data["id"]
        title = data["title"]
        content = data["content"]
        writer = request.user
        users = data["user_ids"]
        try:
            userlist = ManagedUserList.objects.get(id = list_id)
        except:
            return self.error("존재하지 않는 관리리스트 입니다.")
        userlist.title = title
        userlist.content = content

        except_userlist = []
        userlist.users.clear()
        for user_id in users:
            try:
                user = User.objects.get(id=user_id)
            except:
                except_userlist.append(user_id)
                continue
            userlist.users.add(user)
        userlist.save()
        return self.success(except_userlist)

    @admin_role_required
    @validate_serializer(CreateManagedUserListSerializer)
    def post(self, request):
        data = request.data
        title = data["title"]
        content = data["content"]
        writer = request.user
        users = data["user_ids"]
        if ManagedUserList.objects.filter(title__contains=title).exists():
            return self.error('이미 존재하는 제목입니다')
        userlist = ManagedUserList.objects.create(writer=writer,
                                                 title=title,
                                                 content=content)
        except_userlist = []
        for user_id in users:
            try:
                user = User.objects.get(id=user_id)
            except:
                except_userlist.append(user_id)
                continue
            userlist.users.add(user)
        userlist.save()
        return self.success(except_userlist)

    @admin_role_required
    def delete(self, request):
        id = request.GET.get("id")
        if not id:
            return self.error("잘못 된 값입니다")
        try:
            userlist = ManagedUserList.objects.get(id=id)
        except:
            return self.error("해당 리스트가 존재하지 않습니다")
        userlist.users.clear()
        userlist.delete()
        return self.success()

class ForceUpdateAllUserRatingAPI(APIView):
    @super_admin_required
    def get(self, request):
        users = User.objects.all()
        for user in users:
            user.userprofile.update_rating(user)
        return self.success()

class UserAdminAPI(APIView):
    @validate_serializer(ImportUserSeralizer)
    @super_admin_required
    def post(self, request):
        """
        Import User
        """
        data = request.data["users"]

        user_list = []
        for user_data in data:
          # id password email real_name school major
            try: 
                school = user_data[4]
            except IndexError:
                user_data.append('')
            try: 
                major = user_data[5]
            except IndexError:
                user_data.append('')
            if len(user_data[0]) < 1:
                return self.error('닉네임이 빈 데이터가 존재합니다.')
            if len(user_data[1]) < 1:
                return self.error('비밀번호가 빈 데이터가 존재합니다.')
            if len(user_data[3]) < 1:
                return self.error('이름이 빈 데이터가 존재합니다.')
            if len(user_data[0]) > 32:
                return self.error(f"'{user_data}' 처리 중 문제가 발생하였습니다.")
            # 이메일을 별도로 설정하지 않은 경우
            if len(user_data[2]) < 1:
                user_list.append(User(username=user_data[0], password=make_password(user_data[1])))  
            else:
                user_list.append(User(username=user_data[0], password=make_password(user_data[1]), email=user_data[2]))

        try:
            with transaction.atomic():
                ret = User.objects.bulk_create(user_list)
                UserProfile.objects.bulk_create([UserProfile(user=ret[i], real_name=data[i][3], school=data[i][4], major=data[i][5]) for i in range(len(ret))])
            return self.success()
        except IntegrityError as e:
            # Extract detail from exception message
            #    duplicate key value violates unique constraint "user_username_key"
            #    DETAIL:  Key (username)=(root11) already exists.
            return self.error(str(e).split("\n")[1])

    @validate_serializer(EditUserSerializer)
    @super_admin_required
    def put(self, request):
        """
        Edit user api
        """
        data = request.data
        try:
            user = User.objects.get(id=data["id"])
        except User.DoesNotExist:
            return self.error("존재하지 않는 유저입니다")
        if User.objects.filter(username=data["username"].lower()).exclude(id=user.id).exists():
            return self.error("Username already exists")
        if data["email"]:
            if User.objects.filter(email=data["email"].lower()).exclude(id=user.id).exists():
                return self.error("Email already exists")
        else:
            data["email"] = ""

        pre_username = user.username
        user.username = data["username"].lower()
        user.email = data["email"].lower()
        user.admin_type = data["admin_type"]
        user.is_disabled = data["is_disabled"]
        user.is_email_verify = data["is_email_verify"]

        if data["admin_type"] == AdminType.ADMIN:
            user.problem_permission = data["problem_permission"]
        elif data["admin_type"] == AdminType.SUPER_ADMIN:
            user.problem_permission = ProblemPermission.ALL
        else:
            user.problem_permission = ProblemPermission.NONE

        if data["password"]:
            user.set_password(data["password"])

        if data["open_api"]:
            # Avoid reset user appkey after saving changes
            if not user.open_api:
                user.open_api_appkey = rand_str()
        else:
            user.open_api_appkey = None
        user.open_api = data["open_api"]

        if data["two_factor_auth"]:
            # Avoid reset user tfa_token after saving changes
            if not user.two_factor_auth:
                user.tfa_token = rand_str()
        else:
            user.tfa_token = None

        user.two_factor_auth = data["two_factor_auth"]

        user.save()
        if pre_username != user.username:
            Submission.objects.filter(username=pre_username).update(username=user.username)

        UserProfile.objects.filter(user=user).update(real_name=data["real_name"])
        return self.success(UserAdminSerializer(user).data)

    @super_admin_required
    def get(self, request):
        """
        User list api / Get user by id
        """
        user_id = request.GET.get("id")
        if user_id:
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return self.error("존재하지 않는 유저입니다")
            return self.success(UserAdminSerializer(user).data)

        user = User.objects.all().order_by("-create_time")

        keyword = request.GET.get("keyword", None)
        if keyword:
            user = user.filter(Q(username__icontains=keyword) |
                               Q(userprofile__real_name__icontains=keyword) |
                               Q(email__icontains=keyword))
        return self.success(self.paginate_data(request, user, UserAdminSerializer))

    @super_admin_required
    def delete(self, request):
        id = request.GET.get("id")
        if not id:
            return self.error("Invalid Parameter, id is required")
        ids = id.split(",")
        if str(request.user.id) in ids:
            return self.error("Current user can not be deleted")
        User.objects.filter(id__in=ids).delete()
        return self.success()


class GenerateUserAPI(APIView):
    @super_admin_required
    def get(self, request):
        """
        download users excel
        """
        file_id = request.GET.get("file_id")
        if not file_id:
            return self.error("Invalid Parameter, file_id is required")
        if not re.match(r"^[a-zA-Z0-9]+$", file_id):
            return self.error("Illegal file_id")
        file_path = f"/tmp/{file_id}.xlsx"
        if not os.path.isfile(file_path):
            return self.error("File does not exist")
        with open(file_path, "rb") as f:
            raw_data = f.read()
        os.remove(file_path)
        response = HttpResponse(raw_data)
        response["Content-Disposition"] = "attachment; filename=users.xlsx"
        response["Content-Type"] = "application/xlsx"
        return response

    @validate_serializer(GenerateUserSerializer)
    @super_admin_required
    def post(self, request):
        """
        Generate User
        """
        data = request.data
        number_max_length = max(len(str(data["number_from"])), len(str(data["number_to"])))
        if number_max_length + len(data["prefix"]) + len(data["suffix"]) > 32:
            return self.error("Username should not more than 32 characters")
        if data["number_from"] > data["number_to"]:
            return self.error("Start number must be lower than end number")

        file_id = rand_str(8)
        filename = f"/tmp/{file_id}.xlsx"
        workbook = xlsxwriter.Workbook(filename)
        worksheet = workbook.add_worksheet()
        worksheet.set_column("A:B", 20)
        worksheet.write("A1", "Username")
        worksheet.write("B1", "Password")
        i = 1

        user_list = []
        for number in range(data["number_from"], data["number_to"] + 1):
            raw_password = rand_str(data["password_length"])
            user = User(username=f"{data['prefix']}{number}{data['suffix']}", password=make_password(raw_password))
            user.raw_password = raw_password
            user_list.append(user)

        try:
            with transaction.atomic():

                ret = User.objects.bulk_create(user_list)
                UserProfile.objects.bulk_create([UserProfile(user=user) for user in ret])
                for item in user_list:
                    worksheet.write_string(i, 0, item.username)
                    worksheet.write_string(i, 1, item.raw_password)
                    i += 1
                workbook.close()
                return self.success({"file_id": file_id})
        except IntegrityError as e:
            # Extract detail from exception message
            #    duplicate key value violates unique constraint "user_username_key"
            #    DETAIL:  Key (username)=(root11) already exists.
            return self.error(str(e).split("\n")[1])
