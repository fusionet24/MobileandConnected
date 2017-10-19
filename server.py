import tornado.httpserver#import http server
import tornado.ioloop#import io
import tornado.web#import web
import sqlite3#import sql lite
import sys#import system
############################################################################################################################################
_db = sqlite3.connect('sensor.db')#connect to sensor database
portnumber = 30002#portnumber
_cursor = _db.cursor()#database cursor
################DELETE#######################################################################################################################
class sensorRequestHandler(tornado.web.RequestHandler):
        def delete(self):
                try:
                        _cursor.execute("DROP TABLE IF EXISTS data")#Drop table if exists
                        _cursor.execute("CREATE TABLE data (ID INT, value REAL, time INT)") #Create a NEW TABLE
                        _db.commit()#Commit the changes to db
                        self.write('OK')#Return OKAY
                        print('Server Delete Request')#Output to Console
                except:
                        print('Error With Delete Request from ' + self.request.remote_ip)
                        self.write('Error')
################GET###########################################################################################################################
        def get(self, ID):
                try:
                        range = self.get_argument("range",default="0,"+str(sys.maxint)).split(',')#get rangage arguement, defeault arguement and spilt of string
                        params = [ID]+range #get parameter range
                        _cursor.execute("SELECT * FROM data WHERE ID=? AND time>=? AND time<=?", params)#select data from data base
                        records = [] #new records array
                        for row in _cursor:#For loop for cursor
                                records = {'ID':row[0],'temp':row[1],'time':row[2]}# get each record in request
                        self.write(tornado.escape.json_encode(records))# write out json to client
                        print('GET REQUEST from '+ self.request.remote_ip)# Show Connection from user IP 
                except:
                        print('ERROR')
                        self.write('Error')
###############PUT###########################################################################################################################
        def put(self,ID):
                try:
                        record = (int(ID), float(self.get_argument("value")), int(self.get_argument("time")))#Gets record arguements from put HTTP send
                        _cursor.execute("INSERT INTO data VALUES (?,?,?)",record)#Inputs into Database
                        _db.commit()#Commit to db
                        self.write('OK')#Write OKAY to client
                        print('PUT REQUEST from ' + self.request.remote_ip)# Show connection from user IP
                except:
                        print("Error")
                        self.write('ERROR')
#############################################################################################################################################
application = tornado.web.Application([
        (r"/sensors/all", sensorRequestHandler),#URI TEMPLATES
        (r"/sensor/([0-9]+)", sensorRequestHandler),#URI TEMPLATES
])
#############################################################################################################################################
if __name__ == "__main__":#Main function
        http_server = tornado.httpserver.HTTPServer(application)
        http_server.listen(portnumber)
        print('RESTFUL TEMPERATURE PI Sensor SERVER RUNNING')
        tornado.ioloop.IOLoop.instance().start()
