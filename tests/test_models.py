"""Model unit tests."""
import datetime
import os
from io import TextIOWrapper
from pathlib import Path
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

    def test_accessible_filepath(self):
        """Test to ensure filepath attribute can be used to access files"""
        filepath = (Path.cwd() / 'tests' / 'test.txt').as_posix()
        test_file = open(filepath, "w")
        test_file.write("Hello world!")
        test_file.close()
        resume = Resume(name="resume_name", filepath=filepath)
        resume_file = open(resume.filepath, 'r')
        assert type(resume_file) == TextIOWrapper
        assert resume_file.readline() == "Hello world!"
        resume_file.close()
        os.remove(filepath)


@pytest.mark.usefixtures("db")
class TestCoverLetter:
    """CoverLetter test cases."""

    def test_get_by_id(self):
        """Test retrieval of CoverLetter by id"""
        cover_letter = CoverLetter(name="cover_letter_name")
        db.session.add(cover_letter)
        db.session.commit()
        retrieved = CoverLetter.query.filter_by(id=cover_letter.id).first()
        assert retrieved == cover_letter

    def test_str(self):
        """test __str__ method of CoverLetter"""
        cover_letter = CoverLetter(name="cover_letter_name")
        db.session.add(cover_letter)
        db.session.commit()
        assert str(cover_letter) == 'cover_letter_name'

