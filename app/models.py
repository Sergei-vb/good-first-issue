from gino import Gino

db = Gino()


class Issue(db.Model):
    __tablename__ = "issues"

    id = db.Column(db.Integer, primary_key=True)
    issue_id = db.Column(db.Integer, unique=True)
    api_url = db.Column(db.String(length=255), unique=True)
    html_url = db.Column(db.String(length=255), unique=True)
    title = db.Column(db.String(length=255))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    closed_at = db.Column(db.DateTime)
    comments_count = db.Column(db.Integer)
    labels = db.Column(db.ARRAY(db.String(length=255)))
    repository_api_url = db.Column(
        db.String(length=255),
        db.ForeignKey("repositories.api_url", ondelete="CASCADE"),
        nullable=False,
    )


class Repository(db.Model):
    __tablename__ = "repositories"

    id = db.Column(db.Integer, primary_key=True)
    repository_id = db.Column(db.Integer, unique=True)
    api_url = db.Column(db.String(length=255), unique=True)
    html_url = db.Column(db.String(length=255), unique=True)
    name = db.Column(db.String(length=255))
    full_name = db.Column(db.String(length=255))
    fork = db.Column(db.Boolean)
    archived = db.Column(db.Boolean)
    forks_count = db.Column(db.Integer)
    stargazers_count = db.Column(db.Integer)
