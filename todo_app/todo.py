from datetime import datetime, timedelta
from functools import wraps

from django.conf import settings
from flask import Blueprint, redirect, render_template, request, session

from notes.models import Note, NoteTag
from middleware import masterkey

bp = Blueprint('notes', __name__, url_prefix='/notes')


def protect(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        passw = request.args.get('p')
        if passw is not None:
            if passw == settings.VERY_COOL_PASSWORD:
                session['has_admin'] = True
            else:
                session.pop('has_admin', None)
            session['is_logged_in'] = True
        if 'is_logged_in' not in session or not session['is_logged_in']:
            return 'Need password!'
        if 'has_admin' in session and session['has_admin']:
            masterkey.db_local.db_to_use = 'private'
        else:
            masterkey.db_local.db_to_use = 'default'
        return func(*args, **kwargs)
    return wrapper


def flasked_notes(notes):
    notes = [
        {
            'id': n.id, 'tags': [t.name for t in n.tags.all()], 'date': str(n.time)[0:-9],
            'title': n.content.capitalize(), 'body': n.detail, 'is_done': n.is_done, 'is_important': n.is_important
        } for n in notes
    ]
    return notes


def get_notes(**kwargs):
    notes = Note.objects.all()
    if len(kwargs) > 0:
        notes = notes.filter(**kwargs)
    notes = flasked_notes(notes)
    return notes


def set_is_done(id, is_done):
    n = Note.objects.get(id=id)
    n.is_done = is_done
    n.save()


def set_is_important(id):
    n = Note.objects.get(id=id)
    n.is_important = True
    n.save()


def filter_tags(notes, tags_lst):
    return [n for n in notes if any([tag in n['tags'] for tag in tags_lst])]


def filter_tags_not(notes, tags_lst):
    return [n for n in notes if not any([tag in n['tags'] for tag in tags_lst])]


def filter_is_done(notes, is_done):
    return [n for n in notes if n['is_done'] == is_done]


todo_filter = ('todo', 'todos', 'task', 'tasks')


def get_non_todos(amount: int = None, tags=None):
    if tags is not None:
        if not isinstance(tags, (list, tuple)):
            tags = [tags]
        notes = Note.objects.filter(tags__name__in=tags)
    else:
        notes = Note.objects.all().exclude(tags__name__in=todo_filter)
    notes = notes.order_by('-id')[:amount]
    return flasked_notes(notes)


@bp.route('/')
@bp.route('/all')
@bp.route('/all/<tags>')
@protect
def all(tags=None):
    notes = get_non_todos(amount=20, tags=tags)
    # if tags is not None:
    #     if not isinstance(tags, (list, tuple)):
    #         tags = [tags]
    #     notes = filter_tags(notes, tags)
    return render_template('notes/index.html', notes=notes, title='NOTES')


@bp.route('all/date')
@bp.route('all/date/<date>')
@protect
def all_date(date=None):
    new_date = datetime.today()
    if date == 'prev':  # previous
        new_date -= timedelta(days=1)
    elif date is not None:
        new_date = datetime.fromisoformat(str(date))
    filters = {'time__date__range': [new_date, new_date]}
    notes = get_notes(**filters)
    return render_template('notes/index.html', notes=notes, title='NOTES')


@bp.route('/todo')
@bp.route('/todo/<tags>')
@protect
def todo(tags=None):
    todos = filter_is_done(filter_tags(get_notes(), todo_filter), False)
    if tags is None:
        todos = filter_tags_not(todos, ('work',))
    else:
        if not isinstance(tags, (list, tuple)):
            tags = [tags]
        todos = filter_tags(todos, tags)
    todos = sorted(todos, key=lambda t: t['is_important'], reverse=True)
    return render_template('notes/index.html', notes=todos, title='TODO')


@bp.route('/done')
@protect
def done():
    dones = filter_is_done(filter_tags(get_notes(), todo_filter), True)
    return render_template('notes/index.html', notes=dones, title='DONE')


@bp.route('/activate/<int:id>/<string:is_done>')
@protect
def activate(id, is_done):
    is_done = True if is_done == 'True' else False
    set_is_done(id, not is_done)
    return redirect(request.referrer)


@bp.route('/make_important/<int:id>/')
def make_important(id):
    set_is_important(id)
    return redirect(request.referrer)
