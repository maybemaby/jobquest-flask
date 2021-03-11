from app import create_app, db
from app.models import JobPosting, Resume, CoverLetter


app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'JobPosting': JobPosting, 'Resume': Resume, 'CoverLetter': CoverLetter}
