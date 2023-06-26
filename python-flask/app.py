from flask import request
from flask_cors import *

from json_flask import JsonFlask
from json_response import JsonResponse
from db import *

import json

# 创建视图应用，使用改造后的JsonFlask对象
app = JsonFlask(__name__)

# 解决跨域
CORS(app, supports_credentials=True)

# 数据库连接对象
db = SQLManager()

# 编写视图函数，绑定路由
@app.route("/all", methods=["GET"])  # 查询（全部）
def all():
    result = db.get_list(sql='select * from user')
    return JsonResponse.success(msg='查询成功', data=result)


@app.route("/add", methods=["POST"])  # 添加（单个）
def add():
    data = json.loads(request.data)  # 将json字符串转为dict
    isOk = db.modify(sql='insert into user(name,age,sex) values(%s,%s,%s)',
                      args=[data['name'], data['age'], data['sex']])
    # python三元表达式
    return JsonResponse.success(msg='添加成功') if isOk else JsonResponse.fail(msg='添加失败')


@app.route("/update", methods=["PUT"])  # 修改（单个）
def update():
    # request.data获取请求体数据
    # 前端在发送请求时，由于指定了Content-Type为application/json；故request.data获取到的就是json数据
    data = json.loads(request.data)  # 将json字符串转为dict
    if 'id' not in data:
        return JsonResponse.fail(msg='需要传入id')
    isOk = db.modify(sql='update user set name=%s,age=%s,sex=%s where id=%s',
                      args=[data['name'], data['age'], data['sex'], data['id']])
    return JsonResponse.success(msg='修改成功') if isOk else JsonResponse.fail(msg='修改失败')


@app.route("/delete", methods=["DELETE"])  # 删除（单个）
def delete():   
    # request.args获取请求链接中 ? 后面的所有参数；以字典的方式存储
    if 'id' not in request.args:
        return JsonResponse.fail(msg='需要传入id')
    isOk = db.modify(sql='delete from user where id=%s', args=[request.args['id']])
    return JsonResponse.success(msg='删除成功') if isOk else JsonResponse.fail(msg='删除失败')



# 运行flask：默认是8000端口，开启debug模式
if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)
