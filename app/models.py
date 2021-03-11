from app import db
import datetime


class JobPosting(db.Model):
    """Represents job postings being recorded with related info.

    Class used in SQLAlchemy ORM with one-to-one relationships with Resume and CoverLetter
    classes. JobPosting status uses boolean type to interpret as application status.

    __tablename__ = jobposting

    :param company: Name of company job posting under.
    :type company: String
    :param position: Name of position being hired for.
    :type position: String
    :param updated: Last update time. defaults to time of database addition.
    :type updated: datetime.date
    :param status: True for applied to postings, False otherwise.
    :type status: Boolean
    :return: None
    """
    __tablename__ = "jobposting" # noqa

    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(32))
    location_city = db.Column(db.String(32))
    location_state = db.Column(db.String(5))
    updated = db.Column(db.DateTime, default=datetime.date.today())
    position = db.Column(db.String(32))
    status = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text, default=None)
    resume = db.relationship("Resume", uselist=False, back_populates="jobposting") # noqa
    coverletter = db.relationship("CoverLetter", uselist=False, back_populates="jobposting") # noqa

    def __str__(self):
        return f"{self.position} for {self.company} in {self.location_city}, {self.location_state}"

    def __repr__(self):
        return f"<JobPosting(id={self.id}, company={self.company}, position={self.position})>"


class Resume(db.Model):

    __tablename__ = "resume" # noqa

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    updated = db.Column(db.DateTime, default=datetime.date.today())
    jobposting_id = db.Column(db.Integer, db.ForeignKey("jobposting.id")) # noqa
    jobposting = db.relationship("JobPosting", back_populates="resume") # noqa
    filepath = db.Column(db.String)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Resume(name={self.name})>"

    def connect_post(self, job_post: JobPosting):
        if not self.jobposting:
            self.jobposting = job_post # noqa


class CoverLetter(db.Model):

    __tablename__ = "coverletter" # noqa

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    updated = db.Column(db.DateTime, default=datetime.date.today())
    jobposting_id = db.Column(db.Integer, db.ForeignKey("jobposting.id")) # noqa
    jobposting = db.relationship("JobPosting", back_populates="coverletter") # noqa
    filepath = db.Column(db.String)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<CoverLetter(name={self.name})>"

    def connect_post(self, job_post: JobPosting):
        if not self.jobposting:
            self.jobposting = job_post # noqa
