import sys
from flask import Blueprint, render_template, redirect, request
from .connector import get_conn

bp = Blueprint('notes', __name__, url_prefix='/notes')


def protect(func):
    def wrapper(*args, **kwargs):
        passw = request.args.get('p')
        if passw != 'shh123':
            return 'Need password!'
        return func(*args, **kwargs)
    return wrapper


is_done_1 = True
is_done_2 = False
todos = [
    {
        'id': 1,
        'tags': ['blah', '3242', 'tasks'],
        'date': "2019-09-29 14:00",
        'title': 'do some stuff',
        'body': 'lajdflkajlfkajdlkfa',
        'is_done': is_done_1
    },
    {
        'id': 2,
        'tags': ['asdfa', 'tasks'],
        'date': "2019-09-29 14:01",
        'title': 'do some stuff2',
        'body': 'dlkjlk ljdfla fa oi',
        'is_done': is_done_2
    }
]

def get_tags():
    conn = get_conn()
    tags = conn.tags.list().json()
    tags_n = {t['id']: t['name'] for t in tags}
    tags_r = {t['name']: t['id'] for t in tags}
    return tags_n, tags_r


def get_todos():
    conn = get_conn()
    tags_n, tags_r = get_tags()
    notes = conn.notes.list().json()
    todos = [
        {
            'id': n['id'], 'tags': [tags_n[t] for t in n['tags']], 'date': n['time'],
            'title': n['content'].capitalize(), 'body': n['detail'], 'is_done': True
        } for n in notes
    ]
    return todos


def filter_tags(notes, tags_lst):
    return [n for n in notes if any([tag in n['tags'] for tag in tags_lst])]


todo_filter = ('todo', 'todos', 'task', 'tasks')


@bp.route('/')
@bp.route('/all')
@protect
def all():
    todos = get_todos()
    return render_template('todo/index.html', todos=todos, title='NOTES')


@bp.route('/todo')
@protect
def todo():
    todos = filter_tags(get_todos(), todo_filter)
    return render_template('todo/index.html', todos=todos, title='TODO')


@bp.route('/done')
@protect
def done():
    todos = filter_tags(get_todos(), todo_filter)
    return render_template('todo/index.html', todos=todos, title='DONE')


@bp.route('/activate/<int:id>/<string:is_done>')
@protect
def activate(id, is_done):

    # print(is_done, file=sys.stderr)

    if id == 1:
        is_done_1 = not (True if is_done == 'True' else False)
    else:
        is_done_2 = not (True if is_done == 'True' else False)
    return redirect('/')
