import json, random, string, os
from PerfectCRM import settings
from django.utils.timezone import now
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from crm.permissions.permission import check_permission_decorate
from crm import forms, models
from django.core.cache import cache


# Create your views here.
@login_required
def index(request):
    return render(request, "index.html")


@check_permission_decorate
@login_required
def sales_index(request):
    """销售首页"""
    return render(request, "sales/index.html")


def customer_registration(request, enrollment_id, random_str):
    """客户需要填写报名信息"""
    if cache.get(enrollment_id) == random_str:
        enrollment_obj = models.Enrollment.objects.filter(id=enrollment_id).first()  # 获取报名对象
        customer_obj = enrollment_obj.customer  # 通过报名对象获取客户对象
        contract_content = enrollment_obj.enrolled_class.contract.content.format(qq=customer_obj.qq)
        if request.method == "GET":
            customer_form_obj = forms.CustomerModelForm(instance=customer_obj)
        else:
            customer_form_obj = forms.CustomerModelForm(request.POST, instance=customer_obj)
            if customer_form_obj.is_valid():
                error_dict = {}
                for k, v in customer_form_obj.cleaned_data.items():
                    if not v:  # 用户没写东西
                        error_dict[k] = "* 此项必填！"
                for error_field, error_message in error_dict.items():
                    customer_form_obj.add_error(error_field, error_message)
                if len(customer_form_obj.errors) == 0:
                    customer_form_obj.save()  # 存储用户对象
                    enrollment_obj.contract_agreed = True
                    enrollment_obj.save()  # 更新报名内容
        response = render(request, "customer/registration.html", {
            "enrollment_obj": enrollment_obj,
            "customer_form_obj": customer_form_obj,
            "contract_content": contract_content
        })
    else:
        response = render(request, "pages-403.html", {"errors": ["此链接已失效，请联系您的课程顾问重新为您生成报名链接！"]})
    return response


def upload_identity_photo(request):
    """客户上传身份证照片"""
    ret = {"status": False, "error": None, "data": None}  # 要返回的内容
    if request.method == "POST":
        if request.is_ajax():
            enrollment_id = request.POST.get("enrollment_id")  # 获取报名对象ID
            identity_photo_path = os.path.join(settings.ENROLLED_DATA_DIR, enrollment_id)  # 客户身份证照片存放地址
            os.makedirs(identity_photo_path, exist_ok=True)  # 确保目录存在
            for k, file_obj in request.FILES.items():  # 存储文件
                with open(os.path.join(identity_photo_path, file_obj.name), "wb") as f:
                    for line in file_obj:
                        f.write(line)
            ret["status"] = True
    return HttpResponse(json.dumps(ret))


@login_required
def download_identity_photo(request):
    """销售下载客户身份证照片进行核查"""
    if request.method == "GET":
        customer_id = request.GET.get("customer_id")
        enrolled_class_id = request.GET.get("enrolled_class_id")
        file_name = request.GET.get("file_name", "")
        enrollment_obj = models.Enrollment.objects.filter(
            customer__id=customer_id,
            enrolled_class_id=enrolled_class_id
        ).first()
        if enrollment_obj:
            identity_photo_path = os.path.join(settings.ENROLLED_DATA_DIR, str(enrollment_obj.id))  # 客户身份证照片存放地址
            file_path = os.path.join(identity_photo_path, file_name)
            if os.path.isfile(file_path):
                f = open(file_path, "rb")
                file_obj = f.read()
                f.close()
                # 设定文件头，这种设定可以让任意文件都能正确下载，而且已知文本文件不是本地打开
                response = HttpResponse(file_obj, content_type='APPLICATION/OCTET-STREAM')
                response['Content-Disposition'] = 'attachment; filename=' + file_name  # 设定传输给客户端的文件名称
                response['Content-Length'] = os.path.getsize(file_path)  # 传输给客户端的文件大小
                return response
            else:
                return HttpResponse("文件不存在！")
        else:
            return HttpResponse("报名信息不存在！")


def get_registration_url(enrollment_obj):
    """获取客户填写报名信息的随机URL"""
    random_str = "".join(random.sample(string.ascii_lowercase + string.digits, 6))
    cache.set(enrollment_obj.id, random_str, 60 * 10)  # 设置链接超时时间为10分钟
    registration_url = "http://127.0.0.1:8000/crm/customer/registration/%s/%s/" % (
        enrollment_obj.id, random_str
    )
    return registration_url


