from flask import jsonify, request, session, render_template, redirect, url_for, flash
from models import db, User, Article


def register_routes(app):
    # HTML routes
    @app.route('/')
    def index():
        return redirect(url_for('view_articles'))

    @app.route('/login', methods=['GET'])
    def login_page():
        if 'user_id' in session:
            return redirect(url_for('view_articles'))
        return render_template('login.html')

    @app.route('/register', methods=['GET'])
    def register_page():
        if 'user_id' in session:
            return redirect(url_for('view_articles'))
        return render_template('register.html')

    @app.route('/articles')
    def view_articles():
        articles = Article.query.order_by(Article.created_at.desc()).all()
        return render_template('articles.html', articles=articles)

    @app.route('/articles/<int:article_id>')
    def view_article(article_id):
        article = Article.query.get_or_404(article_id)
        return render_template('article_detail.html', article=article)

    @app.route('/articles/new', methods=['GET'])
    def new_article_page():
        if 'user_id' not in session:
            flash('Please login to create an article', 'warning')
            return redirect(url_for('login_page'))
        return render_template('article_form.html')

    @app.route('/articles/<int:article_id>/edit', methods=['GET'])
    def edit_article_page(article_id):
        if 'user_id' not in session:
            flash('Please login to edit articles', 'warning')
            return redirect(url_for('login_page'))

        article = Article.query.get_or_404(article_id)
        if article.user_id != session['user_id']:
            flash('You can only edit your own articles', 'danger')
            return redirect(url_for('view_articles'))

        return render_template('article_form.html', article=article)

    # Authentication routes (Form-based)
    @app.route('/register', methods=['POST'])
    def register():
        # Handle both JSON and form data
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form

        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not username or not email or not password:
            if request.is_json:
                return jsonify({'error': 'Username, email, and password are required'}), 400
            flash('Username, email, and password are required', 'danger')
            return redirect(url_for('register_page'))

        if User.query.filter_by(username=username).first():
            if request.is_json:
                return jsonify({'error': 'Username already exists'}), 400
            flash('Username already exists', 'danger')
            return redirect(url_for('register_page'))

        if User.query.filter_by(email=email).first():
            if request.is_json:
                return jsonify({'error': 'Email already exists'}), 400
            flash('Email already exists', 'danger')
            return redirect(url_for('register_page'))

        new_user = User(username=username, email=email)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        if request.is_json:
            return jsonify({'message': 'User registered successfully', 'user': new_user.to_dict()}), 201

        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login_page'))

    @app.route('/login', methods=['POST'])
    def login():
        # Handle both JSON and form data
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form

        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            if request.is_json:
                return jsonify({'error': 'Username and password are required'}), 400
            flash('Username and password are required', 'danger')
            return redirect(url_for('login_page'))

        user = User.query.filter_by(username=username).first()

        if not user or not user.check_password(password):
            if request.is_json:
                return jsonify({'error': 'Invalid username or password'}), 401
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login_page'))

        session['user_id'] = user.id
        session['username'] = user.username

        if request.is_json:
            return jsonify({'message': 'Login successful', 'user': user.to_dict()}), 200

        flash('Login successful!', 'success')
        return redirect(url_for('view_articles'))

    @app.route('/logout')
    def logout():
        session.clear()
        flash('Logout successful', 'success')
        return redirect(url_for('view_articles'))

    @app.route('/me', methods=['GET'])
    def get_current_user():
        if 'user_id' not in session:
            return jsonify({'error': 'Not authenticated'}), 401

        user = User.query.get(session['user_id'])
        if not user:
            session.clear()
            return jsonify({'error': 'User not found'}), 404

        return jsonify(user.to_dict()), 200

    @app.route('/users', methods=['GET'])
    def get_users():
        users = User.query.all()
        return jsonify([user.to_dict() for user in users])

    @app.route('/users', methods=['POST'])
    def create_user():
        data = request.get_json()

        new_user = User(
            username=data.get('username'),
            email=data.get('email')
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify(new_user.to_dict()), 201

    @app.route('/users/<int:user_id>', methods=['GET'])
    def get_user(user_id):
        user = User.query.get_or_404(user_id)
        return jsonify(user.to_dict())

    @app.route('/users/<int:user_id>', methods=['PUT'])
    def update_user(user_id):
        user = User.query.get_or_404(user_id)
        data = request.get_json()

        if 'username' in data:
            user.username = data['username']
        if 'email' in data:
            user.email = data['email']

        db.session.commit()
        return jsonify(user.to_dict())

    @app.route('/users/<int:user_id>', methods=['DELETE'])
    def delete_user(user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'}), 200

    # Article routes (Form-based + API)
    @app.route('/articles/new', methods=['POST'])
    @app.route('/articles/<int:article_id>/edit', methods=['POST'])
    def save_article(article_id=None):
        if 'user_id' not in session:
            flash('Please login to manage articles', 'warning')
            return redirect(url_for('login_page'))

        if article_id:
            article = Article.query.get_or_404(article_id)
            if article.user_id != session['user_id']:
                flash('You can only edit your own articles', 'danger')
                return redirect(url_for('view_articles'))
            article.title = request.form.get('title')
            article.content = request.form.get('content')
            flash('Article updated successfully!', 'success')
        else:
            article = Article(
                title=request.form.get('title'),
                content=request.form.get('content'),
                user_id=session['user_id']
            )
            db.session.add(article)
            flash('Article created successfully!', 'success')

        db.session.commit()
        return redirect(url_for('view_article', article_id=article.id))

    @app.route('/articles/<int:article_id>/delete', methods=['POST'])
    def delete_article(article_id):
        if 'user_id' not in session:
            flash('Please login to delete articles', 'warning')
            return redirect(url_for('login_page'))

        article = Article.query.get_or_404(article_id)
        if article.user_id != session['user_id']:
            flash('You can only delete your own articles', 'danger')
            return redirect(url_for('view_articles'))

        db.session.delete(article)
        db.session.commit()
        flash('Article deleted successfully!', 'success')
        return redirect(url_for('view_articles'))

    # API routes
    @app.route('/api/articles', methods=['GET'])
    def api_get_articles():
        articles = Article.query.all()
        return jsonify([article.to_dict() for article in articles])

    @app.route('/api/articles', methods=['POST'])
    def api_create_article():
        data = request.get_json()
        new_article = Article(
            title=data.get('title'),
            content=data.get('content'),
            user_id=data.get('user_id')
        )
        db.session.add(new_article)
        db.session.commit()
        return jsonify(new_article.to_dict()), 201

    @app.route('/api/articles/<int:article_id>', methods=['GET'])
    def api_get_article(article_id):
        article = Article.query.get_or_404(article_id)
        return jsonify(article.to_dict())

    @app.route('/api/articles/<int:article_id>', methods=['PUT'])
    def api_update_article(article_id):
        article = Article.query.get_or_404(article_id)
        data = request.get_json()
        if 'title' in data:
            article.title = data['title']
        if 'content' in data:
            article.content = data['content']
        db.session.commit()
        return jsonify(article.to_dict())

    @app.route('/api/articles/<int:article_id>', methods=['DELETE'])
    def api_delete_article(article_id):
        article = Article.query.get_or_404(article_id)
        db.session.delete(article)
        db.session.commit()
        return jsonify({'message': 'Article deleted successfully'}), 200

    # Get articles by user
    @app.route('/users/<int:user_id>/articles', methods=['GET'])
    def get_user_articles(user_id):
        user = User.query.get_or_404(user_id)
        return jsonify([article.to_dict() for article in user.articles])
