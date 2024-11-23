# yourapp/middleware.py

from django.shortcuts import render

from anusha.forms import BasicDetailForm, OtherBasicDetailForm, goldBasicDetailForm
from anusha.models import basicdetailform
from bhanu.forms import eduBasicDetailForm
from business.forms import busBasicDetailForm
from ganesh.forms import creditBasicDetailForm
from ravi.forms import HomeBasicDetailForm, plBasicDetailForm
from seetha.forms import CLBasicDetailForm
from datetime import date, datetime


class XFrameOptionsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
       
        response['X-Frame-Options'] = 'SAMEORIGIN'  # or 'ALLOW-FROM http://example.com'
        return response



class AuthMiddleware:
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
       
       
        if request.GET.get('refCode') or request.GET.get('franrefCode'):
            request.session['frmDSAFranch']="Access"
        else:
            if request.session.get('frmDSAFranch'):
                del request.session['frmDSAFranch']
            self.clearSessionsAfter3months(request)
        
        if request.path.startswith('/el/apply-educationalLoan') and not request.session.get('eduAppliId') and not request.session.get('frmDSAFranch'):
          
            form = eduBasicDetailForm()
            request.session['eduUrl']=request.build_absolute_uri()
            return render(request,'ebasicdetail.html',{'form':form})
        
        elif request.path.startswith('/bl/demo') and not request.session.get('busiAppliId') and not request.session.get('frmDSAFranch'):
           
            form = busBasicDetailForm()
            request.session['busiUrl']=request.build_absolute_uri()
            return render(request,'busbasicdetail.html',{'form':form})
       
        elif request.path.startswith('/lapapply/') and not request.session.get('lapAppliId') and not request.session.get('frmDSAFranch'):
           
            form = BasicDetailForm()
           
            return render(request,'customer/basicdetailform.html',{'form':form})
        
        elif request.path.startswith('/goldloan/') and not request.session.get('goldAppliId') and not request.session.get('frmDSAFranch'):
           
            form = goldBasicDetailForm()
           
            return render(request,'customer/goldbasicdetail.html',{'form':form})
            
                
        elif request.path.startswith('/cl/car-loan-application/') and not request.session.get('carAppliId') and not request.session.get('frmDSAFranch'):
          
            form = CLBasicDetailForm() # request.session['busiUrl']=request.build_absolute_uri()
            return render(request,'carbasicdetailform.html',{'form':form})
        
        
        elif request.path.startswith('/pl/personal/') and not request.session.get('plAppliId') and not request.session.get('frmDSAFranch'):
           
            form = plBasicDetailForm()
            # request.session['busiUrl']=request.build_absolute_uri()
            return render(request,'admin/basic.html',{'form':form})
        
        
        elif request.path.startswith('/cc/credit/') and not request.session.get('ccAppliId') and not request.session.get('frmDSAFranch'):
           
            form = creditBasicDetailForm()
            
            return render(request,'credbasicdetail.html',{'form':form})
        
           
        elif request.path.startswith('/otherloan/') and not request.session.get('otherAppliId') and not request.session.get('frmDSAFranch'):
           
            form = OtherBasicDetailForm()
          
            return render(request,'customer/otherbasicdetail.html',{'form':form})
        
        elif request.path.startswith('/pl/home/') and not request.session.get('hmAppliId') and not request.session.get('frmDSAFranch'):
           
            form = HomeBasicDetailForm()
            
            return render(request,'admin/hlbasic.html',{'form':form})
        else:
         
            return self.get_response(request)
    
    def clearSessionsAfter3months(self,request):
        if request.session.get('BusinessLoanExpiryDate'):
            exiparydate=datetime.strptime(request.session.get('BusinessLoanExpiryDate'), '%Y-%m-%d')
        
            if datetime.today() > exiparydate: request.session.pop('busiAppliId', None)
            
        if request.session.get('CarLoanExpiryDate'):
            exiparydate=datetime.strptime(request.session.get('CarLoanExpiryDate'), '%Y-%m-%d')
            if datetime.today() > exiparydate: request.session.pop('carAppliId', None)
        
        if request.session.get('EducationLoanExpiryDate'):
            exiparydate=datetime.strptime(request.session.get('EducationLoanExpiryDate'), '%Y-%m-%d')
            if datetime.today() > exiparydate: request.session.pop('eduAppliId', None)
        
        if request.session.get('LAPLoanExpiryDate'):
            exiparydate=datetime.strptime(request.session.get('LAPLoanExpiryDate'), '%Y-%m-%d')
            if datetime.today() > exiparydate: request.session.pop('lapAppliId', None)
        
        if request.session.get('OtherLoanExpiryDate'):
            exiparydate=datetime.strptime(request.session.get('OtherLoanExpiryDate'), '%Y-%m-%d')
            if datetime.today() > exiparydate: request.session.pop('otherAppliId', None)
        
        if request.session.get('GoldLoanExpiryDate'):
            exiparydate=datetime.strptime(request.session.get('GoldLoanExpiryDate'), '%Y-%m-%d')
            if datetime.today() > exiparydate: request.session.pop('goldAppliId', None)
        
        if request.session.get('HLoanExpiryDate'):
            exiparydate=datetime.strptime(request.session.get('HLoanExpiryDate'), '%Y-%m-%d')
            if datetime.today() > exiparydate: request.session.pop('hmAppliId', None)
        
        if request.session.get('PLoanExpiryDate'):
            exiparydate=datetime.strptime(request.session.get('PLoanExpiryDate'), '%Y-%m-%d')
            if datetime.today() > exiparydate: request.session.pop('plAppliId', None)
        
        
        if request.session.get('CrditCardLoanExpiryDate'):
            exiparydate=datetime.strptime(request.session.get('CrditCardLoanExpiryDate'), '%Y-%m-%d')
            if datetime.today() > exiparydate: request.session.pop('ccAppliId', None)
        
        