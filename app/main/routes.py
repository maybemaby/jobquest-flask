import datetime
from pathlib import Path
from app import db
from flask import render_template, flash, redirect, url_for, request, send_from_directory, current_app
from werkzeug.utils import secure_filename
from app.main.forms import JobPostingForm, ResumeForm, CoverLetterForm, SearchForm, DeleteForm, NotesForm, \
    EditPostingForm
from app.models import JobPosting, Resume, CoverLetter
from app.main import bp


# TODO: File Validation


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    search_form = SearchForm()
    form1 = ResumeForm()
    form2 = CoverLetterForm()
    delete_form = DeleteForm()
    page = request.args.get('page', 1, type=int)
    if request.method == 'POST' and search_form.validate():
        postings = search_form.filter_query().paginate(page, current_app.config['POSTS_PER_PAGE'], False)
        if postings.total == 0:
            flash('No postings found in your search.')
        resumes = Resume.query.order_by(Resume.id)
        cover_letters = CoverLetter.query.order_by(CoverLetter.id)
        next_url = url_for('main.index', page=postings.next_num) if postings.has_next else None
        prev_url = url_for('main.index', page=postings.prev_num) if postings.has_prev else None
    else:
        postings = JobPosting.query.order_by(JobPosting.id).paginate(page, current_app.config['POSTS_PER_PAGE'], False)
        resumes = Resume.query.order_by(Resume.id)  # noqa
        cover_letters = CoverLetter.query.order_by(CoverLetter.id)  # noqa
        next_url = url_for('main.index', page=postings.next_num) if postings.has_next else None
        prev_url = url_for('main.index', page=postings.prev_num) if postings.has_prev else None
    return render_template('index.html', title='Home', postings=postings.items, resumes=resumes,
                           cover_letters=cover_letters,
                           form1=form1, form2=form2, search_form=search_form, delete_form=delete_form,
                           next_url=next_url,
                           prev_url=prev_url)  # noqa


@bp.route('/new-entry', methods=['GET', 'POST'])
def new_entry():
    form = JobPostingForm()
    if form.validate_on_submit():
        company = form.company.data
        position = form.position.data
        location_city = form.location_city.data
        location_state = form.location_state.data
        updated = form.updated.data
        status = form.status.data
        posting = JobPosting(company=company,
                             position=position,
                             location_city=location_city,
                             location_state=location_state,
                             updated=updated, status=status)
        db.session.add(posting)
        resume_file = request.files['resume']  # noqa
        resume_add(resume_file, posting)
        cover_letter_file = request.files['cover_letter']
        cover_letter_add(cover_letter_file, posting)
        db.session.commit()
        flash(f'New entry submitted for {form.company.data}: {form.position.data}')
        return redirect(url_for('main.index'))
    return render_template('jobsubmit.html', title='New Entry', form=form)  # noqa


@bp.route('/delete/<job_post_id>', methods=['POST'])
def delete_entry(job_post_id):
    form = DeleteForm()
    if request.method == "POST" and form.submit():
        entry = JobPosting.query.filter_by(id=job_post_id).first_or_404()
        flash(f'Entry for {entry.company}: {entry.position} removed.')
        db.session.delete(entry)
        db.session.commit()
        return redirect(url_for('main.index'))
    else:
        flash('Entry could not be removed.')
        return redirect(url_for('main.index'))


@bp.route('/resume-upload/<job_post_id>', methods=['POST'])
def upload_resume(job_post_id):
    form = ResumeForm()
    if form.validate_on_submit():
        resume_file = request.files['resume']
        job_post = JobPosting.query.filter_by(id=job_post_id).first()
        if job_post is None:
            flash('Could not add to job post.')
            return redirect(url_for('main.index'))
        resume_add(resume_file, job_post)
        db.session.commit()
        return redirect(url_for('main.index'))
    else:
        flash('Unable to add resume. Try again later.')
        return redirect(url_for('main.index'))


@bp.route('/cover-letter-upload/<job_post_id>', methods=['POST'])
def upload_cover_letter(job_post_id):
    form = CoverLetterForm()
    if form.validate_on_submit():
        cover_letter_file = request.files['cover_letter']
        job_post = JobPosting.query.filter_by(id=job_post_id).first()
        if job_post is None:
            flash('Could not add to job post.')
            return redirect(url_for('main.index'))
        cover_letter_add(cover_letter_file, job_post)
        db.session.commit()
        return redirect(url_for('main.index'))
    else:
        flash('Unable to add cover letter. Try again later.')
        return redirect(url_for('main.index'))


@bp.route('/docs/<filetype>/<name>')
def file_serve(filetype, name):
    if filetype == 'resume':
        return send_from_directory(Path.cwd() / 'app' / 'uploads' / 'resumes', name)
    if filetype == 'cover_letter':
        return send_from_directory(Path.cwd() / 'app' / 'uploads' / 'coverletters', name)


def resume_add(file, job_post: JobPosting = None):
    """
    Adds a Resume object to the db session from a File object taken from forms.

    :param file: object derived from client POST request in form FileFields
    :type file: file
    :param job_post: Optional arg to connect Resume object to existing JobPosting in db.
    :type job_post: JobPosting
    :return: None
    """
    if file.filename != '':
        resume_dir = Path.cwd() / 'app' / 'uploads' / 'resumes' / secure_filename(file.filename)
        file.save(resume_dir)
        resume = Resume(name=file.filename, filepath=resume_dir.as_posix(), jobposting=job_post)
        db.session.add(resume)


def cover_letter_add(file, job_post: JobPosting = None):
    """
    Adds a CoverLetter object to the db session from a File object taken from forms.

    :param file: object derived from client POST request in form FileFields.
    :type file: file
    :param job_post: Optional arg to connect CoverLetter object to exist
    :type job_post: JobPosting
    :return: None
    """
    if file.filename != '':  # noqa
        cover_letter_dir = Path.cwd() / 'app' / 'uploads' / 'coverletters' / secure_filename(file.filename)
        file.save(cover_letter_dir)
        cover_letter = CoverLetter(name=file.filename, filepath=cover_letter_dir.as_posix(),
                                   jobposting=job_post)
        db.session.add(cover_letter)


@bp.route('/detail/<job_post_id>', methods=['GET', 'POST'])
def posting_detail(job_post_id):
    posting = JobPosting.query.filter_by(id=job_post_id).first_or_404()
    form1 = ResumeForm()
    form2 = CoverLetterForm()
    notes_form = NotesForm()
    if request.method == "POST" and notes_form.submit():
        posting.notes = notes_form.notes.data
        db.session.commit()
        flash('Your notes have been saved.')
    return render_template('postingdetail.html', title=f'{posting.company}: {posting.position}', posting=posting,
                           form1=form1, form2=form2, notes_form=notes_form)


@bp.route('/edit-posting/<job_post_id>', methods=['GET', 'POST'])
def edit_posting(job_post_id):
    posting = JobPosting.query.filter_by(id=job_post_id).first_or_404()
    form = EditPostingForm()
    if form.validate_on_submit():
        posting.company = form.company.data
        posting.position = form.position.data
        posting.location_city = form.location_city.data
        posting.location_state = form.location_state.data
        posting.status = form.status.data
        posting.updated = datetime.date.today()
        db.session.commit()
        flash('Posting edited!')
        return redirect(url_for('main.posting_detail', job_post_id=posting.id))
    return render_template('edit_posting.html', title='Edit Posting', posting=posting, form=form)
