#Imports

from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask import jsonify

db_connect = create_engine('sqlite:///quiz.db')
app = Flask(__name__)
api = Api(app)

#Classes

class Quiz(Resource):
    """GET response for Quiz"""

    def get(self, quiz_id):
        conn = db_connect.connect()
        query = conn.execute("select * from quiz where id =%d "  %int(quiz_id))
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        
        if result['data'] == []:
            print(result)
            response = jsonify({})
            response.status_code = 404
            return response
        
        response = jsonify(result['data'][0])
        response.status_code = 200
        return response
    
    def post(self, quiz_id):
        pass

class QuizList(Resource):
    """POST response for Quiz"""

    def get(self):
        pass
    
    def post(self):
        conn = db_connect.connect()
        print(request.json)
        name = request.json['name']
        description = request.json['description']

        query = conn.execute("insert into quiz (name, description) values ('{0}', '{1}')".format(name,description))

        query = conn.execute("select * from quiz where name ='{0}' and description='{1}' ".format(name,description))
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        

        if result['data'] == []:
            print(result)
            response = jsonify(dict(status="failure",reason="explanation"))
            response.status_code = 400
            return response
        
        response = jsonify(result['data'][0])
        response.status_code = 201
        return response
    

class Question(Resource):
    """GET response for Question"""

    def get(self, question_id):
        conn = db_connect.connect()
        query = conn.execute("select * from questions where id =%d "  %int(question_id))
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        
        if result['data'] == []:
            print(result)
            response = jsonify({})
            response.status_code = 404
            return response
        
        response = jsonify(result['data'][0])
        response.status_code = 200
        return response
    
    def post(self, question_id):
        pass

class QuestionList(Resource):
    """POST Response for Questions"""

    def get(self):
        pass
    
    def post(self):
        conn = db_connect.connect()
        request.args
        print(request.json)
        name = request.json['name']
        options = request.json['options']
        correct_option = request.json['correct_option']
        quiz = request.json['quiz']
        points = request.json['points']

        query = conn.execute("insert into questions (name, options, correct_option, quiz, points) values ('{0}', '{1}', '{2}', '{3}', '{4}')".format(name,options,correct_option,quiz,points))
        query = conn.execute("select * from questions where name ='{0}' and options='{1}' ".format(name,options))
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        

        if result['data'] == []:
            print(result)
            response = jsonify(dict(status="failure",reason="explanation"))
            response.status_code = 400
            return response
        
        response = jsonify(result['data'][0])
        response.status_code = 201
        return response    

class QuizQuestion(Resource):

    """GET response for QuizQuestion"""

    def get(self, quiz_id):
        conn = db_connect.connect()
        #query = conn.execute("select * from questions where id =%d "  %int(quiz_id))
        #query = conn.execute("select quiz.*, questions.* from quiz LEFT JOIN questions ON quiz.id=questions.quiz where quiz.id =%d "  %int(quiz_id))
        query = conn.execute("select quiz.id quiz_id, quiz.name quiz_name, quiz.description quiz_description, questions.id question_id, questions.name question_name, questions.options question_options, questions.correct_option question_correct_option, questions.points question_points from quiz left join questions on quiz.id = questions.quiz where quiz.id =%d "  %int(quiz_id))
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        print(result['data'][0])
        
        if result['data'] == []:
            print(result)
            response = jsonify({})
            response.status_code = 404
            return response
        
        new_dictionary = result['data'][0]
        final_dictionary = dict(name=new_dictionary['quiz_name'], description=new_dictionary['quiz_description'], questions=[dict(id=new_dictionary['question_id'], name=new_dictionary['question_name'], options=new_dictionary['question_options'], correct_option=new_dictionary['question_correct_option'], points=new_dictionary['question_points'])])
        #response = jsonify(result['data'][0])
        response = jsonify(final_dictionary)
        response.status_code = 200
        return response
    
    def post(self, question_id):
        pass
        
api.add_resource(QuizList, '/api/quiz/') # Route_2
api.add_resource(Quiz, '/api/quiz/<quiz_id>') # Route_1

api.add_resource(QuestionList, '/api/questions/') # Route_4
api.add_resource(Question, '/api/questions/<question_id>') # Route_3

api.add_resource(QuizQuestion, '/api/quiz-questions/<quiz_id>') # Route_5

#Main

if __name__ == '__main__':
     app.run(port='8080')