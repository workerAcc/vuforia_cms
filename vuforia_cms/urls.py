from django.conf.urls import patterns, include, url
from django.contrib import admin

from django.conf import settings

from cms import receivers

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'vuforia_cms.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'cms.views.session.login_view', name='login'),
    url(r'^logout$', 'cms.views.session.logout_view', name='logout'),

    url(r'^account/list$', 'cms.views.account.list',
        name='account_list'),
    url(r'^account/new$', 'cms.views.account.new',
        name='account_new'),
    url(r'^account/edit/(?P<acctypeid>\d+)/(?P<userid>\d+)$',
        'cms.views.account.edit', name='account_edit'),
    url(r'^account/edit_pw/(?P<acctypeid>\d+)/(?P<userid>\d+)$',
        'cms.views.account.edit_pw', name='account_edit_pw'),
    url(r'^account/edit_status/(?P<acctypeid>\d+)/(?P<userid>\d+)$',
        'cms.views.account.edit_status', name='account_edit_status'),

    url(r'^content/list$', 'cms.views.content.list',
        name='content_list'),
    url(r'^content/new/(?P<contractno>\d+)$', 'cms.views.content.new',
        name='content_new'),
    url(r'^content/edit/(?P<contractno>\d+)$', 'cms.views.content.edit',
        name='content_edit'),

    url(r'^content/edit_open/(?P<contractno>\d+)$',
        'cms.views.content.edit_open', name='content_edit_open'),

    url(r'^contract/new/(?P<companyid>\d+)$', 'cms.views.contract.new',
        name='contract_new'),
    url(r'^contract/edit/(?P<contractno>\d+)$', 'cms.views.contract.edit',
        name='contract_edit'),

    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$','django.views.static.serve',
           {'document_root': settings.MEDIA_ROOT}),
    )

