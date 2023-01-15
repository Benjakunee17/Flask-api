#server site
from flask import Flask
from flask_restful import Api,Resource,abort,reqparse,marshal_with,fields
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

#request parser
city_add_args=reqparse.RequestParser()
city_add_args.add_argument("name",type=str,required=True,help="กรุณาป้อนชื่อจังหวัดเป็นตัวอักษร")
city_add_args.add_argument("temp",type=str,required=True,help="กรุณาป้อนอุณหภูมิเป็นตัวอักษร")
city_add_args.add_argument("weather",type=str,required=True,help="กรุณาป้อนสภาพอากาศเป็นตัวอักษร")
city_add_args.add_argument("people",type=str,required=True,help="กรุณาป้อนจำนวนประชากรเป็นตัวอักษร")

#update parse
city_update_args=reqparse.RequestParser()
city_update_args.add_argument("name",type=str,required=True,help="กรุณาป้อนชื่อจังหวัดที่ต้องการแก้ไข")
city_update_args.add_argument("temp",type=str,required=True,help="กรุณาป้อนอุณหภูมิที่ต้องการแก้ไข")
city_update_args.add_argument("weather",type=str,required=True,help="กรุณาป้อนสภาพอากาศที่ต้องการแก้ไข")
city_update_args.add_argument("people",type=str,required=True,help="กรุณาป้อนจำนวนประชากรที่ต้องการแก้ไข")

resource_field = {
    "id":fields.Integer,
    "name":fields.String,
    "temp":fields.String,
    "weather":fields.String,
    "people":fields.String
}
mycity={
    1:{"name":"ชลบุรี","weather":"อากาศร้อนอบอ้าว","people":1500},
    2:{"name":"ระยอง","weather":"ฝนตก","people":3000},
    "bangkok":{"name":"กรุงเทพ","weather":"พายุ","people":2000}
}


#validate request
#def notFoundCity(city_id):
#    if city_id not in mycity:
#        abort(404,message="ไม่พบข้อมูล")

#def notFoundNameCity(name):
#    if name not in mycity:
#       abort(404,message="ไม่พบข้อมูล")

#design
class WeatherCity(Resource):

    @marshal_with(resource_field)
    def get(self,city_id):
        result = CityModel.query.filter_by(id=city_id).first()
        if not result:
            abort(404,message="ไม่พบนะ")
        return result


    #def get(self,city_id):
        #notFoundNameCity(city_id)
        #notFoundCity(city_id)
        #return mycity[name]
        #return mycity[city_id]

 #connect database
    @marshal_with(resource_field)
    def post(self,city_id):
        result = CityModel.query.filter_by(id=city_id).first()
        if result:
            abort(409,message="รหัสนี้ซ้ำแล้ว")
        args=city_add_args.parse_args()
        city=CityModel(id=city_id,name=args["name"],temp=args["temp"],weather=args["weather"],people=args["people"])
        db.session.add(city)
        db.session.commit()
        return city,201

    

        #return {"data":"Create Resource:" +name}
    @marshal_with(resource_field)
    def patch(self,city_id):
        args=city_update_args.parse_args()
        result = CityModel.query.filter_by(id=city_id).first()
        if not result:
            abort(404,message="ไม่พบจังหวัดที่จะแก้ไข")
        if args["name"]:
            result.name=args["name"]
        if args["temp"]:
            result.temp=args["temp"]
        if args["weather"]:
            result.weather=args["weather"]
        if args["people"]:
            result.people=args["people"]

        db.session.commit() 
        return result
        


#call
api.add_resource(WeatherCity,"/weather/<int:city_id>")
#api.add_resource(WeatherCity,"/weather/<int:city_id>")

if __name__ == "__main__":
    app.run(debug=True)