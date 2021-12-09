from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.mail import send_mail
from django.core.validators import MinLengthValidator, RegexValidator
from phonenumber_field.modelfields import PhoneNumberField
from faker import Faker
from students.validators import no_elon_validator, older_than_18
from django.utils.translation import ugettext as _
from students.managers import CustomUserManager, PeopleManager
from django.contrib.auth import get_user_model
from groups.models import *


class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('mentor', 'Mentor')
    )

    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)

    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    photo = models.ImageField(upload_to='user_photos/', null=True, blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


class ExtendedUser(CustomUser):
    people = PeopleManager()

    class Meta:
        proxy = True
        ordering = ('first_name',)

    def some_action(self):
        print(self.username)


class UserProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    phone_number = models.CharField(
        null=True, max_length=14, unique=True,
        blank=True, validators=[RegexValidator("\d{10,14}")]
    )
    birthdate = models.DateField(null=True, blank=True, default=datetime.date.today, validators=[older_than_18])
    avatar = models.ImageField(upload_to='avatar', null=True, blank=True)
    resume = models.FileField(upload_to='resume', null=True, blank=True)
    course = models.ForeignKey("groups.Course", null=True, blank=True, related_name="user_course",
                               on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.user.first_name}_{self.user.last_name}"


class Person(models.Model):
    first_name = models.CharField(
        max_length=60, null=False, validators=[MinLengthValidator(2)]
    )
    last_name = models.CharField(
        max_length=80, null=False, validators=[MinLengthValidator(2)]
    )
    email = models.EmailField(max_length=120, null=True, validators=[no_elon_validator])
    phone_number = PhoneNumberField(unique=True, null=True)

    class Meta:
        abstract = True


class Student(Person):
    birthdate = models.DateField(null=True, default=datetime.date.today)

    avatar = models.ImageField(upload_to='media', null=True,
                               blank=True)
    resume = models.FileField(upload_to='static', null=True,
                              blank=True)

    course = models.ForeignKey(
        "groups.Course", null=True, related_name="students",
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return f"{self.full_name()}, {self.age()}, {self.email} ({self.id}) {self.avatar}" \
               f"{self.resume}"

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def age(self):
        return datetime.datetime.now().year - self.birthdate.year

    @classmethod
    def generate_instances(cls, count):
        faker = Faker()
        for _ in range(count):
            st = cls(
                first_name=faker.first_name(),
                last_name=faker.last_name(),
                email=faker.email(),
                birthdate=faker.date_time_between(start_date="-30y", end_date="-18y"),
            )
            st.save()


class Invite(models.Model):
    id = models.UUIDField(
        primary_key=True, unique=True, default=uuid.uuid4, editable=False
    )
    inviter_student = models.ForeignKey("students.Student", null=True, on_delete=models.SET_NULL)
    course = models.ForeignKey("groups.Course", null=True, on_delete=models.SET_NULL)
    invited_st_first_name = models.CharField(
        max_length=100, null=False, validators=[MinLengthValidator(2)]
    )
    invited_st_last_name = models.CharField(
        max_length=100, null=False, validators=[MinLengthValidator(2)]
    )
    count_invites = models.IntegerField(default=0)