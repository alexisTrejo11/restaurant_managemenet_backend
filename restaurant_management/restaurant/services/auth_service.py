from restaurant.utils.result import Result

class AuthService:
    def __init__(self):
        pass

    def validate_staff_singup_credentials(self, serializer_data) -> Result:
        return Result.success()

    def validate_login_credentials(self)-> Result:
        return Result.success()

    def proccess_login(self):
        pass

    def proccess_singup(self):
        pass