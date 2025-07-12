from flask import jsonify, Blueprint

from app.db.models import User, db
from app.app_types.UserType import UserType

bp = Blueprint("users", __name__, url_prefix="/v1/users")


@bp.route("/<string:user_name>/<string:user_type>", methods=["POST"])
def create_user(user_name, user_type):
    """
    Create a new user
    ---
    parameters:
      - name: user_name
        in: path
        type: string
        required: true
        description: The username to create
      - name: user_type
        in: path
        type: string
        required: true
        description: The type of the user (e.g., 'admin', 'regular')
    responses:
      201:
        description: User successfully created
      400:
        description: Bad request, e.g. missing or invalid parameters
      409:
        description: Conflict – user with this name already exists
    """

    if not UserType.is_valid_usertype(user_type):
        return jsonify({"error": "User type is not supported"}), 409

    existing_user = User.query.filter_by(user_name=user_name).first()
    if existing_user:
        return jsonify({"error": "Username already exists"}), 409

    new_user = User(user_name=user_name, user_type=user_type)
    db.session.add(new_user)
    db.session.commit()

    return (
        jsonify(
            {
                "message": f"User '{user_name}' created successfully",
                "user_id": new_user.id,
            }
        ),
        201,
    )
