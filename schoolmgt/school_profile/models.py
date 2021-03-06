# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
 
class SubjectDetails(models.Model):
    subject_name = models.CharField(max_length=80, blank=True, null=True)
    subject_code = models.CharField(max_length=15, blank=True, unique=True)
    
    def __unicode__(self):
       return self.subject_name
    
    class Meta:
        db_table = 'subject_details'
        ordering = ['id']
        indexes = [
            models.Index(fields=['subject_code'],name='subject_details_idx1'),
        ]
                
class StudentDetails(models.Model):
    student_name = models.CharField(max_length=50, blank=True, null=True)
    student_dob = models.DateField(null=True)
    student_phone_number = models.CharField(max_length=10, null=True,blank=True)
    student_address = models.TextField(null=True,blank=True)
   # student_subject = models.ForeignKey(SubjectDetails, related_name='student_subject_code', on_delete=models.CASCADE)
    student_pass_fail = models.BooleanField(default=False)
    student_total = models.IntegerField(null=True, blank=True)
    student_rank = models.IntegerField(null=True, blank=True)
    
    def __unicode__(self):
       return self.student_name
    
    class Meta:
        db_table = 'student_details'
        ordering = ['id']
        indexes = [
            models.Index(fields=['student_name'],name='student_details_idx1'),
        ]
        
class TeacherDetails(models.Model):
    teacher_name = models.ForeignKey(User, related_name='teacher_name', on_delete=models.CASCADE)
    teacher_subject = models.ForeignKey(SubjectDetails, related_name='teacher_subject_code', on_delete=models.CASCADE)
    teacher_address = models.TextField()
    
    class Meta:
        db_table = 'teacher_details'
        ordering = ['id']
        indexes = [
            models.Index(fields=['teacher_name'],name='teacher_details_idx1'),
        ]
        

        
class MarkDetails(models.Model):
    student_id = models.ForeignKey(StudentDetails, related_name='student_id', on_delete=models.CASCADE)
    subject_id = models.ForeignKey(SubjectDetails, related_name='subject_id', on_delete=models.CASCADE)
    mark = models.IntegerField(null=False)
    
    def __unicode__(self):
       return str(self.mark)
   
    class Meta:
        db_table = 'mark_details'
        ordering = ['id']
        indexes = [
            models.Index(fields=['mark'],name='mark_details_idx1'),
        ]
        
    