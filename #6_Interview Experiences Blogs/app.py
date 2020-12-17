from flask import Flask, render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager
from datetime import datetime

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blogs.db'
db = SQLAlchemy(app)
migrate=Migrate(app,db)
manager=Manager(app)

manager.add_command('db',MigrateCommand)

posts_tags=db.Table('posts_tags',
                    db.Column('blog_id',db.Integer,db.ForeignKey('blog.id')),
                    db.Column('tag_id',db.Integer,db.ForeignKey('tag.id'))
)


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prelude=db.Column(db.String(100), nullable = False,default='Prelude')
    #overview=db.column(db.Text, nullable=False,default='Overview')
    overview=db.Column(db.Text)
    sl_company=db.relationship('Sl_company',backref=db.backref('scompany'), lazy=True)
    intrv_company=db.relationship('Intrv_company',backref=db.backref('icompany'), lazy=True)
    #conclusion=db.column(db.text,nullable=False,default='Conclusion')
    conclusion=db.Column(db.Text)
    tags=db.relationship('Tag',secondary=posts_tags,backref=db.backref('tags'), lazy='dynamic')
    date_posted=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return 'Blog post'+ str(self.id)

class Sl_company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sl_company=db.Column(db.String(100), nullable = False,default='Company')
    details=db.Column(db.Text,nullable=False,default='details')
    problems=db.relationship('Problem',backref=db.backref('problems'), lazy=True)
    blog_id=db.Column(db.Integer, db.ForeignKey('blog.id'))

    def __repr__(self):
        return str(self.id)

class Problem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    problem_statement=db.Column(db.Text,nullable=False,default='Problem Statement')
    sample_test_case=db.Column(db.Text,nullable=False,default='Sample Test Case')
    explaination=db.Column(db.Text,nullable=False,default='Explaination')
    expected_solution=db.Column(db.Text,nullable=False,default='Expected Solution')
    tag=db.relationship('Tag',backref=db.backref('tg'), lazy=True)
    sl_company_id=db.Column(db.Integer, db.ForeignKey('sl_company.id'))

    def __repr__(self):
        return str(self.id)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag=db.Column(db.String(100), nullable = False,default='Company')
    problem_id=db.Column(db.Integer, db.ForeignKey('problem.id'))

    def __repr__(self):
        return str(self.id)

class Intrv_company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    intrv_company=db.Column(db.String(100), nullable = False,default='Company')
    detail=db.Column(db.Text,nullable=False,default='detail')
    blog_id=db.Column(db.Integer, db.ForeignKey('blog.id'))

    def __repr__(self):
        return str(self.id)


@app.route('/blogs', methods=['GET','POST'])
def blogs():
    if request.method =='POST':
        post_prelude=request.form['prelude']
        post_overview=request.form['overview']
        post_conclusion=request.form['conclusion']
        b=Blog(prelude=post_prelude,overview=post_overview,conclusion=post_conclusion)
        post_sl_company=request.form['sl_company']
        post_details=request.form['details']
        s=Sl_company(sl_company=post_sl_company,details=post_details)
        ps=request.form['problem_statement']
        exp=request.form['explaination']
        stc=request.form['sample_test_case']
        es=request.form['expected_solution']
        p=Problem(problem_statement=ps,sample_test_case=stc,explaination=exp,expected_solution=es)
        t=request.form['tag']
        tag=Tag(tag=t)
        p.tag.append(tag)
        s.problems.append(p)
        b.sl_company.append(s)
        b.tags.append(tag)
        #b.tags.append(post_sl_company)
        post_i_company=request.form['intrv_company']
        post_detail=request.form['detail']
        i=Intrv_company(intrv_company=post_i_company,detail=post_detail)
        b.intrv_company.append(i)
        #db.session.add(t)
        #db.session.add(p)
        #db.session.add(i)
        #db.session.add(s)
        db.session.add(b)
        db.session.commit()
        return redirect('/blogs')
    else:
        title=request.args.get('title')
        tag=request.args.get('tag')
        tags=request.args.get('tags')
        page=request.args.get('page',1,type=int)
        if tag:
            all_posts=Blog.query.filter(Blog.tags.any(Tag.tag.like(tag))).order_by(Blog.date_posted).paginate(page=page,per_page=5)
        elif title:
            all_posts=Blog.query.filter(Blog.tags.any(Tag.tag.like(title))).order_by(Blog.date_posted).paginate(page=page,per_page=5)
        elif tags:
            all_posts=Blog.query.filter(Blog.tags.any(Tag.tag.like(tags))).order_by(Blog.date_posted).paginate(page=page,per_page=5)
        else:
            all_posts=Blog.query.order_by(Blog.date_posted).paginate(page=page,per_page=5)
        return render_template('blogs.html', posts=all_posts)

