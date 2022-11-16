from pydantic import BaseModel, validator
import regex as re


class APIError(ConnectionError):
    pass


class InvalidEmail(ValueError):
    pass


class InvalidPhoneNumber(ValueError):
    pass


class InvalidPointOfContact(ValueError):
    pass


class CustomData(BaseModel):
    clientSkinType: str = ''
    clientSkinSensivity: str = ''
    clientMainIssue: str = ''
    city: str = ''
    customerTelegramId: str | int
    customerDoctorSpecialization: str = ''
    howHearAboutNaosPro: str = ''


class SubscribeData(BaseModel):
    brand: str
    pointOfContact: str

    @validator('pointOfContact')
    def valid_point_of_contact(cls, point_of_contact: str) -> str:
        possible_values = ('Email', 'SMS', 'Viber', 'Webpush', 'Mobilepush')
        error_text = f'Системное имя канала подписки может принимать значения: {", ".join(possible_values)}'
        if point_of_contact in possible_values:
            return point_of_contact
        else:
            raise InvalidPointOfContact(error_text)


class CustomerData(BaseModel):
    email: str
    lastName: str
    firstName: str
    middleName: str
    mobilePhone: str = ''
    customFields: CustomData
    subscriptions: list[SubscribeData] = list()

    @validator('email')
    def valid_email(cls, email: str) -> str:
        error_text = (
            'Должен соответствовать RFC 5321. Если упростить, то любой email должен подходить под шаблон:\n'
            '{латиница, цифры и некоторые знаки пунктуации}@{домен}\n\n'
            'Где домен - это 1 или более секций разделенных точками и состоящих из латиницы, цифр или дефиса. Каждая секция домена должна быть не больше 61 символа.\n'
            'Максимальная длина email - 254 символа\n'
        )
        email_re = r"^([\p{L}0-9_\-!#\$%&'\*\+/=\?\^`\{}\|~])+([\.\p{L}0-9_\-!#\$%&'\*\+/=\?\^`\{}\|~])*@([\p{L}0-9]([\p{L}0-9\-]{0,61}[\p{L}0-9])?\.)*[\p{L}0-9]([\p{L}0-9\-]{0,61}[\p{L}0-9])?$"
        if re.match(email_re, email) and len(email) <= 254:
            return email
        else:
            raise InvalidEmail(error_text)

    @validator('mobilePhone')
    def valide_phone_number(cls, phone_number: str) -> str:
        error_text = 'Неверный номер телефона'
        phone_number = phone_number.replace('-', '').replace('+', '').replace('(', '').replace(')', '').replace(' ', '')
        if (phone_number.isdigit() and len(phone_number) >= 11) or phone_number == '':
            return phone_number
        else:
            raise InvalidPhoneNumber(error_text)
