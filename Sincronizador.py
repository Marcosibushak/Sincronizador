import cherrypy
from cherrypy.lib import static
from cherrypy.lib.httputil import parse_query_string
from mako.template import Template
import mimetypes
import MySQLdb
import requests
import os
import os.path
import shutil
from md5 import md5
import sys
import json
reload(sys)
sys.setdefaultencoding("utf-8")
import xlrd
from xlwt import Workbook
import string
import csv
from datetime import datetime, date, time, timedelta
import calendar
import subprocess
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, wait, as_completed#Para peticiones Concurrentes
from time import time
import time
#Integracion gmail
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
import uuid
from lxml import etree
import xml.etree.ElementTree as ET
import urllib
import hashlib
from hmac import HMAC
from lxml import etree
import xml.etree.ElementTree as ET
import commands
#-------------------------------------------------------------
properties=json.loads(open('properties.json').read())
main_dir=properties['main_dir']
#headers={'Authorization':'NLAuth nlauth_account=4140678, nlauth_email=marcos@ibushak.com, nlauth_signature=M@rcos182347@@ibushak, nlauth_role=3','Content-Type':'application/json',}
headers={'Authorization':'NLAuth nlauth_account='+str(properties['netsuite']['account'])+', nlauth_email='+str(properties['netsuite']['email'])+', nlauth_signature='+str(properties['netsuite']['signature'])+', nlauth_role='+str(properties['netsuite']['role'])+'','Content-Type':'application/json',}


host=properties['data_base']['host']
db_user=properties['data_base']['user']
db_pass=properties['data_base']['password']
db_name=properties['data_base']['database_name']

db = MySQLdb.connect(host=host,user=db_user,passwd=db_pass,db=db_name)
#Direccion="13.82.229.26"
Direccion=properties['address']
Puerto=properties['ports'][0]

PATH = os.path.abspath(os.path.dirname(__file__))
class home(object):
    @cherrypy.expose
    def index(self):
        raise cherrypy.HTTPRedirect('https://www.ibushak.com/', status=301)
class api(object):
    @cherrypy.expose
    def index(self):
        cherrypy.response.status = 200
        raise cherrypy.HTTPRedirect('https://www.ibushak.com/', status=301)
    @cherrypy.expose
    @cherrypy.tools.allow(methods=['POST'])
    def access_token(self,public_key=None,secret_key=None,*args,**kwargs):
        global host
        global db_user
        global db_pass
        global db_name
        db = MySQLdb.connect(host=host,user=db_user,passwd=db_pass,db=db_name)
        PUBLIC_KEY=public_key
        PRIVATE_KEY=secret_key
        if public_key==None or secret_key==None:
            cherrypy.response.status = 400
            cherrypy.response.headers['Content-Type'] = "application/json"
            return """{"message": "Wrong number of parameters","error": "invalid_request","status": 400,"cause": []}"""
        else:
            Authorized=Valida_Credenciales(PUBLIC_KEY,PRIVATE_KEY)
            if Authorized:
                ahora=datetime.now()
                fecha=str(ahora.year)+"-"+str(ahora.month)+"-"+str(ahora.day)+"T"+time.strftime("%H:%M:%S")
                milisegundo=str(int(round(time.time()*1000)))
                concatenated = PUBLIC_KEY+milisegundo+PRIVATE_KEY
                signature=str(hashlib.sha256(concatenated).hexdigest())
                cur=db.cursor()
                SQL="INSERT INTO `"+str(db_name)+"`.`server_token_history` (`access_token`, `created`, `refresh_token`, `public_key`, `milisegundo`, `valido`) VALUES ('API_ACCT-"+str(hashlib.sha256(fecha+signature).hexdigest())+"', '"+str(fecha)+"', 'API_RT-"+str(signature)+"', '"+PUBLIC_KEY+"','"+str(milisegundo)+"','Si');"
                dbuser=cur.execute(SQL)
                db.commit()
                cur.close()
                db.close()
                cherrypy.response.status = 200
                cherrypy.response.headers['Content-Type'] = "application/json"
                #result=commands.getoutput('/usr/bin/python /home/marcosibushak/Sistemas/Token_Ibushak.py')
                return '{"access_token":"API_ACCT-'+str(hashlib.sha256(fecha+signature).hexdigest())+'","expires_in":10800,"refresh_token":"API_RT-'+str(signature)+'","status":200}'
            else:
                cherrypy.response.status = 400
                cherrypy.response.headers['Content-Type'] = "application/json"
                return '{"message": "invalid client_id or client_secret.","error": "invalid_client","status": 400,"cause": []}'
