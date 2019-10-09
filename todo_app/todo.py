from functools import wraps
from django.conf import settings
from flask import Blueprint, render_template, redirect, request, session
from notes.models import Note, NoteTag


bp = Blueprint('notes', __name__, url_prefix='/notes')


def protect(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'is_logged_in' not in session:
            passw = request.args.get('p')
            if passw != settings.VERY_COOL_PASSWORD:
                return 'Need password!'
            session['is_logged_in'] = True
        return func(*args, **kwargs)
    return wrapper

def flasked_notes(notes):
    notes = [
        {
            'id': n.id, 'tags': [t.name for t in n.tags.all()], 'date': str(n.time)[0:-9],
            'title': n.content.capitalize(), 'body': n.detail, 'is_done': n.is_done
        } for n in notes
    ]
    return notes


def get_notes():
    notes = Note.objects.all()
    notes = flasked_notes(notes)
    return notes


def set_is_done(id, is_done):
    n = Note.objects.get(id=id)
    n.is_done = is_done
    n.save()


def filter_tags(notes, tags_lst):
    return [n for n in notes if any([tag in n['tags'] for tag in tags_lst])]


def filter_is_done(notes, is_done):
    return [n for n in notes if n['is_done'] == is_done]


todo_filter = ('todo', 'todos', 'task', 'tasks')


def get_non_todos():
    notes = Note.objects.all().exclude(tags__name__in=todo_filter)
    return flasked_notes(notes)


@bp.route('/')
@bp.route('/all')
@protect
def all():
    notes = get_non_todos()
    return render_template('notes/index.html', notes=notes, title='NOTES')


@bp.route('/todo')
@protect
def todo():
    todos = filter_is_done(filter_tags(get_notes(), todo_filter), False)
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
