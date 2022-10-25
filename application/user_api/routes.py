# application/user_api/routes.py
from . import user_api_blueprint
from .. import db, login_manager
from ..models import User
from flask import make_response, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
import random, string
from passlib.hash import sha256_crypt


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


@login_manager.request_loader
def load_user_from_request(request):
    api_key = request.headers.get('Authorization')
    if api_key:
        api_key = api_key.replace('Basic ', '', 1)
        user = User.query.filter_by(api_key=api_key).first()
        if user:
            return user
    return None

@user_api_blueprint.route('/')
def index():
    return "<p> Welcome to User Api <p>"

@user_api_blueprint.route('/api/users', methods=['GET'])
def get_users():
    data = []
    for row in User.query.all():
        data.append(row.to_json())

    response = jsonify(data)
    return response


@user_api_blueprint.route('/api/user/create', methods=['POST'])
def post_register():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    invited_code = request.form['invited_code']
    username = request.form['username']
    password = request.form['password']

    print("first_name =>", first_name)
    print("last_name =>", last_name)
    print("email =>", email)
    print("username =>", username)
    print("password =>", password)

    password = sha256_crypt.hash((str(request.form['password'])))
    user = User.query.filter(User.username == username).first()
    # check if the user exists
    if user:
        return {'message': 'this username already exists'}
    # check if the username is valid
    if (0< len(username) <= 15) and '.' not in username and '_' not in username:
        return {'message': 'the username is invalid'}
    user = User()
    user.email = email
    user.first_name = first_name
    user.last_name = last_name
    user.password = password
    user.username = username
    user.referral_code = generate_referral_code()
    user.invited_code = invited_code
    user.authenticated = True

    # db.session.add(user)
    # db.session.commit()
    # response = jsonify({'message': 'User added', 'status':'success'})
    response = jsonify({'message': 'User added', 'status':'success', 'result': user.to_json()})
    try:
        db.session.add(user)
        # TODO: tell wallet service to create a on chain address for this user
        db.session.commit()
        return {'msg': 'success'}
    except Exception as e:
        db.session.rollback()
        return {'message': 'When the user is generated, insertion into database failed', 'code': 201}


# the invite code will be used when the bot is activated by this user
def check_invite(user, invited_code):
    invited_code = invited_code.strip()
    # compare this user's invited code with other users' referral code
    invite_user = User.query.filter(User.referral_code == invited_code).first()  # 用户输入的邀请码和邀请用户数据库中的邀请码比对
    if invite_user:
        # TODO: use the ledger service api to add a new ledge of paying the inviter
        pass
    else:
        return {'msg': 'This invited code is invalid.'}


def generate_referral_code():
    poolOfChars = string.ascii_letters + string.digits
    random_codes = lambda x, y: ''.join([random.choice(x) for i in range(y)])
    candidate = random_codes(poolOfChars, 6)
    while User.query.filter(User.referral_code == candidate).first():
        candidate = random_codes(poolOfChars, 6)
    return candidate


@user_api_blueprint.route('/api/<int:user_id>/referral_code', methods=['GET', 'POST'])
def referral_code(user_id):
    user = User.query.filter(User.id == user_id).first()
    if user:
        if request.method == 'POST':
            referral_code = request.form['referral_code']
            if not referral_code.isalnum():
                return {'message': 'the custom referral code has to be alphanumeric.'}
            if len(referral_code) < 4 or len(referral_code) > 12:
                return {'message': 'the length of custom referral code has to be between 4 to 12'}
            user.referral_code = referral_code
            try:
                db.session.add(user)
                db.session.commit()
                return {'msg': 'success'}
            except Exception as e:
                db.session.rollback()
                return {'message': 'Insertion into database failed', 'code': 201}
        else:
            return {'referral_code': user.referral_code}
    else:
        return f'User not found'



@user_api_blueprint.route('/api/user/login', methods=['POST'])
def post_login():
    username = request.form['username']
    user = User.query.filter_by(username=username).first()
    print(user)
    password = request.form['password']
    if user:
        # print('here')
        encrypted_pass = sha256_crypt.encrypt(user.password)
        test_password = str(password)
        print(test_password)
        print(sha256_crypt.verify(str(password), encrypted_pass))
        if sha256_crypt.verify(str(password), encrypted_pass):
            # print('here2')
            user.encode_api_key()
            # db.session.commit()
            # login_user(user)
            print("current user =>", current_user);

            return make_response(jsonify({'message': 'Logged in', 'api_key': user.api_key, 'success': True}))
        else:
            return make_response(jsonify({'message': 'invalid username or password', 'success': False}), 401)
    return make_response(jsonify({'message': 'invalid username or password', 'success': False}), 401)


@user_api_blueprint.route('/api/user/logout', methods=['POST'])
def post_logout():
    if current_user.is_authenticated:
        logout_user()
        return make_response(jsonify({'message': 'You are logged out'}))
    return make_response(jsonify({'message': 'You are not logged in'}))


@user_api_blueprint.route('/api/user/<username>/exists', methods=['GET'])
def get_username(username):
    item = User.query.filter_by(username=username).first()
    if item is not None:
        response = jsonify({
            'id': item.id,
            'username': item.username,
            'result': True})
    else:
        response = jsonify({'message': 'Cannot find username'}), 404
    return response


@login_required
@user_api_blueprint.route('/api/user', methods=['GET'])
def get_user():
    if current_user.is_authenticated:
        return make_response(jsonify({'result': current_user.to_json()}))

    return make_response(jsonify({'message': 'Not logged in'})), 401