class syncer(object):
    @cherrypy.expose
    def index(self):
        raise cherrypy.HTTPRedirect('http://'+str(Direccion)+':'+str(Puerto)+'/syncer/login')
    @cherrypy.expose
    def login(self):
        global main_dir
        return open(str(main_dir)+'/src/views/index.html')
    @cherrypy.expose
    @cherrypy.tools.allow(methods=['POST'])
    def do_login(self,**kwargs):
        global main_dir
        global Direccion
        global Puerto
        USUARIO=cherrypy.request.params.get('email')
        PASSWORD=cherrypy.request.params.get('password')
        if USUARIO=="" or PASSWORD=="" or USUARIO=="mail@ibushak.com" or PASSWORD=="password":
            authorize_url='http://'+str(Direccion)+':'+str(Puerto)+'/syncer/login'
            raise cherrypy.HTTPRedirect(authorize_url)
        else:
            #access='User_can_see_Onboarding'
            users = get_users(USUARIO, PASSWORD)

            #print users
            #Access Token Ibushak
            a=json.loads(users)
            if a['status']==200:
                Token=a['access_token']
            #if users:
                authorize_url='http://'+str(Direccion)+':'+str(Puerto)+'/syncer/main'#?password='+str(Token)
                cherrypy.session['mystring'] = Token#encrypt_pw(pass_dado)
                raise cherrypy.HTTPRedirect(authorize_url)
            else:
                authorize_url='http://'+str(Direccion)+':'+str(Puerto)+'/syncer/login'
                raise cherrypy.HTTPRedirect(authorize_url)
    @cherrypy.expose
    def main(self):
        global main_dir
        global Direccion
        global Puerto
        try:
            psw=cherrypy.session['mystring']
            print psw
            if valida_token(psw)==True:
                global host
                global db_user
                global db_pass
                global db_name
                Usuario="""SELECT 
                                T1.razon_social_empresa,
                                T3.correo_usuario,
                                T2.nombre_rol
                            FROM 
                                Sincronizador.server_empresas AS T1,
                                Sincronizador.server_roles AS T2,
                                Sincronizador.server_usuarios AS T3,
                                Sincronizador.server_token_history as T4
                            WHERE
                                T4.access_token='"""+str(psw)+"""'
                                AND T3.status_usuario='Activo'
                                AND T4.public_key=T3.public_key
                                AND T2.idserver_roles=T3.rol_usuario;"""
                db = MySQLdb.connect(host=host,user=db_user,passwd=db_pass,db=db_name)
                cur = db.cursor()
                dbuser=cur.execute(Usuario)
                cur.close()
                db.close()
                if os.path.exists('/home/marcosibushak/files/Excel.xls'):
                    os.remove('/home/marcosibushak/files/Excel.xls')
                return open(str(main_dir)+'/src/views/home.html')
            else:
                authorize_url='http://'+str(Direccion)+':'+str(Puerto)+'/syncer/login'
                raise cherrypy.HTTPRedirect(authorize_url)
        except Exception as e:
            print str(e)
            authorize_url='http://'+str(Direccion)+':'+str(Puerto)+'/syncer/login'
            raise cherrypy.HTTPRedirect(authorize_url)
def Valida_Credenciales(Public,secret):
    global host
    global db_user
    global db_pass
    global db_name
    SQL="SELECT Public_Key FROM Sincronizador.server_usuarios WHERE Public_Key='"+str(Public) +"' AND Secret_Key='"+str(secret)+"';"
    #print SQL
    db = MySQLdb.connect(host=host,user=db_user,passwd=db_pass,db=db_name)
    cur = db.cursor()
    dbuser=cur.execute(SQL)
    #resultados = cur.fetchone()
    #print resultados
    cur.close()
    db.close()
    return dbuser
