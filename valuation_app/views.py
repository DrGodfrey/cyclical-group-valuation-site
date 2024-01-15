from django.shortcuts import render
from django.http import HttpResponse

from .models import Company, CircularOwnership, Company_model, retrieve_price_or_update
from .stock_tracker_av import *





# USES ALPHAVANTAGE API TO FETCH UP TO DATE SHAREPRICES:

bollore_shareprice = retrieve_price_or_update(ticker='BOL.PA')
umg_shareprice = retrieve_price_or_update(ticker='UMG.AMS')
odet_shareprice = retrieve_price_or_update(ticker='ODET.PA')
vivendi_shareprice = retrieve_price_or_update(ticker='VIV.PA')



# Bollore 'galaxy'
bollore = Company('Bolloré SE', shares_outstanding=(2902650243 - 99.1 * 10 ** 6) , shareprice=bollore_shareprice)
umg = Company('Universal Music Group', shares_outstanding=1.81 * 10 ** 9, shareprice=umg_shareprice)
odet = Company("Compagnie de l'Odet", shares_outstanding=6590000, shareprice=odet_shareprice)
vivendi = Company("Vivendi", shares_outstanding=1139051437, shareprice=vivendi_shareprice)

# Naspers/Prosus (legacy - crossholding has since been simplified)
tencent = Company("Tencent", shares_outstanding=9541000000, shareprice=38.72, currency='€')
prosus = Company("Prosus", shares_outstanding = 2003 * 10 ** 6, shareprice=66.93, currency='€')
naspers = Company("Naspers", shares_outstanding = 410 * 10 ** 6, shareprice=158.5, currency='€')

# Asign Assets
bollore.asign_asset(asset=umg, is_company_object=True, ownership_fraction=0.1810) # was 17.7%, cash flow statement implies they've been buying
odet.asign_asset(asset=umg, is_company_object=True, ownership_fraction=0.0033)
bollore.asign_asset(asset=vivendi, is_company_object=True, ownership_fraction=0.29)
odet.asign_asset(asset=vivendi, is_company_object=True, ownership_fraction=0.005)
bollore.asign_asset('Cash', (1.415*10**9)) #source - 'liquidity'
bollore.asign_asset('Expected proceeds from sale of Bolloré logistics', 4.65*10**9) # 4.65B euros, prior to net cash/debt

prosus.asign_asset(asset=tencent, is_company_object=True, ownership_fraction=0.259)
prosus.asign_asset('Meituan', 3.37*10**9)
prosus.asign_asset('Delivery Hero', 2.53*10**9)
prosus.asign_asset('Other listed assets', 1.97*10**9)
prosus.asign_asset('Unlisted Assets', 23.8*10**9)
prosus.asign_asset('Net Cash', 0.37*10**9)

naspers.asign_asset('Naspers assets outside of Prosus', 1.12*10**9)

bollore_odet_group = CircularOwnership(company_1=bollore, company_1_outside_ownership=0.292, company_2=odet, company_2_outside_ownership=0.16)
# source: https://www.bollore.com/bollo-content/uploads/2023/07/2023-07-28-bol-resultats-h1-2023-uk-v5.pdf
prosus_naspers_group = CircularOwnership(company_1=prosus, company_1_outside_ownership=0.38, company_2=naspers, company_2_outside_ownership=0.47)

def load_index(request):
    company_model = Company_model.objects.all()
    return render(request, 'valuation_app/index.html', {
        'cyclical_groups': [bollore_odet_group, prosus_naspers_group],
        'company_model': company_model
    })
