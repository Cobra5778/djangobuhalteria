from django.conf.urls import url
from . import views

urlpatterns = [
    # ex: /buhalteriya/
    url(r'^$', views.wellcome, name='wellcomeb'),
    # ex: /buhalteriya/wellcome/
    url(r'^wellcome/$', views.wellcome, name='wellcomeb'),
    # ex: /buhalteriya/TTK/
    url(r'^TTK/$', views.TTK_main, name='TTK_main'),
    # ex: /buhalteriya/my_downloadfile/
    url(r'^my_downloadfile/$', views.my_downloadfile, name='my_downloadfile'),
    # ex: /buhalteriya/export_TTK_to_xlsm/
    url(r'^export_TTK_to_xlsm/$', views.export_TTK_to_xlsm, name='export_TTK_to_xlsm'),
    # ex: /buhalteriya/TTKakt/
    url(r'^TTKakt/$', views.TTKakt, name='TTKakt'),
    # ex: /buhalteriya/nav_mounth/
    url(r'^nav_mounth/$', views.nav_mounth, name='buh_nav_mounth'),
    # ex: /buhalteriya/Summ_Stoim_TTK/
    url(r'^Summ_Stoim_TTK/$', views.Summ_Stoim_TTK, name='Summ_Stoim_TTK'),
    # ex: /buhalteriya/downloadCSV_TTK/
    url(r'^downloadCSV_TTK/$', views.downloadCSV_TTK, name='downloadCSV_TTK'),
    # ex: /buhalteriya/RTK/
    url(r'^RTK/$', views.RTK_main, name='RTK_main'),
    # ex: /buhalteriya/RTKsumm/
    url(r'^RTKsumm/$', views.RTKsumm, name='RTKsumm'),
    # ex: /buhalteriya/export_RTK_to_xlsx/
    url(r'^export_RTK_to_xlsx/$', views.export_RTK_to_xlsx, name='export_RTK_to_xlsx'),
    # ex: /buhalteriya/nav_mounth_TTK/
    url(r'^nav_mounth_TTK/$', views.nav_mounth_TTK, name='nav_mounth_TTK'),
    # ex: /buhalteriya/Summ_Stoim_RTK/
    url(r'^Summ_Stoim_RTK/$', views.Summ_Stoim_RTK, name='Summ_Stoim_RTK'),
    # ex: /buhalteriya/ballansy/.
    url(r'^ballansy/$', views.ballansy, name='ballansy'),
    # ex: /buhalteriya/ballansy_uriki/.
    url(r'^ballansy_uriki/$', views.ballansy_uriki, name='ballansy_uriki'),
    # ex: /buhalteriya/nav_ballansy/
    url(r'^nav_ballansy/$', views.nav_ballansy, name='nav_ballansy'),
    # ex: /buhalteriya/ballansy_fiziki/
    url(r'^ballansy_fiziki/$', views.ballansy_fiziki, name='ballansy_fiziki'),
    # ex: /buhalteriya/export_ballanse_xlsx/
    url(r'^export_ballanse_xlsx/$', views.export_ballanse_xlsx, name='export_ballanse_xlsx'),
    # ex: /buhalteriya/compare_sf/
    url(r'^compare_sf/$', views.compare_sf, name='compare_sf'),
    # ex: /buhalteriya/sf_result/
    url(r'^sf_result/$', views.sf_result, name='sf_result'),
]
