import enum


class NotificationType(enum.Enum):
    email = "email"


class Notificaiton:
    def __init__(self, type):
        self.type = type


class EmailNotification(Notificaiton):
    def __init__(self, email, subject, message):
        super().__init__(type=NotificationType.email)

        self.email = email
        self.subject = subject
        self.message = message