@login_required
def show_contract(request):
    """
    展示合同内容
    :param request:
    :return:
    """
    customer_id = request.GET.get("customer_id")
    enrolled_class_id = request.GET.get("enrolled_class_id")
    enrollment_obj = models.Enrollment.objects.filter(
        customer__id=customer_id,
        enrolled_class_id=enrolled_class_id
    ).first()
    customer_obj = enrollment_obj.customer  # 通过报名对象获取客户对象
    contract_content = enrollment_obj.enrolled_class.contract.content.format(qq=customer_obj.qq)
    return render(request, "show_contract.html", {"contract_content": contract_content})


@login_required
def contract_rejection(request, customer_id, enrolled_class_id):
    """
    驳回合同
    :param request:
    :param customer_id: 用户ID
    :param enrolled_class_id: 报名班级ID
    :return:
    """
    models.Enrollment.objects.filter(
        customer__id=customer_id,
        enrolled_class_id=enrolled_class_id
    ).update(contract_agreed=False, contract_approved=False)
    return redirect("/kind_admin/crm/customer/")


@login_required
def enrollment(request, customer_id):
    """销售为客户报名"""
    customer_obj = models.Customer.objects.filter(id=customer_id).first()  # 获取客户对象
    enrollment_form_obj = forms.EnrollmentForm()  # 报名model_from
    payment_form_obj = forms.PaymentModelForm()  # 缴费model_form
    if request.method == "POST":
        ret = {"status": False, "errors": None, "data": None}
        if request.POST.get("first_step"):
            # print("报名流程第一步！")
            enrollment_form_obj = forms.EnrollmentForm(request.POST)
            if enrollment_form_obj.is_valid():
                try:
                    enrollment_obj = models.Enrollment.objects.create(
                        customer=customer_obj,
                        enrolled_class_id=request.POST.get("enrolled_class"),
                        consultant=customer_obj.consultant,
                    )
                    ret["errors"] = "请将此链接发给客户填写:%s" % get_registration_url(enrollment_obj)
                except Exception as e:
                    enrollment_obj = models.Enrollment.objects.filter(
                        customer=customer_obj,
                        enrolled_class_id=request.POST.get("enrolled_class")
                    ).first()
                    if enrollment_obj.contract_agreed:  # 用户同意合同并填入了个人信息资料，此时销售可以继续第二步操作了
                        customer_obj = models.Customer.objects.filter(id=customer_id).first()  # 获取最新的客户对象
                        ret["data"] = {"identity_photo_list": [], "customer_info": {
                            "name": ["客户姓名", customer_obj.name],
                            "qq_name": ["qq名称", customer_obj.qq_name],
                            "phone": ["手机号", customer_obj.phone],
                            "person_id": ["身份证号", customer_obj.person_id],
                            "contact_email": ["联系邮箱", customer_obj.contact_email],
                        }}  # 第一步操作返回的内容
                        # 客户身份证照片存放地址
                        identity_photo_path = os.path.join(settings.ENROLLED_DATA_DIR, str(enrollment_obj.id))
                        for file_name in os.listdir(identity_photo_path):
                            ret["data"]["identity_photo_list"].append(file_name)
                        ret["status"] = True
                    else:
                        ret["errors"] = "请将此链接发给客户填写:%s" % get_registration_url(enrollment_obj)
            else:
                ret["errors"] = enrollment_form_obj.errors.as_ul()
            return HttpResponse(json.dumps(ret))
        elif request.POST.get("second_step"):
            # print("报名流程第二步！")
            ret["status"] = True
            return HttpResponse(json.dumps(ret))
        elif request.POST.get("third_step"):
            # print("报名流程第三步！")
            models.Enrollment.objects.filter(
                customer_id=request.POST.get("customer_id"),
                enrolled_class_id=request.POST.get("enrolled_class_id")
            ).update(contract_approved=True)
            ret["status"] = True
            return HttpResponse(json.dumps(ret))
        elif request.POST.get("fourth_step"):
            # print("报名流程第四步！")
            class_obj = models.ClassList.objects.filter(id=request.POST.get("enrolled_class_id")).first()  # 获取用户报名的班级
            data = {
                "customer": customer_obj,
                "course": class_obj.course,
                "amount": request.POST.get("amount"),
                "consultant": customer_obj.consultant,
            }
            payment_form_obj = forms.PaymentModelForm(data=data)
            if payment_form_obj.is_valid():
                models.Payment.objects.create(**data)  # 创建缴费记录
                customer_obj.status = 1  # 将客户状态改为已报名
                customer_obj.save()  # 保存客户对象
                ret["status"] = True
            else:
                ret["errors"] = payment_form_obj.errors.as_ul()
            return HttpResponse(json.dumps(ret))
    return render(request, "sales/enrollment.html", {
        "customer_obj": customer_obj,
        "enrollment_form_obj": enrollment_form_obj,
        "payment_form_obj": payment_form_obj,
    })
