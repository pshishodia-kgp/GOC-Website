import json
from sqlalchemy import and_
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, current_user, logout_user, login_required
from goc import app, db, USERNAME_REGEX_NOT
from goc.forms import *
from goc.models import *
from bs4 import BeautifulSoup as soup
import requests


# Home Page
@app.route('/')
def home():
    return render_template('home.j2', title = '')

@app.route('/forum')
def postList():
    interview = request.args.get('interview')
    if interview == 'True':
        tag_url = request.args.get('tag')
        page = request.args.get('page', 1, int)
        if tag_url:
            posts = Post.query.filter(and_(Post.blog != None, Post.tags.any(name=tag_url))).order_by(Post.id.desc()).paginate(per_page=2, page=page)
        else:
            posts = Post.query.filter(Post.blog != None).order_by(Post.id.desc()).paginate(per_page=2, page=page)
    else:
        tag_url = request.args.get('tag')
        page = request.args.get('page', 1, int)
        if tag_url:
            posts = Post.query.filter(Post.tags.any(name=tag_url)).order_by(Post.id.desc()).paginate(per_page=2, page=page)
        else:
            posts = Post.query.order_by(Post.id.desc()).paginate(per_page=2, page=page)
    tags = Tag.query.all()
    return render_template('allblogs.j2', title='Posts', posts=posts, allTags=tags, tag_url=tag_url, interview=interview)

@app.route('/post')           ## get single blog having given id
def post():
    post_id = request.args.get('post_id')
    if not post_id:
        return redirect(url_for('postList'))

    post = Post.query.filter_by(id=int(post_id)).first()

    if post:
        return render_template('blog.j2', title=post.title, post=post)
    else:
        flash('Post Not Found!', 'danger')
        return redirect(url_for('postList'))


