#imports
from flask import Flask, render_template,redirect,request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



#my app

app=Flask(__name__)
Scss(app)

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
db = SQLAlchemy(app)

#data class(row of data)
class mytask(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    content = db.Column(db.String(100),nullable=False)
    complete = db.Column(db.Integer,default=0)
    created = db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self):
        return f"Task {self.id}"
    
with app.app_context():
    db.create_all()


#Routes to webpages
@app.route('/',methods=["POST","GET"])
def index():
    #ADD A TASK     
    if request.method == 'POST':
        current_task = request.form.get('content')  # Corrected key retrieval
        if current_task:
            new_task = mytask(content=current_task)
            try:
                db.session.add(new_task)
                db.session.commit()
                return redirect('/')
            except Exception as e:
                print(f"ERROR: {e}")
                return f"ERROR: {e}"
    #see all current task
    else:
        tasks = mytask.query.order_by(mytask.created).all() 
        return render_template("index.html",tasks = tasks) 
    

    

#delete an item
@app.route("/delete/<int:id>")
def delete(id:int):
    delete_task=mytask.query.get_or_404(id)
    try:
        db.session.delete(delete_task)  
        db.session.commit()
        return redirect('/')
    except Exception as e:
        return f"ERROR: {e}"




#edit an item
@app.route("/edit/<int:id>",methods = ['GET','POST'])
def edit(id:int):
    task=mytask.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form.get('content',task.content)
        try:
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return f"ERROR: {e}"
    else:
        return render_template("edit.html",task=task)
    



if __name__ == "__main__":
    app.run(debug=True)