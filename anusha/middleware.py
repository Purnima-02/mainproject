
from anusha.forms import BasicDetailForm,goldBasicDetailForm,OtherBasicDetailForm
from django.shortcuts import render



class LapAuthMiddleware:
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
       
        
        if request.path.startswith('/lapapply/') and not request.session.get('lap_id'):
            
            form = BasicDetailForm()
            request.session['lap_return_url'] = request.build_absolute_uri()
            return render(request, 'customer/basicdetailform.html', {'form': form})
        
        elif request.path.startswith('/goldloan/') and not request.session.get('gold_id'):
           
            form = goldBasicDetailForm()
            request.session['gold_return_url'] = request.build_absolute_uri()
            return render(request, 'customer/goldbasicdetail.html', {'form': form})
        
        elif request.path.startswith('/otherloan/') and not request.session.get('other_id'):
            
            form = OtherBasicDetailForm()
            request.session['other_return_url'] = request.build_absolute_uri()
            return render(request, 'customer/otherbasicdetail.html', {'form': form})
            
        else:
    
           
            return self.get_response(request)
