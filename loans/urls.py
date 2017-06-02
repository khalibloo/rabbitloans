from loans.views import LoanViewSet, UserViewSet, MeViewSet, api_root
from rest_framework import renderers

loan_list = LoanViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
loan_detail = LoanViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
#loan_highlight = LoanViewSet.as_view({
#    'get': 'highlight'
#}, renderer_classes=[renderers.StaticHTMLRenderer])
user_list = UserViewSet.as_view({
    'get': 'list',
    'post': 'create',
})
user_detail = UserViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
me_detail = MeViewSet.as_view({
    'get': 'retrieve'
})
