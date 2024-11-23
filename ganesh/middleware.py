from django.shortcuts import redirect

class ApplicationStepMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        valid_paths = {
            'crebasicdetail': '/crebasicdetail/',
            'credit': '/credit/',
            'document_detail': '/document_detail/',
            'success': '/success/',
        }

        if request.path.startswith('/ccapply/'):
            step = request.session.get('application_step', 'crebasicdetail')
            expected_path = valid_paths.get(step, '/crebasicdetail/')

            if not request.path.startswith(expected_path):
                if step == 'crebasicdetail':
                    return redirect('crebasicdetail')
                elif step == 'credit':
                    return redirect('credit')
                elif step == 'document_detail':
                    application_id = request.session.get('application_id', '')
                    return redirect('document_detail', application_id=application_id)
                elif step == 'success':
                    application_id = request.session.get('application_id', '')
                    return redirect('success')  # Ensure 'success' URL is defined

        response = self.get_response(request)
        return response