@app.route('/blogs/new',methods=['GET','POST'])
def new_post():
    if request.method =='POST':
        post_prelude=request.form['prelude']
        post_overview=request.form['overview']
        post_conclusion=request.form['conclusion']
        b=Blog(prelude=post_prelude,overview=post_overview,conclusion=post_conclusion)
        post_sl_company=request.form['sl_company']
        post_details=request.form['details']
        s=Sl_company(sl_company=post_sl_company,details=post_details)
        ps=request.form['problem_statement']
        exp=request.form['explaination']
        stc=request.form['sample_test_case']
        es=request.form['expected_solution']
        p=Problem(problem_statement=ps,sample_test_case=stc,explaination=exp,expected_solution=es)
        t=request.form['tag']
        tag=Tag(tag=t)
        p.tag.append(tag)
        s.problems.append(p)
        b.sl_company.append(s)
        b.tags.append(tag)
        b.tags.append(post_sl_company)
        post_i_company=request.form['intrv_company']
        post_detail=request.form['detail']
        i=Intrv_company(intrv_company=post_i_company,detail=post_detail)
        b.intrv_company.append(i)
        #db.session.add(t)
        #db.session.add(p)
        #db.session.add(i)
        #db.session.add(s)
        db.session.add(b)
        db.session.commit()
        return redirect('/blogs')
    else:
        return render_template('new.html')

@app.route('/blogs/addcompany/<int:id>',methods=['GET','POST'])
def adds(id):
    post=Blog.query.get_or_404(id)
    if method=='POST':
        post_company=request.form['sl_company']
        post_details=request.form['details']
        post_ps=request.form['problem_statement']
        post_stc=request.form['sample_test_case']
        post_exp=request.form['explaination']
        post_es=request.form['expected_solution']
        p=Problem(problem_statement=post_ps,sample_test_case=post_stc,explaination=post_exp,expected_solution=post_es)
        com=Sl_company(sl_company=post_company,details=post_details)
        com.problems.append(p)
        post.problems.append(com)
        db.session.commit()
        return redirect('/blogs')
    else:
        return render_template('addcompany.html',post=post)


@app.route('/blogs/addintrv/<int:id>',methods=['GET','POST'])
def addi(id):
    post=Blog.query.get_or_404(id)
    if method=='POST':
        post_i=request.form['intrv_company']
        post_detail=request.form['detail']
        i=Intrv_company(intrv_company=post_i,detail=post_detail)
        post.intrv_company.append(i)
        db.session.commit()
        return redirect('/blogs')
    else:
        return render_template('addintrv.html',post=post)



@app.route('/blogs/addproblem/<int:id1>/<int:id2>',methods=['GET','POST'])
def addp(id1,id2):
    company=Sl_company.query.get_or_404(id2)
    post=Blog.query.get_or_404(id1)
    if method=='POST':
        ps=request.form['problem_statement']
        stc=request.form['sample_test_case']
        exp=request.form['explaination']
        es=request.form['expected_solution']
        p=Problem(problem_statement=ps,sample_test_case=stc,explaination=exp,expected_solution=es)
        company.problems.append(p)
        post.sl_company=company
        db.session.commit()
        return redirect('/blogs')
    else:
        return render_template('addproblem.html',post=post)

@app.route('/blogs/addtag/<int:id1>/<int:id2>/<int:id3>',methods=['GET','POST'])
def addt(id1,id2,id3):
    post=Blog.query.get_or_404(id1)
    company=Sl_company.query.get_or_404(id2)
    problem=Problem.query.get_or_404(id3)
    if method=='POST':
        t=request.form['tag']
        problem.tags.append(t)
        db.session.commit()
        return redirect('/blogs')
    else:
        return render_template('addtag.html',post=post,sl_company=company,problem=problem)


if __name__=='__main__':
    app.run(debug=True)

