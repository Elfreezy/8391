from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required

from datetime import datetime

from app import db
from app.posts import posts as bp
from app.models import Post, slugy
from app.posts.forms import PostForm


@bp.route('/create_post', methods=['POST', 'GET'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit() and request.method == 'POST':
        post = Post(title=form.title.data, body=form.body.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        post.set_tags(tags=form.tags.data)
        return redirect(url_for('posts.posts'))
    return render_template('posts/create_post.html', form=form)


@bp.route('/posts')
@login_required
def posts():
    posts = Post.query.all()
    return render_template('posts/posts.html', posts=posts)


@bp.route('/edit_post/<slug>', methods=['POST', 'GET'])
def edit_post(slug):
    id = request.args.get('id')
    post = Post.query.filter_by(id=id).first_or_404()
    form = PostForm(formdata=request.form, obj=post)
    if form.validate_on_submit() and request.method == 'POST':
        post.title, post.body, post.slug = form.title.data, form.body.data, slugy(form.title.data)
        post.created = datetime.utcnow()
        post.set_tags(tags=form.tags.data)
        db.session.add(post)
        db.session.commit()
        flash('Success')
        return redirect(url_for('posts.post', slug=post.slug, id=post.id))
    form.tags.data = 'New_tags'
    return render_template('posts/edit_post.html', form=form, id=post.id, slug=post.slug, tags=post.tags)


@bp.route('/delete/<slug>', methods=['POST', 'GET'])
def delete_post(slug):
    id = request.args.get('id')
    if id and request.method == 'GET':
        post = Post.query.filter_by(id=id).first()
        db.session.delete(post)
        db.session.commit()
        flash('Delete is success')
        return redirect(url_for('profile', id=current_user.id))
    return redirect(url_for('index'))


@bp.route('/post/<slug>')
@login_required
def post(slug):
    id = request.args.get('id')
    post = Post.query.filter_by(id=id).first()
    tags = post.tags
    return render_template('posts/post.html', post=post, tags=tags)