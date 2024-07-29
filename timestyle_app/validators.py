import re
from abc import ABC, abstractmethod

from django.forms import ValidationError
from .constants import *
from django.db.models import Model as DBModel
from collections import OrderedDict
# from .models import Users

class Validator(ABC):

    def __init__(self, required=False):
        super().__init__()
        self.required = required

    @abstractmethod
    def validate(self):
        pass

    @abstractmethod
    def performValidation(self, value: str, errorKey: str) -> str:
        pass

class EmptyDataValidator(Validator):

    def validate(self, value: str):
        return value is None or value.strip() == ""
    
    def performValidation(self, value: str, errorKey: str) -> str:
        pass

class RegexValidator(Validator):

    def __init__(self, regex: str, required=False):
        super().__init__(required=required)
        self.pattern = re.compile(regex)
        self.emptyValidator = EmptyDataValidator()

    def isEmpty(self, value: str):
        return self.emptyValidator.validate(value=value)
    
    def validate(self, value) -> bool:
        return self.pattern.match(value) is not None

    def performValidation(self, value: str, errorKey = "Input Field") -> str:
        isEmpty = self.isEmpty(value=value)
        if self.required and isEmpty:
            return errorKey + " is a required field"
        if not isEmpty and not self.validate(value):
            return "Invalid value '" + str(value) + "' for " + errorKey

class DateRegexValidator(RegexValidator):

    def __init__(self, required=False):
        super().__init__(regex=DATE_REGEX, required=required)

    def performValidation(self, value: str, errorKey = "Input Field") -> str:
        isEmpty = self.isEmpty(value=value)
        if self.required and isEmpty:
            return errorKey + " is a required field"
        if not isEmpty and re.match(DATE_REGEX, value, flags=re.IGNORECASE) is None:
            return errorKey + " given is invalid. Please provide in format (dd-mm-yyyy)"

class MobileRegexValidator(RegexValidator):

    def __init__(self, required = False):
        super().__init__(regex=MOBILE_REGEX, required=required)

    def performValidation(self, value: str, errorKey = "Input Field") -> str:
        print(self.pattern)
        error = super().performValidation(value, errorKey)
        # if error is None and Users.objects.filter(mobile_number=value).count() > 0:
        #     return "User already Exists with mobile: "+value
        return error
    def __call__(self, value):
        print(self.pattern)
        error = super().performValidation(value, "Input Field")
        if error is not None:
            raise ValidationError(error)

# class EmailRegexValidator(RegexValidator):

#     def __init__(self, required = False):
#         super().__init__(regex=EMAIL_REGEX, required=required)

#     def performValidation(self, value: str, errorKey = "Input Field") -> str:
#         error = super().performValidation(value, errorKey)
#         if error is None and Users.objects.filter(email=value).count() > 0:
#             return "User already Exists with email: "+value

class NameRegexValidator(RegexValidator):

    def __init__(self, required = False):
        super().__init__(regex=NAME_REGEX, required=required)
    

class DbBasedDataValidator(Validator):

    def __init__(self, dbModel: DBModel, required: bool = False) -> None:
        super().__init__(required=required)
        self.required = required
        self.dbModel = dbModel
        self.emptyValidator = EmptyDataValidator()



class UserDataSanityChecker():

    def __init__(self, fields: list) -> None:
        self.fields = fields
        self.firstNameValidator = NameRegexValidator(True)
        self.lastNameValidator = NameRegexValidator(False)
        # self.emailValidator = EmailRegexValidator(True)
        self.mobileValidator = MobileRegexValidator(True)
        self.dobValidator = DateRegexValidator(False)

    def getErrors(self, errors: list) -> list:
        return list(filter(lambda error: error is not None, errors))
    
    def runDataSanity(self, row: OrderedDict) -> list:
        errorStr = []
        for key in self.fields:
            value = row.get(key)
            if key == 'first_name':
                errorStr.append(self.firstNameValidator.performValidation(value, "First Name"))
            
            elif key == 'last_name':
                errorStr.append(self.lastNameValidator.performValidation(value, "Last Name"))

            elif key == 'email':
                errorStr.append(self.emailValidator.performValidation(value, "Email"))

            elif key == 'mobile_number':
                errorStr.append(self.mobileValidator.performValidation(value, "Mobile Number"))
            
            elif key == 'dob':
                errorStr.append(self.dobValidator.performValidation(value, "DOB"))
        
        return self.getErrors(errorStr)
        
