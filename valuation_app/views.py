from django.shortcuts import render
from django.http import HttpResponse

from .models import Company, CircularOwnership, Company_model
# Create your views here

bollore = Company('Bolloré SE', shares_outstanding=2902650243, shareprice=6.00)
umg = Company('Universal Music Group', shares_outstanding=1.81 * 10 ** 9, shareprice=18.78)
odet = Company("Compagnie de l'Odet", shares_outstanding=6590000, shareprice=1512)
vivendi = Company("Vivendi", shares_outstanding=1139051437, shareprice=8.45)
cgeo = Company("Georgia Capital", shares_outstanding = 44.09 * 10 ** 6, shareprice=8.49, currency="£")
tencent = Company("Tencent", shares_outstanding=9541000000, shareprice=36.90, currency='€')

prosus = Company("Prosus", shares_outstanding = 2003 * 10 ** 6, shareprice=62.10, currency='€')
naspers = Company("Naspers", shares_outstanding = 410 * 10 ** 6, shareprice=141.41, currency='€')

# Asign Assets
bollore.asign_asset(asset=umg, is_company_object=True, ownership_fraction=0.177)
odet.asign_asset(asset=umg, is_company_object=True, ownership_fraction=0.005)
bollore.asign_asset(asset=vivendi, is_company_object=True, ownership_fraction=0.289)
odet.asign_asset(asset=vivendi, is_company_object=True, ownership_fraction=0.005)
bollore.asign_asset('Cash', 2*10**9)
bollore.asign_asset('Expected proceeds from sale of Bolloré logistics', 4*10**9)

prosus.asign_asset(asset=tencent, is_company_object=True, ownership_fraction=0.259)
prosus.asign_asset('Meituan', 3.37*10**9)
prosus.asign_asset('Delivery Hero', 2.53*10**9)
prosus.asign_asset('Other listed assets', 1.97*10**9)
prosus.asign_asset('Unlisted Assets', 23.8*10**9)
prosus.asign_asset('Net Cash', 0.37*10**9)

naspers.asign_asset('Naspers assets outside of Prosus', 1.12*10**9)

bollore_odet_group = CircularOwnership(company_1=bollore, company_1_outside_ownership=0.33, company_2=odet, company_2_outside_ownership=0.16)
prosus_naspers_group = CircularOwnership(company_1=prosus, company_1_outside_ownership=0.38, company_2=naspers, company_2_outside_ownership=0.47)

def load_index(request):
    company_model = Company_model.objects.all()
    return render(request, 'valuation_app/index.html', {
        'cyclical_groups': [bollore_odet_group, prosus_naspers_group],
        'company_model': company_model
    })
