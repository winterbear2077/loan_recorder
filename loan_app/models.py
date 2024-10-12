from django.db import models
from django.utils import timezone
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE_CASCADE
import uuid


class BaseP(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=255)
    contact_info = models.CharField(max_length=255, blank=True)
    create_at = models.DateTimeField(default=timezone.now)
    is_valid = models.BooleanField(default=True)
    avatar = models.CharField(default="https://litchi-beer.oss-cn-shanghai.aliyuncs.com/avatar.jpg", max_length=255)


    def get_id(self):
        return str(self.id)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
        ordering = ['name', 'create_at']
        indexes = [
            models.Index(fields=['name'])
        ]


class User(BaseP):
    is_lender = models.BooleanField(default=False)
    is_borrower = models.BooleanField(default=False)


class Lender(BaseP):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='lender')


class Borrower(BaseP):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='borrower')


class DebtRecords(SafeDeleteModel):
    STATUS = {
        'PENDING': 'PENDING',
        'PAID': 'PAID',
        'OVERDUE': 'OVERDUE'
    }
    _safedelete_policy = SOFT_DELETE_CASCADE

    lender = models.ForeignKey(Lender, related_name='debt_lender', on_delete=models.CASCADE)
    borrower = models.ForeignKey(Borrower, related_name='debt_borrower', on_delete=models.CASCADE)
    principal = models.DecimalField(default=0, max_digits=12, decimal_places=4)
    interest_rate = models.DecimalField(default=0, max_digits=12, decimal_places=4)
    due_date = models.DateTimeField()
    status = models.CharField(max_length=8, choices=STATUS, default='PENDING')
    created_at = models.DateTimeField(default=timezone.now)
    update_at = models.DateTimeField(default=timezone.now)
    is_valid = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.principal}/{self.interest_rate}"


class RepaymentRecords(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    debt_id = models.ForeignKey(DebtRecords, related_name='repayment', on_delete=models.CASCADE),
    repayment_date = models.DateTimeField(),
    amount = models.DecimalField(max_digits=12, decimal_places=4)
    principal_paid = models.DecimalField(max_digits=12, decimal_places=4)
    interest_paid = models.DecimalField(max_digits=12, decimal_places=4)
    created_at = models.DateTimeField(default=timezone.now)
    is_valid = models.BooleanField(default=True)

    def __str__(self):
        return f"Debt ID: {self.debt_id}, Repayment Date: {self.repayment_date}, Amount: {self.amount}"