def valida_token(access_token):
    global host
    global db_user
    global db_pass
    global db_name

    db = MySQLdb.connect(host=host,user=db_user,passwd=db_pass,db=db_name)
    cur=db.cursor()
    dbuser=cur.execute("SELECT * FROM Sincronizador.server_token_history where access_token='"+access_token+"' and valido='Si';")
    cur.close()
    db.close()
    if dbuser:
        return True
    else:
        return False
def get_users(usuario, password):
    global host
    global db_user
    global db_pass
    global db_name
    db = MySQLdb.connect(host=host,user=db_user,passwd=db_pass,db=db_name)
    cur = db.cursor()
    print 'SELECT public_key,secret_key FROM Sincronizador.server_usuarios WHERE correo_usuario="'+str(usuario)+'" AND password_usuario="'+str(password)+'"  AND status_usuario="activo";'
    dbuser=cur.execute('SELECT public_key,secret_key FROM Sincronizador.server_usuarios WHERE correo_usuario="'+str(usuario)+'" AND password_usuario="'+str(password)+'"  AND status_usuario="activo";')
    if dbuser:
        resultados = cur.fetchall()
        for registro in resultados:
            public=registro[0]
            private=registro[1]
        url="http://"+str(Direccion)+':'+str(Puerto)+"/api/access_token?public_key="+public+"&secret_key="+private
        r=requests.request("POST", url)
        #print r.text
    else:
        url="http://"+str(Direccion)+':'+str(Puerto)+"/api/access_token?public_key=#########&secret_key=###########"
        r=requests.request("POST", url)
    cur.close()
    db.close()
    #print dbuser
    return r.text
if __name__ == '__main__':
    home=home()
    home.api=api()
    home.syncer=syncer()
    if len(properties['ports'])>1:
        # adicionamos un server extra
        from cherrypy import _cpserver
        cherrypy.engine.timeout_monitor.unsubscribe()
        if len(properties['ports'])==2:
            server = _cpserver.Server()
            server.socket_host = '0.0.0.0'
            server.socket_port = int(properties['ports'][1])
            server.subscribe()
        if len(properties['ports'])==3:
            server = _cpserver.Server()
            server.socket_host = '0.0.0.0'
            server.socket_port = int(properties['ports'][1])
            server.subscribe()
            server1 = _cpserver.Server()
            server1.socket_host = '0.0.0.0'
            server1.socket_port = int(properties['ports'][2])
            server1.subscribe()
    # Configurando el puerto por default
    cherrypy.config.update({'server.socket_host': '0.0.0.0', 'server.socket_port': int(Puerto),'server.thread_pool': 5000,'server.socket_queue_size': 5000,'response.timeout':1000000000000000,})
    cherrypy.tree.mount(home, '/',config={
        '/favicon.ico':{
            'tools.staticfile.on': True,
            'tools.staticfile.filename': '/home/marcosibushak/images/favicon.ico'
        },
        '/': {
            'tools.sessions.on': True,
            'tools.sessions.timeout':180,
        },
        '/onboarding/TableFilter': {
            'tools.staticdir.on' : True,
            'tools.staticdir.dir' : '/home/marcosibushak/Js/TableFilter_EN',
        },
        '/css':{
            'tools.staticdir.on' : True,
            'tools.staticdir.dir' : str(main_dir)+'/src/css',
        },
        '/images':{
            'tools.staticdir.on' : True,
            'tools.staticdir.dir' : str(main_dir)+'/src/assets/images',
        },
        '/fonts':{
            'tools.staticdir.on' : True,
            'tools.staticdir.dir' : '/home/marcosibushak/fonts',
        },
        '/js':{
            'tools.staticdir.on' : True,
            'tools.staticdir.dir' : str(main_dir)+'/src/js',
        },
        '/files':{
            'tools.staticdir.on' : True,
            'tools.staticdir.dir' : '/home/marcosibushak/files',
            }
        ,
        '/PlugInExcel':{
            'tools.staticdir.on' : True,
            'tools.staticdir.dir' : '/home/marcosibushak/PlugInExcel',
            }
        })
    cherrypy.engine.start()
    cherrypy.engine.block()