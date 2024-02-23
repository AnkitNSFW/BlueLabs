import sys, datetime
sys.path.append('')
from app.models import UserCred, OTP
from utility.email_functions.email_notification import send_otp_email
from utility.utility_func import jwt_encode, jwt_decode, generate_otp, to_sha256, utc_translation, current_DT


def user_exist(user_id):
    return UserCred.objects.filter(user_id=user_id).exists()

def UserLogin(user_id, user_password):
    msg=''
    jwt_token = None
    # try:
    if user_exist(user_id=user_id):
        user_details = UserCred.objects.get(user_id=user_id)
        if user_details.password==to_sha256(user_password):
            user_data = {
                'user_id': user_id,
                'password': to_sha256(user_password),
                'first_name': user_details.first_name,
                'last_name': user_details.last_name
            }
            jwt_token = jwt_encode(payload=user_data)
            msg='User verified'
            return msg, jwt_token
        else:
            msg='Invalid password'
            return msg, jwt_token
    else:
        return 'User does not exist', jwt_token
    # except:
    #     msg = 'Unable to access the Database.'
    #     return msg, jwt_token
    
def create_user(user_id, first_name, last_name, password):
    if not user_exist(user_id):
        UserCred(
            first_name=first_name,
            last_name=last_name,
            user_id=user_id,
            password=to_sha256(password)
        ).save()
        return True
    else:
        return False
    
def check_login_status(request):
    auth_token = request.session.get("auth_token", None)
    if auth_token: 
        user_data = jwt_decode(auth_token)
        if user_exist(user_data['user_id']):
            return user_data
    return None

def set_otp(user_id, first_name, last_name, password):
    if OTP.objects.filter(user_id=user_id).exists():
        OTP.objects.get(user_id=user_id).delete()

    otp = generate_otp()
    send_otp_email(to_addr=user_id, otp=otp)
    OTP(
        user_id= user_id,
        otp = otp,
        first_name = first_name,
        last_name = last_name,
        password = password,
        valid_till = datetime.datetime.now() + datetime.timedelta(minutes=2)
    ).save()

def update_user_last_login_timestamp(user_id):
    user = UserCred.objects.get(user_id=user_id)
    user.last_login = current_DT()
    user.save()

def fetch_user_name(user_id):
    if UserCred.objects.filter(user_id=user_id).exists():
        return UserCred.objects.get(user_id=user_id).first_name
    else:
        return "User"
    
def check_otp_and_make_user(user_id, otp):
    if OTP.objects.filter(user_id=user_id).exists():
        OTP_Object = OTP.objects.get(user_id=user_id)
        current =utc_translation(datetime.datetime.now())
        valid_till = OTP_Object.valid_till
        if (current>valid_till):
            return False, 'OTP has Expired, signup again'
        if str(OTP_Object.otp)==otp :
            create_user_status = create_user(
                                user_id=user_id, 
                                first_name=OTP_Object.first_name, 
                                last_name=OTP_Object.last_name, 
                                password=OTP_Object.password
                                )
            if create_user_status:
                OTP_Object.delete()
                return True, OTP_Object.password
            else:
                return False, 'Something went wrong'
        else:
            return False, 'Invalid OTP'
    else:
        return False, 'OTP not genetated, signup again'
