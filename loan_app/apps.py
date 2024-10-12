from django.apps import AppConfig


class LoanAppConfig(AppConfig):
    name = 'loan_app'

    def ready(self):
        import loan_app.signals
