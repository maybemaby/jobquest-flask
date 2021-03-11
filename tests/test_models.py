"""Model unit tests."""
import datetime
import pytest
from app.models import JobPosting, Resume, CoverLetter


@pytest.mark.usefixtures("db")
class TestJobPosting:
    """JobPosting tests."""

    def test_get_by_id(self):
        # Get JobPosting by ID.
        posting = JobPosting(company="company",
                             position="position",
                             location_city="location_city",
                             location_state="state")
        posting.save()
        retrieved = JobPosting.query.filter_by(posting.id)
        assert retrieved == posting
