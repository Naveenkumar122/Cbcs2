from django.contrib import admin
from django.urls import path
from Admin import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login),
    #path to student module
    path('add_student/',views.add_student,name='addStudent'),
    path('edit_student/',views.edit_student,name='editStudent'),
    path('update_student/',views.updateStudent,name='upadateStudent'),
    path('delete_student/<int:id>',views.deleteStudent,name='deleteStudent'),
    # paths related to courses
    path('course/',views.Course,name='course'),
    path('edit_course/<int:id>',views.editCourse,name='editCourse'),
    path('delete_course/<int:id>',views.deleteCourse,name='deleteCourse'),
    path('search-course/',views.searchCourse,name='searchCourse'),
    #path for adding seats
    path('addSeats/',views.seatAllocate,name='addSeats'),
    path('edit_seats/<int:id>',views.editSeat,name="editSeats"),
    path('delete_seats/<int:id>',views.deleteSeat,name='deleteSeats'),
    path('search-seats/',views.searchSeat,name='searchSeats'),
    #path for reports
    path('live-report/',views.liveReport),
    path('live-report-ind/<int:id>',views.liveReportInd),
    #path for site settings
    path('site-settings/',views.siteSet,name='siteSettings')
]
