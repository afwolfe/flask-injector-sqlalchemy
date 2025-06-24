from flask.blueprints import Blueprint

from app.repository import UserRepository


people = Blueprint(
    "people", __name__, template_folder="templates", static_folder="static"
)


@people.route("/")
def test(repo: UserRepository):
    user = repo.get_by_name("Tom")
    if user:
        return "Test: Username %s " % user.username
    else:
        return "User not found"
