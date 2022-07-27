# import os
# version = "-v2"
# sha_code = "d20866994a4668e83a6db022cfcfb3777d2cd41ca236ebdd72331e5bf4c53b05152e74a5062c2b2c3dc2ea010fef88d4791d74628de81ede7935aba746078208"
# start_dire = r"D:\decode\python3\SecureCRTCipher.py dec "+version+" "+sha_code
# r = os.system("python %s" %start_dire)
import datetime
from flask import *
import json
import os

app = Flask("__name__", template_folder='./')

@app.route('/')
def index():
    return render_template("decode.html")

@app.after_request
def cors(environ):
    environ.headers['Access-Control-Allow-Origin'] = '*'
    environ.headers['Access-Control-Allow-Method'] = '*'
    environ.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return environ

@app.route("/login", methods=["POST"])
def login():
    # 获取前端json数据
    data = request.get_data()
    print(data)
    json_data = json.loads(data)
    print(json_data)

    id_user = json_data.get("userId")
    password = json_data.get("password")
    print("userId is " + id_user)
    print("password is " + password)

    # 给前端传输json数据
    info = dict()
    info['status'] = 'success'
    info['time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return jsonify(info)

@app.route("/decode", methods=["POST"])
def decode():
    # 获取前端json数据
    data = request.get_data()
    print(data)
    json_data = json.loads(data)
    print(json_data)

    version = json_data.get("version")
    sha_code = json_data.get("sha_code")
    start_dire = r"D:\decode\python3\SecureCRTCipher.py dec " + version + " " + sha_code
    cmd = os.popen("python %s" % start_dire)
    code1 = cmd.read()
    code = code1.strip('\n')
    print("version is " + version)
    print("sha_code is " + sha_code)
    print("code is " + code)
    # 给前端传输json数据
    info = dict()
    info['version'] = version
    info['sha_code'] = sha_code
    info['code'] = code
    return jsonify(info)

if __name__ == '__main__':
    app.run(port=8899, host='10.21.36.50',debug=True)  # 此处可自定义使用端口