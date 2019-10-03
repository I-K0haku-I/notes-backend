from functools import wraps
from django.conf import settings
from flask import Blueprint, render_template, redirect, request, session
from .connector import get_conn


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


def get_tags():
    conn = get_conn()
    tags = conn.tags.list().json()
    tags_n = {t['id']: t['name'] for t in tags}
    tags_r = {t['name']: t['id'] for t in tags}
    return tags_n, tags_r


def get_notes():
    conn = get_conn()
    tags_n, tags_r = get_tags()
    notes = conn.notes.list().json()
    notes = [
        {
            'id': n['id'], 'tags': [tags_n[t] for t in n['tags']], 'date': n['time'],
            'title': n['content'].capitalize(), 'body': n['detail'], 'is_done': n['is_done']
        } for n in notes
    ]
    return notes

def set_is_done(id, is_done):
    conn = get_conn()
    conn.notes.update(id, {'is_done': is_done})

def filter_tags(notes, tags_lst):
    return [n for n in notes if any([tag in n['tags'] for tag in tags_lst])]

def filter_is_done(notes, is_done):
    return [n for n in notes if n['is_done'] == is_done]

todo_filter = ('todo', 'todos', 'task', 'tasks')


@bp.route('/')
@bp.route('/all')
@protect
def all():
    notes = get_notes()
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
    if not is_done:
        return redirect('/notes/todo')
    else:
        return redirect('/notes/done')
