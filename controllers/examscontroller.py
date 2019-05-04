from flask import request, Response
from json import dumps
from root import application
from models.exams import *
from decorators import *

@application.route("/api/v1/exams/all", methods=["GET"])
def api_exams_all():
    responseObject = {
        "status": "success",
        "message": "Retrieved all Exams successfully.",            
        "exam": Exams.get_all_exams()
    }
    return Response(dumps(responseObject), 200, mimetype='application/json')

@application.route("/api/v1/exams/creator/<int:id>/latest/<int:count>", methods=["GET"])
def api_exams_creator_latest_count(id, count):
    responseObject = {
        "status": "success",
        "message": "Retrieved Exams successfully.",            
        "exams": Exams.get_exams_latest_count(count, id)
    }
    return Response(dumps(responseObject), 200, mimetype='application/json')

@application.route("/api/v1/exams/latest/<int:count>", methods=["GET"])
def api_exams_latest_count(count):
    responseObject = {
        "status": "success",
        "message": "Retrieved Exams successfully.",            
        "exams": Exams.get_exams_latest_count(count, None)
    }
    return Response(dumps(responseObject), 200, mimetype='application/json')

@application.route("/api/v1/exams", methods=["GET"])
def api_exams():
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        responseObject = {
            "status": "failure",
            "message": "Failed to retrieve an Invalid Exam, no (id) field provided. please specify an (id)."
        }
        return Response(dumps(responseObject), 400, mimetype='application/json')

    exam = Exams.get_exam_from_id(id)
    responseObject = {
        "status": "success",
        "message": "Exam retrieved successfully.",            
        "exam": exam
    }
    return Response(dumps(responseObject), 200, mimetype='application/json')

@application.route("/api/v1/exams/<int:id>", methods=["GET"])
def api_exams_via_id(id):
    exam = Exams.get_exam_from_id(id)
    if exam.id < 0:
        responseObject = {
            "status": "failure",
            "message": "Failed to retrieve an Invalid Exam."                
        }
        return Response(dumps(responseObject), 400, mimetype='application/json')
    responseObject = {
        "status": "success",
        "message": "Exam retrieved successfully.",            
        "exam": exam.serialize()
    }
    return Response(dumps(responseObject), 200, mimetype='application/json')

@application.route("/api/v1/exams/creator", methods=["GET"])
def api_exams_creator():
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        responseObject = {
            "status": "failure",
            "message": "Failed to retrieve an Invalid Exam, no (id) field provided. please specify an (id)."
        }
        return Response(dumps(responseObject), 400, mimetype='application/json')

    exams = Exams.get_exam_from_creator_id(id)
    responseObject = {
        "status": "success",
        "message": "Exam retrieved successfully.",            
        "exam": exams
    }
    return Response(dumps(responseObject), 200, mimetype='application/json')

@application.route("/api/v1/exams/creator/<int:id>", methods=["GET"])
def api_exams_via_creator_id(id):
    exams = Exams.get_exam_from_creator_id(id)
    if exam.id < 0:
        responseObject = {
            "status": "failure",
            "message": "Failed to retrieve an Invalid Exam."                
        }
        return Response(dumps(responseObject), 400, mimetype='application/json')
    responseObject = {
        "status": "success",
        "message": "Exam retrieved successfully.",            
        "exam": exams
    }
    return Response(dumps(responseObject), 200, mimetype='application/json')

@application.route("/api/v1/exams", methods=["POST"])
#@token_required
def api_add_exam():
    request_data = request.get_json()
    if(Exams.validate_exam(request_data)):
        exam = Exams.submit_exam_from_json(request_data)
        if exam is None or exam.id < 0:
            responseObject = {
                "status": "failure",
                "message": "Failed to add an Invalid Exam."                
            }
            return Response(dumps(responseObject), 500, mimetype='application/json')
        responseObject = {
            "status": "success",
            "message": "Exam added successfully.",            
            "exam": exam.serialize()
        }
        return Response(dumps(responseObject), 201, mimetype='application/json')
    else:
        responseObject = {
            "status": "failure",
            "message": "Failed to add an Invalid Exam."                
        }
        return Response(dumps(responseObject), 400, mimetype='application/json')

@application.route("/api/v1/exams/<int:id>", methods=["PUT"])
@token_required
def api_update_exam_via_id(id):
    request_data = request.get_json()
    if(validate_exam(request_data)):
        for exam in exams:
            if exam['id'] == id:
                exams[exams.index(exam)] = request_data
        response = Response("", 204, mimetype='application/json')
        response.headers['Location'] = "/api/v1/exams/" + str(request_data['id'])
        return response
    else:
        responseObject = {
            "status": "failure",
            "message": "Failed to update an Invalid Exam."                
        }
        return Response(dumps(responseObject), 404, mimetype='application/json')

@application.route("/api/v1/exams/<int:id>", methods=["DELETE"])
@token_required
def api_delete_exam_via_id(id):
    exam = Exams.delete_exam_from_id(id)
    if exam is None or exam.id < 0:
        responseObject = {
            "status": "failure",
            "message": "Failed to delete an Invalid Exam."                
        }
        return Response(dumps(responseObject), 404, mimetype='application/json')

    responseObject = {
        "status": "success",
        "message": "Exam deleted successfully.",            
        "exam": exam.serialize()
    }
    return Response(dumps(responseObject), 201, mimetype='application/json')