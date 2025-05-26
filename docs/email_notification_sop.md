# Email Notification Manual

## 1. Overview:
This document describes the usage of the email notification service. The service is responsible for constructing and sending email messages for different events, such as:

- User login

- Tutoring session reminders

- Password recovery

- Successful user registration

- Successful password change

- Creation of a new tutoring

It uses a builder pattern to construct email content dynamically and an SMTP-based service to send it.

## 2. Importing the Framework:
To use the email notification service in your module or script, import the following function:

```python
from app.services.notification import send_email_notification
```

## 3. Usage Example:
**To send a email notification, follow these steps:**

### Step 1: Create a python diccionary `email_data` with the required fields:
Example:
```python
    email_data = {
        # Add required fields in email_data
    }
```
Required Fields in `email_data` types:
| Type                 | Description                                      |
|----------------------|--------------------------------------------------|
| `username`           | The username of the user currently in session.   |
| `emailTo`            | Email to send notification.                      |
| `tutorial`            | Tutoria to be notified.                          |
| `reset_link`         | Recovery password link.                          |

### Step 2: Send the email using the notification service:
```python
    if not send_email_notification("<type_email_notification>", email_data):
        # TODO If email sending fails, log the error
        pass
```

The `"<type_email_notification>"` can be the follow types of email notifications:

| Type                 | Description                                      |     Required Fields in `email_data`      |
|----------------------|--------------------------------------------------|------------------------------------------|
| `"login"`            | Sends a "successful login" notification          |`username`, `emailTo`                     |
| `"reminder"`         | Sends a tutoring session reminder                |`username`, `emailTo`, `tutorial`          |
| `"recoveryPassword"`       | Sends password recovery instructions       |`username`, `emailTo`, `reset_link` |
| `"successRegister"`        | Sends a "successful register" notification       |`username`, `emailTo`,      |
| `"successPasswordChange"`  | Sends a "successful password change" notification       |`username`, `emailTo`,      |
| `"newTutorial"`  | Sends a "successful password change" notification       |`username`, `emailTo`, `tutorial`     |


## Good Practices:
- Always validate email_data before calling the notification service.
- Use environment variables for sensitive data such as SMTP credentials, if you do not have them, ask a member of the notification team.
- Wrap the call to send_email_notification() in try-except blocks in critical systems.


----------------------------------------------------------------------------------------------------------------------

# Design patterns applied in Email Notification

## Functionality
The system for sending notifications by email, where depending on the type of notification (login, reminder, recoveryPassword, etc.), a different email body is constructed and sent using an SMTP service.

### Pattern Factory
It allows to instantiate objects without directly coupling the logic of the type to be created. The decision of which class to instantiate is centralized in the factory `EmailBuilderFactory`, which produces a builder according to the type of notification.

### Pattern Strategy
Allows encapsulating interchangeable algorithms. In this context, each builder (e.g., LoginEmailBuilder, ReminderEmailBuilder) is a strategy implementing the shared interface IBuilder, making them interchangeable at runtime for building email content.

## Motivation for use

- Extensibility: New email types can be easily added by implementing a new builder without modifying the existing code.

- Decoupling: The `EmailService` does not know the details of each email type. It only knows that there is a common interface to build them.

- Single Responsibility: Each class is responsible for building a specific message type or managing its delivery.

## Explanation of implementation and extension guidance

### **1. Builders interface (IBuilder)**

Defined in [`i_notification_builder.py`](../app/services/notification/builders/i_notification_builder.py).

```python
class IBuilder(ABC):
  @abstractmethod
  def build_body(self, data: dict) -> dict:
    pass
```
This interface standardizes the contract for building an email body.

### **2. Concrete builders**
Implemented in [`email_notification_builders.py`](../app/services/notification/builders/email_notification_builders.py) can see the builders.
Examples:
`LoginEmailBuilder`, `ReminderEmailBuilder`, etc. Each implements `build_body(data)` and returns the email content.

### **3. EmailBuilderFactory**
Defined in [`email_service.py`](../app/services/notification/email_service.py), this factory selects the appropriate builder based on a string identifier.

```python
builder = self.factory.create_builder(builder_type)
```

### **4. Mail sending service (email_service.py)**
Located in [`email_service.py`](../app/services/notification/email_service.py), this class `EmailService()` coordinates the entire email-sending process.

**Main Responsibilities:**
- Retrieves the appropriate builder from the factory.

- Builds the email content using the builder.

- Sends the email through an injected notification service (SMTP).

**Key contributors:**

- *IBuilderFactory:* Selects the builder based on type.

- *INotificationService:* Abstract interface to send notifications.

**Workflow**
The `send_email(builder_type: str, data: dict)` method performs the following actions:

- Get the correct builder: the factory `create_builder` method is called to get the appropriate builder based on `builder_type`.

- Build content: The builder generates the message data.

- Send email: Uses the notification service to send the email.

For implementation details, refer to [`email_service.py`](../app/services/notification/email_service.py).

### **5. Guide to extending the email notification system**
To add a new email notification type in [`email_factory.py`](../app/services/notification/factories/email_factory.py), follow these steps:

- Create a new class that implements IBuilder in  [`email_notification_builders.py`](../app/services/notification/builders/email_notification_builders.py).

- Implement the build_body(data: dict) method with the corresponding logic.

- Register this class in EmailBuilderFactory.create_builder(...) adding a new elif.

Example:

```python
class EmailBuilderFactory(IBuilderFactory):
  def create_builder(self, builder_type: str) -> IBuilder:
    if builder_type == "login":
      return email_notification_builders.LoginEmailBuilder()
    elif builder_type == "reminder":
      return email_notification_builders.ReminderEmailBuilder()
    # New mail notification type
    elif builder_type == "<new_type_email_notification>":
        # new type email notification builder create in email_notification_builders.py 
      return email_notification_builders.NewTypeEmailBuilder()
    else:
      raise ValueError("Builder no soportado")

```