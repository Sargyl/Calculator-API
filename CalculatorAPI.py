import os
from flask import Flask, request, jsonify
import math

app = Flask(__name__)
history = []
MAX_LOG_SIZE = 50

def check_integer(num):
    return isinstance(num, int) or (isinstance(num, float) and num.is_integer())

@app.route("/")
def calculator():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Калькулятор-Учебная практика</title>
        <meta charset="UTF-8">
        <style>
            body {
                font-family: Arial;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background: #f5f5f5;
            }
            .calculator {
                background: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            .display {
                width: 100%;
                height: 60px;
                font-size: 24px;
                text-align: right;
                padding: 10px;
                margin-bottom: 15px;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
            .buttons {
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 10px;
                margin-bottom: 20px;
            }
            button {
                padding: 15px;
                font-size: 18px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            .num { background: #e0e0e0; }
            .op { background: #ff9800; color: white; }
            .func { background: #2196f3; color: white; }
            .equals { background: #4caf50; color: white; grid-column: span 2; }
            .log {
                margin-top: 20px;
                background: white;
                padding: 15px;
                border-radius: 10px;
            }
            .log-item {
                padding: 8px;
                border-bottom: 1px solid #eee;
            }
        </style>
    </head>
    <body>
        <div class="calculator">
            <h2>Калькулятор</h2>
            <input type="text" class="display" id="screen" readonly>
            
            <div class="buttons">
                <button class="func" onclick="clearScreen()">C</button>
                <button class="func" onclick="addSymbol('√')">√</button>
                <button class="func" onclick="addSymbol('!')">!</button>
                <button class="op" onclick="addSymbol('/')">/</button>
                
                <button class="num" onclick="addSymbol('7')">7</button>
                <button class="num" onclick="addSymbol('8')">8</button>
                <button class="num" onclick="addSymbol('9')">9</button>
                <button class="op" onclick="addSymbol('*')">×</button>
                
                <button class="num" onclick="addSymbol('4')">4</button>
                <button class="num" onclick="addSymbol('5')">5</button>
                <button class="num" onclick="addSymbol('6')">6</button>
                <button class="op" onclick="addSymbol('-')">-</button>
                
                <button class="num" onclick="addSymbol('1')">1</button>
                <button class="num" onclick="addSymbol('2')">2</button>
                <button class="num" onclick="addSymbol('3')">3</button>
                <button class="op" onclick="addSymbol('+')">+</button>
                
                <button class="num" onclick="addSymbol('0')">0</button>
                <button class="num" onclick="addSymbol('.')">.</button>
                <button class="func" onclick="addSymbol('^')">^</button>
                <button class="equals" onclick="calculate()">=</button>
            </div>
            
            <div id="message" style="color:red; display:none;"></div>
        </div>
        
        <div class="log">
            <h3>История вычислений</h3>
            <div id="logList">
                <div style="color:#999; text-align:center;">Здесь появятся предыдущие операции</div>
            </div>
            <button onclick="clearLog()" style="margin-top:10px; padding:8px;">Очистить историю</button>
        </div>

        <script>
            let expression = '';
            
            function addSymbol(sym) {
                expression += sym;
                document.getElementById('screen').value = expression;
                hideMessage();
            }
            
            function clearScreen() {
                expression = '';
                document.getElementById('screen').value = '';
                hideMessage();
            }
            
            function hideMessage() {
                document.getElementById('message').style.display = 'none';
            }
            
            async function calculate() {
                if (!expression) {
                    showMessage('Введите выражение');
                    return;
                }
                
                let num1, num2, operation;
                
                try {
                    if (expression.includes('√')) {
                        num1 = parseFloat(expression.replace('√', ''));
                        operation = 'sqrt';
                    } else if (expression.includes('!')) {
                        num1 = parseInt(expression.replace('!', ''));
                        operation = 'fact';
                    } else if (expression.includes('^')) {
                        const parts = expression.split('^');
                        num1 = parseFloat(parts[0]);
                        num2 = parseFloat(parts[1]);
                        operation = '^';
                    } else {
                        const ops = ['+', '-', '*', '/'];
                        let op = null;
                        for (let operator of ops) {
                            if (expression.includes(operator)) {
                                op = operator;
                                break;
                            }
                        }
                        if (op) {
                            const parts = expression.split(op);
                            num1 = parseFloat(parts[0]);
                            num2 = parseFloat(parts[1]);
                            operation = op;
                        } else {
                            throw new Error('Неизвестная операция');
                        }
                    }
                    
                    const response = await fetch('/calculate', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({ 
                            a: num1, 
                            b: num2, 
                            op: operation 
                        })
                    });
                    
                    const data = await response.json();
                    
                    if (response.ok) {
                        document.getElementById('screen').value = data.result;
                        expression = data.result.toString();
                        updateLog();
                    } else {
                        showMessage('Ошибка: ' + data.error);
                    }
                    
                } catch (err) {
                    showMessage('Ошибка: ' + err.message);
                }
            }
            
            function showMessage(text) {
                const msg = document.getElementById('message');
                msg.textContent = text;
                msg.style.display = 'block';
            }
            
            async function updateLog() {
                try {
                    const response = await fetch('/log');
                    const log = await response.json();
                    const list = document.getElementById('logList');
                    
                    if (log.length === 0) {
                        list.innerHTML = '<div style="color:#999; text-align:center;">История пуста</div>';
                        return;
                    }
                    
                    list.innerHTML = log.map(item => 
                        `<div class="log-item">${item.a} ${item.op} ${item.b || ''} = ${item.result}</div>`
                    ).join('');
                } catch (err) {
                    console.error('Ошибка загрузки истории:', err);
                }
            }
            
            function clearLog() {
                if (confirm('Очистить историю?')) {
                    fetch('/clear_log', { method: 'POST' })
                        .then(updateLog);
                }
            }
            
            document.addEventListener('keydown', function(e) {
                if (e.key >= '0' && e.key <= '9') addSymbol(e.key);
                else if (['+','-','*','/','.','^','!'].includes(e.key)) addSymbol(e.key);
                else if (e.key === 'Enter') calculate();
                else if (e.key === 'Escape') clearScreen();
                else if (e.key === 'Backspace') {
                    expression = expression.slice(0, -1);
                    document.getElementById('screen').value = expression;
                }
            });
            
            updateLog();
        </script>
    </body>
    </html>
    '''

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

