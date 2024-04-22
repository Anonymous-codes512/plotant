from django.db import models
from account.models import User
from django.contrib.postgres.fields import JSONField 

class Working(models.Model):
    filename = models.CharField(max_length=255)
    date = models.DateTimeField()

    
class Project(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    modified_date = models.DateTimeField(null=True, blank=True)



class File(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    date = models.DateTimeField()
    modified_date = models.DateTimeField(null=True, blank=True)



class Trash(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.CharField(max_length=255)
    filename = models.CharField(max_length=255, null=True, blank=True)
    projectcreatedate = models.DateTimeField()
    filecreatedate = models.CharField(max_length=255, null=True, blank=True)
    modifydate = models.CharField(max_length=255, null=True, blank=True)
    date = models.DateTimeField()


class SharedProject(models.Model):
    name = models.CharField(max_length=255)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_shared_projects')
    sharedWith = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shared_projects')
    date = models.DateTimeField()

    
class Associate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='associated_projects')
    role = models.CharField(max_length=255)
    date = models.DateTimeField()

class Archived(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='archived_projects')
    role = models.CharField(max_length=255)
    date = models.DateTimeField()



# class Result(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_results')
#     algorithm = models.ForeignKey('Algorithm', on_delete=models.CASCADE, related_name='algorithm_results')
#     resultPath = models.CharField(max_length=255)
#     date = models.DateTimeField()
    
