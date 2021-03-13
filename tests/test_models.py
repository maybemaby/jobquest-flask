"""Model unit tests."""
import datetime
import pytest
from app.models import JobPosting, Resume, CoverLetter
from app import db


@pytest.mark.usefixtures("db")
class TestJobPosting:
    """JobPosting tests."""

    def test_get_by_id(self):
        # Get JobPosting by ID.
        posting = JobPosting(company="company",
                             position="position",
                             location_city="location_city",
                             location_state="state")
        db.session.add(posting)
        db.session.commit()
        retrieved = JobPosting.query.filter_by(id=posting.id).first()
        assert retrieved == posting

    def test_updated_default(self):
        """Test posting without specified update to default with datetime.date.today()"""
        posting = JobPosting(company="company",
                             position="position",
                             location_city="location_city",
                             location_state="state")
        db.session.add(posting)
        db.session.commit()
        assert bool(posting.updated)
        assert isinstance(posting.updated, datetime.date)

    def test_str(self):
        """Test posting __str__ output"""
        posting = JobPosting(company="company",
                             position="position",
                             location_city="location_city",
                             location_state="state")
        db.session.add(posting)
        db.session.commit()
        assert str(posting) == "position for company in location_city, state"


@pytest.mark.usefixtures("db")
class TestResume:
    """Resume model tests"""

    def test_get_by_id(self):
        """Test retrieval of resume by id"""
        resume = Resume(name="resume_name")
        db.session.add(resume)
        db.session.commit()
        retrieved = Resume.query.filter_by(id=resume.id).first()
        assert retrieved == resume

    def test_str(self):
        """test __str__ method of Resume"""
        resume = Resume(name="resume_name")
        db.session.add(resume)
        db.session.commit()
        assert str(resume) == 'resume_name'

    def test_connect_post(self):
        """test connect_post method"""
        resume = Resume(name="resume_name")
        posting = JobPosting(company="company",
                             position="position",
                             location_city="location_city",
                             location_state="state")
        db.session.add_all([resume,posting])
        db.session.commit()
        resume.connect_post(posting)
        assert resume.jobposting == posting
        assert posting.resume == resume
