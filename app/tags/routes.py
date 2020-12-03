from flask import request, flash, redirect, url_for, render_template
from app.models import Tag
from app.tags import tags as bp


@bp.route('/delete/<slug>', methods=['POST', 'GET'])
def delete_tag(slug):
    id = request.args.get('id')
    tag_id = request.args.get('tag_id')
    if id and request.method == 'GET':
        tag = Tag.query.filter_by(id=tag_id).first()
        tag.delete_tag()
        flash('Delete is success')
    return redirect(url_for('posts.edit_post', id=id, slug=slug))


@bp.route('tag/<id>')
def tag_page(id):
    tag = Tag.query.filter_by(id=id).first()
    posts = tag.posts
    return render_template('tags/tag.html', tag=tag, posts=posts)