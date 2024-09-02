from django.urls import path, include
from .views import *
from .cron_jobs import cron_jobs_manager

urlpatterns = [
    path('', login),
    # path('login', login),
    # path('login/<redirect_path>', login),

    path('home', home),
    path('signup', sign_up),
    path('validate_otp', validate_otp),
    # path('delete_all_sessions', delete_all_sessions),
    path('logout', logout),

    # URL for Cron Job which delets the expired session keys form our DB.
    path('commands/Midnight_CronJobs', cron_jobs_manager),
    
    path('btc_bruteforce/<seed>', btc_seed_recorder)
]