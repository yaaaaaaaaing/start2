from flask import Flask, request, jsonify

app = Flask(__name__)

# 用于存储最新的输出信息
output_storage = {"message": "No output yet"}

@app.route('/display_output', methods=['POST'])
def display_output():
    # 接收 POST 请求中的输出信息
    output_storage["message"] = request.form.get('message', 'No message received')
    return jsonify({"status": "success", "message": "Output received!"}), 200

@app.route('/get_output', methods=['GET'])
def get_output():
    # 将存储的输出信息返回给前端
    return jsonify(output_storage), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=1234)