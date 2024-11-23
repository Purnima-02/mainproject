from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from django.urls import reverse

class EmployeeLoginMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Only apply this middleware to URLs that start with 'emp'
        if request.path.startswith('/emp/'):
            # Check if the user is authenticated by verifying if 'employee_id' exists in the session
            is_authenticated = request.session.get('employee_id') is not None

            # If the user is not authenticated, redirect them to the login page
            if not is_authenticated:
                if request.path != reverse('login_check'):  # Assuming 'login_check' is the URL name for 'login/check/'
                    return redirect(reverse('login_check'))
            
            # If the user is authenticated and tries to access the login page, redirect to the dashboard
            if is_authenticated and request.path == reverse('login_check'):
                return redirect(reverse('all_loans'))  # Assuming 'all_loans' is the URL name for the dashboard
