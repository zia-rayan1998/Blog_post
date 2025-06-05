from flask import Blueprint, render_template, request, redirect, url_for
from models import BlogPost
from extensions import db

main = Blueprint('main', __name__)

@main.route('/')
def display_blogs():
    blogs = BlogPost.query.order_by(BlogPost.created_at.desc()).all()
    return render_template('display.html', blogs=blogs)

@main.route('/edit', methods=['GET', 'POST'])
@main.route('/edit/<int:blog_id>', methods=['GET', 'POST'])
def edit_blog(blog_id=None):
    blog = BlogPost.query.get(blog_id) if blog_id else None

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if blog:
            blog.title = title
            blog.content = content
        else:
            blog = BlogPost(title=title, content=content)
            db.session.add(blog)

        db.session.commit()
        return redirect(url_for('main.display_blogs'))

    return render_template('edit.html', blog=blog)

@main.route('/delete/<int:blog_id>')
def delete_blog(blog_id):
    blog = BlogPost.query.get_or_404(blog_id)
    db.session.delete(blog)
    db.session.commit()
    return redirect(url_for('main.display_blogs'))
