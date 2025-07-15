import os
import openai
from flask import Flask, request, jsonify
from flask_cors import CORS  # 用于解决跨域问题

app = Flask(__name__)
CORS(app)  # 允许所有源跨域访问，以便前端页面可以调用后端API [oai_citation:1‡juejin.cn](https://juejin.cn/post/7297103474440732707#:~:text=2.%20%E5%9C%A8%20Flask%20%E5%BA%94%E7%94%A8%E7%A8%8B%E5%BA%8F%E4%B8%AD%E5%AF%BC%E5%85%A5%E5%B9%B6%E5%88%9D%E5%A7%8B%E5%8C%96%20Flask,%E6%89%A9%E5%B1%95%EF%BC%9A)

# 从环境变量获取 OpenAI API 密钥（请确保在部署平台上设置OPENAI_API_KEY）
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/", methods=["GET"])
def index():
    # 根路由用于健康检查或提示信息
    return "Backend is running. 请使用 /chat 接口进行交互。"

@app.route("/chat", methods=["POST"])
def chat():
    """处理聊天请求：接收JSON请求，调用OpenAI接口获取回复，返回JSON响应。"""
    data = request.get_json()
    user_message = data.get("message", "")
    if not user_message:
        # 如果请求中没有提供消息，返回错误
        return jsonify({"error": "未提供输入信息"}), 400
    try:
        # 调用OpenAI的对话接口，模型使用gpt-3.5-turbo，可以根据需要改为"gpt-4"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )
        answer = response.choices[0].message["content"]
        # 将回复内容封装为JSON返回
        return jsonify({"response": answer})
    except Exception as e:
        # 捕获调用API过程中出现的异常，避免服务器崩溃
        return jsonify({"error": f"后端错误: {str(e)}"}), 500

# 启动Flask应用（在Render部署时，会使用Gunicorn来启动，本地测试可以使用以下方式）
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
