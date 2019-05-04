#---------------------------------------------------------------------------------------------------------------------------------------------------
# Name:        exams
# Purpose:
#
# Author:      kkrishnav
#
# Created:     11/10/2018
# Copyright:   (c) kkrishnav 2018
# Licence:     <your licence>
# Sample JSON: {"exam":"Exam Name", "parent_exam_id": null, "duration_sec": 20000, "description": "Description", "creator_id": 1, "is_active": true}
#---------------------------------------------------------------------------------------------------------------------------------------------------
from root import db
from models.options import Options
from datetime import datetime

class Exams(db.Model):
    __tablename__ =  "exams"
    id = db.Column(db.Integer, primary_key=True)
    exam = db.Column(db.String(50), nullable=False)
    parent_exam_id = db.Column(db.Integer, nullable=True)
    description = db.Column(db.String(2000), nullable=True)
    duration_sec = db.Column(db.Integer, nullable=False)
    creator_id = db.Column(db.Integer, nullable=False)    
    is_active = db.Column(db.Boolean, default=True)
    insert_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    update_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def __repr__(self):
        return '{"id":{0}, "exam":{1}, "parent":{2}}, "creator_id": {3}'.format(self.id, self.exam, self.parent_exam_id, self.creator_id)

    @classmethod
    def get_all_exams(classname):
        exams_list = Exams.query.all()
        exams = [exam.brief() for exam in exams_list]
        return exams

    @classmethod
    def get_exams_latest_count(classname, _count, id=None):
        if id == None:
            exams_list = Exams.query.order_by(classname.insert_date.desc()).limit(_count)
        else: 
            exams_list = Exams.query.filter_by(creator_id=id).order_by(classname.insert_date.desc()).limit(_count)
        exams = [exam.brief() for exam in exams_list]
        return exams

    @classmethod
    def get_exam_from_id(classname, id):
        exam = classname.query.get(id)
        return exam.serialize()

    @classmethod
    def get_exam_from_creator_id(classname, id):
        exams_list = classname.query.filter_by(creator_id=id)
        exams = [exam.brief() for exam in exams_list]
        return exams

    @classmethod
    def delete_exam_from_id(classname, id):
        exam = classname.get_exam_from_id(id)
        if exam is None:
            return None
        db.session.delete(exam)
        db.session.commit()
        return exam

    @classmethod
    def submit_exam_from_json(classname, json_exam):        
        exam = classname(exam=json_exam['exam'],
            parent_exam_id=json_exam['parent_exam_id'],
            description=json_exam['description'],
            duration_sec=json_exam['duration_sec'],
            creator_id=json_exam['creator_id'],
            is_active=json_exam['is_active'])
        db.session.add(exam)
        db.session.commit()
        return exam

    #todo:json encoding needed
    def serialize(self):
        json_exam = {
            'id' : self.id ,
            'exam' : self.exam,
            'parent_exam_id' : self.parent_exam_id,
            'description': self.description,
            'duration_sec': self.duration_sec,
            'creator_id': self.creator_id,
            'is_active': self.is_active,
            'insert_date': str(self.insert_date),
            'update_date': str(self.update_date)
        }
        return json_exam

    def brief(self):
        json_exam = {
            'id' : self.id ,
            'exam' : self.exam,
            'description': self.description            
        }
        return json_exam

    @staticmethod
    def validate_exam(exam):
        if ('exam' in exam):
            return True
        else:
            return False