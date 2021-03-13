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
