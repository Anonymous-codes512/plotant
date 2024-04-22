from django.urls import path
from . import visitor_views, user_views

urlpatterns = [
    path('getdata', visitor_views.analyse),
    path('getlabels', visitor_views.labels),
    path('getlegends', visitor_views.labels_legends),
    path('test', visitor_views.convertEPS),

    # Registered Users Routes
    path('getData', user_views.analyse),
    path('getLabels', user_views.labels),
    path('getLegends', user_views.labels_legends),
    path('projectCreate', user_views.createProject),
    path('projectsCount', user_views.projectCount),
    path('projectsList', user_views.projectList),
    path('yourProjects', user_views.yourProjects),
    path('projectDelete', user_views.projectDelete),
    path('shareProject', user_views.shareProject),
    path('sharedProjects', user_views.sharedProjects),
    path('archiveProject', user_views.archiveProject),
    path('unArchive', user_views.unArchive),
    path('archivedProjects', user_views.archivedProjects),
    path('fileDelete', user_views.fileDelete),
    path('fileRename', user_views.fileRename),
    path('projectGraphCount', user_views.projectGraphCount),
    path('fileDownload', user_views.download_project_file),
    path('saveFile', user_views.saveFile),
    path('openProject', user_views.projectOpen),
    path('trashedProjectsList', user_views.trashedProject),
    path('projectRestore', user_views.projectRestore),
]