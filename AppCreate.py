from flask import Flask,render_template,redirect,url_for,request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///user.db'#Specify the dtabase name
db = SQLAlchemy(app)

class User(db.Model):

    id = db.Column('id', db.Integer, primary_key=True)  # table attributes which is create in databse User
    username = db.Column(db.String(100))
    email = db.Column(db.String(12))
    password = db.Column(db.String(10))
    confirm = db.Column(db.String(10))


    def __init__(self,username,email,password,confirm):#A constructor for assigning values

        self.username=username
        self.email=email
        self.password=password
        self.confirm=confirm

    def __str__(self):
        return '''
                \n\n###########User-Details################\n
                EMAIL : {}  \n
                USERNAME : {}  \n
                PASSWORD : {}  \n
                CONFIRM: {}  \n
                
                '''.format(self.username,self.email,self.password,self.confirm)



@app.route('/')
@app.route('/home')
def show_login_page():
    return render_template('Loginpage.html')

@app.route('/user',methods=['GET','POST'])
def new_user_reg():
   return render_template('Newuser.html')


@app.route('/info',methods=['GET','POST'])#info written on
def get_data():
        print('***********************************************************************')
        print(request.form)
        user = User(request.form['username'],request.form['email'],request.form['password'],request.form['confirm'])

        #user1 = (request.form)
        #print("the data is", user1)
        db.session.add(user)
        db.session.commit()
        list = User.query.filter_by().all()
        return render_template('regsuccess.html', records=list, msg='Register suceessfully')

@app.route('/edit',methods=['GET','POST'])
def edit():
    if request.method == 'POST':
        updateuser = User.query.filter_by(id=request.form['editid']).first()
        updateuser.username = request.form['username']
        updateuser.email = request.form['email']
        updateuser.password = request.form['password']
        updateuser.confirm= request.form['confirm']
        updateuser.password = request.form['password']
        db.session.commit()
        userlist = User.query.all()
        return render_template('showdata.html', msg="User is Updated", records=userlist)
    uid = request.args.get('id')
    uinfo = User.query.filter_by(id=uid).all()
    return render_template('Newuser.html',records=uinfo)


@app.route('/show',methods=['GET','POST'])#show written in login page
def Login_cre():

    if request.method=='POST':

        ulist = User.query.filter_by(username=request.form['username']).all()
        print("*******************************************************************")
        print('login ho re baba')
        for u in ulist:
            if u.username == request.form['username'] and u.password == request.form['password']:
                userlist = User.query.all()
                return render_template('showdata.html',records=userlist,msg='Login successfullys')
        else:
            return redirect(url_for('show_login_page',msg='invalid credential'))

    uid = request.args.get('delid')
    if uid:
        deleteuser = User.query.filter_by(id=uid).first()
        db.session.delete(deleteuser)
        db.session.commit()
        userlist1 = User.query.all()
        return render_template('showdata.html', msg="User is Deleted", records=userlist1)


if __name__ == '__main__':
    db.create_all()

    app.run(debug=True)