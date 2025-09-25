import os
from flask import Flask, request, jsonify, render_template
import math

app = Flask(__name__)
history = []
MAX_LOG_SIZE = 50

def check_integer(num):
    return isinstance(num, int) or (isinstance(num, float) and num.is_integer())

@app.route("/")
def calculator():
    return render_template('calculator.html')

@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.json
    
    if not data or "op" not in data:
        return jsonify({"error": "Не указана операция"}), 400
        
    operation = data["op"]
    a = data.get("a")
    b = data.get("b")
    
    try:
        if operation == "+":
            result = a + b
        elif operation == "-":
            result = a - b
        elif operation == "*":
            result = a * b
        elif operation == "/":
            if b == 0:
                return jsonify({"error": "Деление на ноль"}), 400
            result = a / b
        elif operation == "^":
            result = a ** b
        elif operation == "sqrt":
            if a < 0:
                return jsonify({"error": "Корень из отрицательного числа"}), 400
            result = math.sqrt(a)
        elif operation == "fact":
            if a < 0 or not check_integer(a):
                return jsonify({"error": "Факториал только для целых >= 0"}), 400
            if a > 100:
                return jsonify({"error": "Слишком большое число"}), 400
            result = math.factorial(int(a))
        else:
            return jsonify({"error": "Неизвестная операция"}), 400
            
    except Exception as e:
        return jsonify({"error": f"Ошибка вычисления: {str(e)}"}), 400
    
    record = {"a": a, "b": b, "op": operation, "result": result}
    history.append(record)
    
    if len(history) > MAX_LOG_SIZE:
        history.pop(0)
    
    return jsonify(record)

@app.route("/log")
def get_log():
    return jsonify(history[::-1])

@app.route("/clear_log", methods=["POST"])
def clear_log():
    history.clear()
    return jsonify({"status": "История очищена"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=False)