# login and sign up routes

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter((User.username==form.username_or_email.data) | (User.email==form.username_or_email.data)).first()
        login_user(user)
        return redirect(url_for('home'))
    else:
        flash('Login Failed. Please check username/email and password', 'danger')
    return render_template('login.j2', title='Login', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = SignUpForm()
    if form.validate_on_submit():
        print(form.username.data)
        user = User(username=form.username.data, email=form.email.data,
            name=form.name.data, password=form.password.data,
            profile_pic_url = form.profile_pic_url.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('signup_verified'))
    return render_template('signup.j2', title='Sign Up', form = form)


@app.route('/signup-verified', methods=['GET', 'POST'])
def signup_verified():
    return render_template('signup_verified.j2', title='Verify Signup')


@app.route('/logout')
def logout():
    logout_user()
    flash('You have been successfully logged out!', 'success')
    return redirect(url_for('home'))


# blog submission route

@app.route('/createPost',methods = ['POST','GET'])
@login_required
def submitPost():

    isBlog = request.args.get('interview')
    allTags = Tag.query.all()

    if isBlog == 'True':
        blog_form = BlogForm()

        if(blog_form.addInterview.data):
            blog_form.interview.rounds.append_entry()        
            return render_template('blogform.j2', post_form=blog_form, allTags=allTags, isBlog=isBlog)
        
        if(blog_form.addShortListing.data):
            blog_form.shortlisting.rounds.append_entry()
            return render_template('blogform.j2', post_form=blog_form, allTags=allTags, isBlog=isBlog)
        
        if(blog_form.validate_on_submit()):

            post_data = Post(
                title = str(blog_form.title.data),
                content = str(blog_form.content.data),
                author_id = current_user.id
            )

            try:
                db.session.add(post_data)
                db.session.commit()
            except:
                return "Error in adding Post"

            post_id = post_data.id

            blog_data = Blog(            
                post_id = post_id,
                shortlisting_content = str(blog_form.shortlisting.content.data),
                interview_content = str(blog_form.interview.content.data)
            )

            try:
                db.session.add(blog_data)
                db.session.commit()
            except:
                return "Error in adding Blog"
            
            blog_id = blog_data.id

            tags = blog_form.tags.data.split()

            for ttag in tags:
                tag = Tag.query.filter_by(name=ttag).first()
                if not tag:
                    tag = Tag(name=ttag)
                    post_data.tags.append(tag)
                    tag.posts.append(post_data)
                    try:
                        db.session.add(tag)
                        db.session.commit()
                    except:
                        return "Error in Adding Tag"
                else:
                    post_data.tags.append(tag)
                    tag.posts.append(post_data)              
            
            for round in blog_form.shortlisting.rounds:
                current_round = Round(
                    round_type = RoundType.shortlisting,
                    company_name = str(round.company_name.data),
                    content = str(round.content.data),
                    blog_id = blog_id,
                    selected = round.selected.data
                )
                tag = Tag.query.filter_by(name=current_round.company_name).first()
                if tag:
                    tag.isCompany = True
                else:
                    tag = Tag(name=current_round.company_name, isCompany=True)
                    tag.posts.append(post_data)
                    post_data.tags.append(tag)
                    db.session.add(tag)
                try:
                    db.session.add(current_round)
                except:
                    return "Error in Adding ShortListing Data"
            
            for round in blog_form.interview.rounds:
                current_round = Round(
                    round_type = RoundType.interview,
                    company_name = str(round.company_name.data),
                    content = str(round.content.data),
                    blog_id = blog_id,
                    selected = round.selected.data,
                    joining = round.joining.data
                )
                try:
                    db.session.add(current_round)
                except:
                    return "Error in Adding Interview Round Data"
            
            try:
                db.session.commit()                       
            except:
                return "Error in commiting changes"

            flash('Post Added Successfully!', 'success')
            return redirect(url_for('postList'))

        return render_template('blogform.j2', post_form=blog_form, allTags=allTags, isBlog=isBlog)
    elif isBlog == 'False':
        post_form = PostForm()

        if post_form.validate_on_submit():
            tags = [str(x) for x in set(post_form.tags.data)]

            post_data = Post(
                title = str(post_form.title.data),
                content = str(post_form.content.data),
                author_id = current_user.id
            )

            try:
                db.session.add(post_data)
                db.session.commit()
            except:
                return "Error in adding Post"
            
            tags = post_form.tags.data.split()

            for ttag in tags:
                tag = Tag.query.filter_by(name=ttag).first()
                if not tag:
                    tag = Tag(name=ttag)
                    post_data.tags.append(tag)
                    tag.posts.append(post_data)
                    try:
                        db.session.add(tag)
                    except:
                        return "Error in Adding Tag"
                else:
                    post_data.tags.append(tag)
                    tag.posts.append(post_data)
            
            try:
                db.session.commit()                       
            except:
                return "Error in commiting changes"

            flash('Post Added Successfully!', 'success')
            return redirect(url_for('postList'))

        return render_template('postform.j2', post_form=post_form, allTags=allTags, isBlog=isBlog)
    else: 
        return redirect(url_for('home'))

@app.route('/add_comment', methods = ['GET', 'POST'])
@login_required
def addComment():
    try: 
        form = request.form
        parent_id = int(form.get('parent_id'))
        # Should actually check in database. Works in general until user tries to abuse the system
        parent_id = parent_id if parent_id != -1 else None
        
        # Put checks here. 
        comment = Comment(
            content = form.get('content'),
            post_id = int(form.get('post_id')),
            parent_id = parent_id,
            author_id = current_user.id,
            depth = int(form.get('depth')),
        )

        db.session.add(comment)
        db.session.commit()
    except: 
        return 'Error in adding comment'
    if form.get('post_id'): 
        return redirect('/post?post_id=' + form.get('post_id'))
    return redirect(url_form('home'))


@app.route('/profile/<username>')
def profile(username): 
    if re.search(USERNAME_REGEX_NOT, username): 
        return 'Invalid Username'
    user = User.query.filter_by(username = str(username)).first()
    if not user: 
        return 'Invalid Username'
    
    return render_template('user_profile.j2', user = user)

# Upvoting a post will have url /vote/post/post_id?upvote=True
@app.route('/vote/<post_or_comment>/<int:id>')
@login_required
def upvote_downvote(post_or_comment, id): 
    upvote = request.args.get('upvote')
    if not upvote: 
        return 'Error'
    if upvote != 'True' and upvote != 'False': 
        return 'Error'
    if post_or_comment != 'post' and post_or_comment != 'comment': 
        return 'Error'

    vote_value = 1 if upvote == 'True' else -1
    
    voted_obj = None
    if post_or_comment == 'post':
        voted_obj = Post.query.filter_by(id = id).first()
    elif post_or_comment == 'comment':
        voted_obj = Comment.query.filter_by(id = id).first()

    if voted_obj == None: 
        return f"No such {post_or_comment} exists"


    vote = next((vote for vote in voted_obj.votes.all() if vote.user_id == current_user.id ), None)
    if vote and vote.vote_value == vote_value: 
        flash('Your previous vote is same', 'info')
    elif vote and vote.vote_value != vote_value: 
        diff = vote_value - vote.vote_value
        try:  
            vote.vote_value = vote_value
            voted_obj.votes_count += diff
            db.session.commit()
            flash('Your vote has been updated', 'info')
        except: 
            flash('Error in updating vote', 'danger')
    else: 
        vote_on = PostOrComment.post if (post_or_comment == 'post') else PostOrComment.comment
        vote = Vote(
            user_id = current_user.id,
            vote_value = vote_value,
            vote_on = vote_on
        )
        try:
            voted_obj.votes_count += vote_value
            voted_obj.votes.append(vote)
            current_user.votes.append(vote)
            db.session.add(vote)
            db.session.add(vote)
            db.session.commit()
            flash('Thanks for voting')
        except: 
            flash('Error in adding your vote')
    
    return json.dumps(voted_obj.votes_count)

def fetchAllKgpians(): 
    KGPCodes = [1355, 504, 19428, 15991, 18251]
    MAX_PAGES, USERS_PER_PAGE = 10, 200

    users = []
    try: 
        for code in KGPCodes: 
            num_pages = MAX_PAGES
            for page in range(1, MAX_PAGES + 1):
                url = f'https://codeforces.com/ratings/organization/{code}/page/{page}'
                reqData = requests.get(url).text
                html_text = requests.get(url).text
                parsed = soup(html_text, 'html.parser')

                if page == 1: 
                    ## set num_pages
                    num_users = int(
                        parsed.find('select', {'name' : 'organizationId'}).\
                            find('option', selected=True).\
                            text.split()[-1]
                    )
                    num_pages = (num_users + USERS_PER_PAGE - 1)//USERS_PER_PAGE    # ceil
                tdList = parsed.find('div', class_='ratingsDatatable').\
                    find('table').find_all('td')[1::4]

                for td in tdList: 
                    users.append(td.text.strip())

                if page == num_pages : 
                    break
    except: 
        print('Error in scraping kgpians usernames from cf')
    return users

def fetchKgpiansCfData(): 
    users = fetchAllKgpians()
    url = 'https://codeforces.com/api/user.info?handles=' + ';'.join(users)
    reqData = requests.get(url).json()

    usersDict = {}
    try: 
        if(reqData['status'] == 'FAILED'):
            print(reqData['comment'])
        elif reqData['status'] == 'OK' : 
            for data in reqData['result']: 
                usersDict[data['handle']] = data
    except: 
        print('Error in fetching users info from cf')

    return usersDict

# Leaderboard route
@app.route('/leaderboard')
def leaderboard():
    kgpians = Kgpian.query.all()
    teams = Team.query.all()
    return render_template('leaderboard.j2', kgpians=kgpians, teams = teams)

# Should be updated differently (like a cron job)
@app.route('/updateUsersList')
def updateUsersList():
    try: 
        usersDict = fetchKgpiansCfData() 
        users = Kgpian.query.all()

        for user in users:
            if user.username in usersDict: 
                user.rating = usersDict[user.username]['rating']
                user.rating = usersDict[user.username]['maxRating']
                usersDict[user.username]['updated'] = True
        
        for handle, data in usersDict.items(): 
            if 'exists' not in data:
                user = Kgpian(
                    username = handle,
                    rating = data['rating'],
                    max_rating = data['maxRating']
                )
                db.session.add(user)
        db.session.commit()
        return 'Updated the kgpians data'
    except: 
        return 'Error in updating kgpians Data'