from django.contrib import admin
from django.urls import path
from Admin import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    #path for login module
    path('login/', views.login),
    path('logout/',views.logout),
    #path to homepage
    path('',views.home),
    #path to student module
    path('add_student/',views.add_student,name='addStudent'),
    path('edit_student/<int:id>',views.edit_student,name='editStudent'),
    path('delete_student/<int:id>',views.deleteStudent,name='deleteStudent'),
    # paths related to courses
    path('course/',views.Course,name='course'),
    path('addType/<int:id>',views.addType),
    path('remType/<int:id>/<int:id1>',views.remType),
    path('addDept/<int:id>',views.addDept),
    path('remDeps/<int:id>/<int:id1>',views.remDeps),
    path('edit_course/<int:id>',views.editCourse,name='editCourse'),
    path('delete_course/<int:id>',views.deleteCourse,name='deleteCourse'),
    #path for additional details
    path('coursead/',views.coursead),
    path('editCoursead/<int:id>',views.editCoursead),
    path('deleteCoursead/<int:id>',views.deleteCoursead),
    #path for adding seats
    path('addSeats/',views.seatAllocate,name='addSeats'),
    path('edit_seats/<int:id>',views.editSeat,name="editSeats"),
    path('delete_seats/<int:id>',views.deleteSeat,name='deleteSeats'),
    #path for reports
    path('live-report/',views.liveReport),
    path('live-report-ind/<int:id>',views.liveReportInd),
    #path for site settings
    path('site-settings/',views.siteSet,name='siteSettings'),
    #path for forget password
    path('forgetPass/',views.forgetPass),
    path('verifyOtp/',views.verifyOtp),
    path('changePass/',views.changePass),
    path('changePass1/',views.changePass1),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)