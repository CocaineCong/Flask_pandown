from flask import Blueprint, request
from jinja2 import Template
import os
import re
import codecs

tools = Blueprint("tools", __name__, url_prefix="/tools")
start_number = 34


@tools.route('/state')
def state():
    '''
    把前端的ts转为后端的py
    :return:
    '''
    '''
    export enum StateCode  {
    susad=34,
    easdsa,
    a,
    asd,




}
    '''
    check_set = set(["export", "enum", "StateCode"])
    word = request.args.get("word")

    word_list = re.findall(r"\w+", word)

    word_list.pop(4)
    print(word_list)
    if set(word_list) > check_set:
        word_list = [(x + start_number, y) for x, y in enumerate(word_list[3:])]
        # return jsonify("index.html")
        template = Template("""from util.api_base import API_exception
start_enum_number = {{start_number}}
class State_code:
            {% for i,k in word %}
    {{k}}={{i}},
{% endfor %}
#批量生成相应的函数
{% for i,k in word %}
        {% if k=="success" %}
def {{k}}_api(data={},msg="一些错误发生了",debug_msg=None,http_code=200):
    
    raise API_exception(debug_msg=debug_msg, http_code=http_code, data=data, state=State_code.{{k}})		
	    {% elif k=="error" %}
def {{k}}_api(msg="一些错误发生了",debug_msg=None):
    
    raise API_exception(msg=msg,debug_msg=debug_msg,state=State_code.{{k}},http_code =400)		
	    {% else %}
def {{k}}_api(data={},msg="一些错误发生了",debug_msg=None,http_code=200):
    raise API_exception(debug_msg=debug_msg, http_code=http_code, data=data, state=State_code.{{k}})
	    {% endif %}
	

{% endfor %} 
      """)
        c = template.render(word=word_list, start_number=start_number)

        print(os.getcwd())
        with codecs.open("util/custom_status.py", encoding="utf-8", mode="w") as fp:
            fp.write(c)
        return "写入成功"
    else:
        return "不符合预定"
