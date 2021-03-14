import datetime
from app.main.forms import JobPostingForm


class TestJobPostingForm:
    """Test form for creating a new jobposting"""

    def test_validate_success(self, db):
        """Test successful submit"""
        form = JobPostingForm(
            company="company",
            position="position",
            location_city="City",
            location_state="State",
            status=True
        )
        assert form.validate() is True
        assert bool(form.updated.data)