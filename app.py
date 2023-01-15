#server site
from flask import Flask
from flask_restful import Api,Resource,abort
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)


#database

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
api=Api(app)


class CityModel(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(100), nullable=False)
    temp = db.Column(db.String(100), nullable=False)
    weather = db.Column(db.String(100), nullable=False)
    people = db.Column(db.String(100), nullable=False)
# จัดformat object ใช้ represent
    def __repr__(self):
        return f"City(name={name},temp={temp},weather={weather},people={people})"

app.app_context().push()
db.create_all()

mycity={
    1:{"name":"ชลบุรี","weather":"อากาศร้อนอบอ้าว","people":1500},
    2:{"name":"ระยอง","weather":"ฝนตก","people":3000},
    "bangkok":{"name":"กรุงเทพ","weather":"พายุ","people":2000}
}

#validate request
#def notFoundCity(city_id):
 #   if city_id not in mycity:
  #      abort(404,message="ไม่พบข้อมูล")

def notFoundNameCity(name):
    if name not in mycity:
        abort(404,message="ไม่พบข้อมูล")

#design
class WeatherCity(Resource):
    def get(self,name):
    #def get(self,city_id):
        notFoundNameCity(name)
        #notFoundCity(city_id)
        return mycity[name]
        #return mycity[city_id]

    def post(self,name):
        return {"data":"Create Resource:" +name}


#call
api.add_resource(WeatherCity,"/weather/<string:name>")
#api.add_resource(WeatherCity,"/weather/<int:city_id>")

if __name__ == "__main__":
    app.run(debug=True)