from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user


class Survey:
    db_name = 'kinetic_db'

    def __init__(self, db_data):
        self.id = db_data['id']
        self.impression = db_data['impression']
        self.feature = db_data['feature']
        self.value = db_data['value']
        self.useful = db_data['useful']
        self.available = db_data['available']
        self.recommend = db_data['recommend']
        self.comment = db_data['comment']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.user_id = db_data['user_id']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO surveys (impression, feature,value, useful, available, recommend, comment, user_id) VALUES (%(impression)s,%(feature)s,%(value)s,%(useful)s, %(available)s, %(recommend)s,%(comment)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM surveys;"
        results = connectToMySQL(cls.db_name).query_db(query)
        all_trees = []
        for row in results:
            print(row['id'])
            all_trees.append(cls(row))
        return all_trees

    # creates an instance of row^

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM surveys WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return cls(results[0])

    @classmethod
    def update(cls, data):
        query = "UPDATE surveys SET impression=%(impression)s,feature=%(feature)s,value=%(value)s, useful=%(useful)s,available=%(available)s,recommend=%(recommend)s,updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM surveys WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @staticmethod
    def validate_survey(survey):
        is_valid = True
        if len(survey['impression']) < 3:
            is_valid = False
            flash("Please fill in the blank", "survey")
        if len(survey['feature']) < 3:
            is_valid = False
        #     flash("Please fill in the blank", "survey")
        # if survey['value'] == "":
        #     is_valid = False
        #     flash("Please choose one option", "survey")
        # if survey['useful'] == "":
        #     is_valid = False
        #     flash("Please chose one option", "survey")
        # if survey['available'] == "":
        #     is_valid = False
        #     flash("Please chose one option", "survey")
        # if survey['recommend'] == "":
        #     is_valid = False
        #     flash("Please chose one option", "survey")

        return is_valid

    @classmethod
    def get_user_info(cls):
        query = "SELECT * FROM surveys JOIN users ON users.id = surveys.user_id;"
        results = connectToMySQL(cls.db_name).query_db(query)
        interests = []
        for dict in results:
            interest = cls(dict)
            users_data = {
                'id': dict['users.id'],
                'created_at': dict['users.created_at'],
                'updated_at': dict['users.updated_at'],
                'first_name': dict['first_name'],
                'last_name': dict['last_name'],
                'email': dict['email'],
                'password': dict['password'],
            }
            user_obj = user.User(users_data)
            interest.user = user_obj
            interests.append(interest)
        return interests

    @classmethod
    def get_trees_with_users(cls, data):
        query = "SELECT * FROM surveys JOIN users ON surveys.user_id = users.id WHERE surveys.id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        for row in results:
            current_survey = cls(row)
            user_data = {
                'id': row['users.id'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'], }
            current_user = user.User(user_data)
            current_survey.user = current_user
        return current_survey
