from flask import Flask, request, jsonify, render_template, session, redirect, url_for
import pymysql
import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # 用于会话管理的密钥

def get_db_connection():
    return pymysql.connect(host='localhost', user='root', password='123456', database='campus_used_goods', charset='utf8mb4')

@app.route('/')
def index():
    # 如果已登录，跳转到商品列表页
    if 'user_id' in session:
        return redirect(url_for('products'))
    with open('index.html', 'r', encoding='utf-8') as f:
        return f.read()

@app.route('/admin_login_page')
def admin_login_page():
    # 显示管理员登录页面
    return """
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
    <meta charset="UTF-8">
    <title>管理员登录 - 校园二手物品管理系统</title>
    <style>
        body {
            font-family: 'Microsoft YaHei', Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        .login-container {
            background-color: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            width: 100%;
            max-width: 400px;
            text-align: center;
        }
        .login-container h2 {
            color: #333;
            margin-bottom: 30px;
            font-size: 28px;
        }
        .admin-icon {
            font-size: 60px;
            margin-bottom: 20px;
            color: #f1c40f;
        }
        .form-group {
            margin-bottom: 20px;
            text-align: left;
        }
        .form-group label {
            display: block;
            margin-bottom: 8px;
            color: #555;
            font-weight: bold;
        }
        .form-group input {
            width: 100%;
            padding: 12px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
            box-sizing: border-box;
        }
        .form-group input:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 5px rgba(102, 126, 234, 0.3);
        }
        .login-btn {
            width: 100%;
            padding: 12px;
            background: linear-gradient(135deg, #f1c40f 0%, #f39c12 100%);
            color: white;
            border: none;
            border-radius: 5px;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .login-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(241, 196, 15, 0.3);
        }
        .back-link {
            display: inline-block;
            margin-top: 20px;
            color: #667eea;
            text-decoration: none;
            font-size: 14px;
        }
        .back-link:hover {
            text-decoration: underline;
        }
    </style>
    </head>
    <body>
        <div class="login-container">
            <div class="admin-icon">⚙️</div>
            <h2>管理员登录</h2>
            <form action="/admin_login" method="post">
                <div class="form-group">
                    <label for="username">管理员账号:</label>
                    <input type="text" id="username" name="username" required placeholder="请输入管理员账号">
                </div>
                <div class="form-group">
                    <label for="password">管理员密码:</label>
                    <input type="password" id="password" name="password" required placeholder="请输入管理员密码">
                </div>
                <button type="submit" class="login-btn">登录</button>
            </form>
            <a href="/" class="back-link">返回普通用户登录</a>
        </div>
    </body>
    </html>
    """

@app.route('/admin_login', methods=['POST'])
def admin_login():
    data = request.form
    conn = get_db_connection()
    cursor = conn.cursor()
    # 专门查询管理员账号
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s AND is_admin = TRUE", 
                   (data['username'], data['password']))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        session['user_id'] = user[0]  # 保存用户ID到会话
        session['username'] = user[1]  # 保存用户名到会话
        session['is_admin'] = True  # 保存管理员状态到会话
        # 添加登录日志
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO logs (user_id, action, details, log_time) VALUES (%s,%s,%s,%s)", 
                       (user[0], '管理员登录', f'管理员账号: {data["username"]}', datetime.datetime.now()))
        conn.commit()
        conn.close()
        return redirect(url_for('admin_logs'))
    else:
        return """
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
        <meta charset="UTF-8">
        <title>登录失败 - 校园二手物品管理系统</title>
        <style>
            body {
                font-family: 'Microsoft YaHei', Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            }
            .error-container {
                background-color: white;
                padding: 40px;
                border-radius: 10px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
                text-align: center;
                max-width: 400px;
            }
            .error-message {
                color: #e74c3c;
                font-size: 24px;
                margin-bottom: 20px;
            }
            .back-btn {
                display: inline-block;
                padding: 12px 30px;
                background: linear-gradient(135deg, #f1c40f 0%, #f39c12 100%);
                color: white;
                text-decoration: none;
                border-radius: 6px;
                font-weight: 600;
                transition: all 0.3s ease;
            }
            .back-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(241, 196, 15, 0.3);
            }
        </style>
        </head>
        <body>
            <div class="error-container">
                <div class="error-message">管理员账号或密码错误！</div>
                <a href="/admin_login_page" class="back-btn">返回管理员登录</a>
            </div>
        </body>
        </html>
        """

@app.route('/login', methods=['POST'])
def login():
    data = request.form
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", 
                   (data['username'], data['password']))
    user = cursor.fetchone()
    
    if user:
        session['user_id'] = user[0]  # 保存用户ID到会话
        session['username'] = user[1]  # 保存用户名到会话
        session['is_admin'] = user[6]  # 保存管理员状态到会话
        
        # 添加登录日志
        cursor.execute("INSERT INTO logs (user_id, action, details, log_time) VALUES (%s,%s,%s,%s)", 
                       (user[0], '用户登录', f'用户名: {data["username"]}', datetime.datetime.now()))
        conn.commit()
        conn.close()
        return redirect(url_for('products'))
    else:
        conn.close()
        return '登录失败，请检查用户名和密码'

@app.route('/logout')
def logout():
    # 记录退出日志
    if 'user_id' in session and session.get('is_admin'):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO logs (user_id, action, details, log_time) VALUES (%s,%s,%s,%s)", 
                       (session['user_id'], '管理员退出', f'管理员账号: {session["username"]}', datetime.datetime.now()))
        conn.commit()
        conn.close()
    session.clear()  # 清除所有会话数据
    return redirect(url_for('index'))

@app.route('/products')
def products():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    # 关联查询商品和卖家信息
    cursor.execute("""
    SELECT p.*, u.phone, u.email, u.address 
    FROM products p 
    JOIN users u ON p.seller_id = u.user_id 
    WHERE p.status = '在售'
    """)
    products = cursor.fetchall()
    conn.close()
    
    # 创建商品列表的HTML内容
    html = f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
    <meta charset="UTF-8">
    <title>商品列表 - 校园二手物品管理系统</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .header {{
            background-color: #333;
            color: white;
            padding: 10px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }}
        .header h1 {{
            margin: 0;
            font-size: 24px;
        }}
        .header .user-info {{
            font-size: 16px;
        }}
        .header a {{
            color: white;
            text-decoration: none;
            margin-left: 15px;
        }}
        .admin-section {{
            background-color: #f1c40f;
            color: #333;
            padding: 5px 10px;
            border-radius: 3px;
            font-weight: bold;
        }}
        .products-container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        .product-card {{
            background-color: white;
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 15px;
            margin-bottom: 15px;
            display: flex;
            justify-content: space-between;
        }}
        .product-info h3 {{
            margin-top: 0;
            color: #333;
        }}
        .product-price {{
            color: #e74c3c;
            font-weight: bold;
            font-size: 18px;
        }}
        .product-actions a {{
            display: inline-block;
            padding: 8px 15px;
            background-color: #3498db;
            color: white;
            text-decoration: none;
            border-radius: 3px;
            margin-top: 10px;
        }}
        .add-product-btn {{
            display: block;
            width: 200px;
            padding: 10px;
            background-color: #2ecc71;
            color: white;
            text-align: center;
            text-decoration: none;
            border-radius: 5px;
            margin-bottom: 20px;
            font-weight: bold;
        }}
    </style>
    </head>
    <body>
        <div class="header">
            <h1>校园二手物品管理系统</h1>
            <div class="user-info">
                欢迎, {session['username']} | 
                { ' <a href="/admin_logs">管理日志</a> | ' if session.get('is_admin') else '' }
                <a href="/add_product_page">添加商品</a> | 
                <a href="/logout">退出登录</a>
            </div>
        </div>
        
        <div class="products-container">
            <a href="/add_product_page" class="add-product-btn">添加新商品</a>
            
            <h2>在售商品列表</h2>
            """
    
    # 处理商品列表为空的情况
    if not products:
        html += f"""
        <div style="background-color: white; padding: 30px; text-align: center; border-radius: 5px; margin-top: 20px;">
            <h3 style="color: #777;">暂无在售商品</h3>
            <p style="color: #999; margin-bottom: 20px;">您可以添加新商品到系统中</p>
            <a href="/add_product_page" style="display: inline-block; padding: 10px 20px; background-color: #2ecc71; color: white; text-decoration: none; border-radius: 3px;">添加商品</a>
        </div>
        """
    else:
        # 添加商品卡片
        for product in products:
            # 生成管理员按钮
            admin_button = ''
            if session.get('is_admin'):
                admin_button = f"""
                    <form action="/remove_product" method="post" style="display:inline; margin-left: 10px;">
                        <input type="hidden" name="product_id" value="{product[0]}">
                        <input type="submit" value="撤销商品" style="padding: 8px 15px; background-color: #e74c3c; color: white; border: none; border-radius: 3px; cursor: pointer;">
                    </form>
                """
            
            html += f"""
            <div class="product-card">
                <div class="product-info">
                    <h3>{product[1]}</h3>
                    <p>{product[2]}</p>
                    <div class="product-price">¥{product[3]}</div>
                    <p>卖家: {product[6]}</p>
                    <p>联系方式: {product[7]}</p>
                    <p>邮箱: {product[8]}</p>
                    <p>交易地点: {product[9] if len(product) > 9 else '-'}</p>
                </div>
                <div class="product-actions">
                    <form action="/buy" method="post" style="display:inline;">
                        <input type="hidden" name="product_id" value="{product[0]}">
                        <input type="hidden" name="buyer_id" value="{session['user_id']}">
                        <input type="submit" value="立即购买" style="padding: 8px 15px; background-color: #3498db; color: white; border: none; border-radius: 3px; cursor: pointer;">
                    </form>
                    {admin_button}
                </div>
            </div>
            """
    
    # 结束HTML
    html += """
        </div>
    </body>
    </html>
    """
    
    return html

@app.route('/add_product_page')
def add_product_page():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    return f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
    <meta charset="UTF-8">
    <title>添加商品 - 校园二手物品管理系统</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .header {{
            background-color: #333;
            color: white;
            padding: 10px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }}
        .header h1 {{
            margin: 0;
            font-size: 24px;
        }}
        .header a {{
            color: white;
            text-decoration: none;
            margin-left: 15px;
        }}
        .form-container {{
            max-width: 600px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        .form-group {{
            margin-bottom: 15px;
        }}
        .form-group label {{
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }}
        .form-group input, .form-group textarea {{
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 3px;
        }}
        .form-group textarea {{
            height: 100px;
            resize: vertical;
        }}
        .submit-btn {{
            background-color: #2ecc71;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 3px;
            cursor: pointer;
            font-size: 16px;
        }}
        .submit-btn:hover {{
            background-color: #27ae60;
        }}
    </style>
    </head>
    <body>
        <div class="header">
            <h1>校园二手物品管理系统</h1>
            <div>
                <a href="/products">商品列表</a> | 
                <a href="/logout">退出登录</a>
            </div>
        </div>
        
        <div class="form-container">
            <h2>添加新商品</h2>
            <form action="/add_product" method="post">
                <input type="hidden" name="seller_id" value="{session['user_id']}">
                
                <div class="form-group">
                    <label for="name">商品名称:</label>
                    <input type="text" id="name" name="name" required>
                </div>
                
                <div class="form-group">
                    <label for="description">商品描述:</label>
                    <textarea id="description" name="description" required></textarea>
                </div>
                
                <div class="form-group">
                    <label for="price">价格:</label>
                    <input type="number" id="price" name="price" step="0.01" min="0" required>
                </div>
                
                <div class="form-group">
                    <label for="location">交易地点:</label>
                    <input type="text" id="location" name="location" required>
                </div>
                
                <button type="submit" class="submit-btn">添加商品</button>
            </form>
        </div>
    </body>
    </html>
    """

@app.route('/register', methods=['POST'])
def register():
    data = request.form
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 检查用户名是否已存在
    cursor.execute("SELECT * FROM users WHERE username = %s", (data['username'],))
    if cursor.fetchone():
        conn.close()
        return f"""
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
        <meta charset="UTF-8">
        <title>注册失败 - 校园二手物品管理系统</title>
        <style>
            body {{
                font-family: 'Microsoft YaHei', Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                background-color: #f0f2f5;
            }}
            .error-container {{
                background-color: white;
                padding: 40px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                text-align: center;
                max-width: 500px;
            }}
            .error-message {{
                color: #e74c3c;
                font-size: 24px;
                margin-bottom: 20px;
            }}
            .back-btn {{
                display: inline-block;
                padding: 12px 30px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                text-decoration: none;
                border-radius: 6px;
                font-weight: 600;
                transition: all 0.3s ease;
            }}
            .back-btn:hover {{
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
            }}
        </style>
        </head>
        <body>
            <div class="error-container">
                <div class="error-message">用户名已存在，请选择其他用户名！</div>
                <a href="/" class="back-btn">返回首页</a>
            </div>
        </body>
        </html>
        """
    
    # 检查是否是管理员注册（管理员注册时需要在密码前加admin_前缀）
    is_admin = False
    if data['password'].startswith('admin_'):
        is_admin = True
        # 移除admin_前缀
        password = data['password'][6:]
    else:
        password = data['password']
    
    # 插入新用户
    cursor.execute("INSERT INTO users (username, password, phone, email, address, is_admin) VALUES (%s,%s,%s,%s,%s,%s)",
                   (data['username'], password, data['phone'], data['email'], data['address'], is_admin))
    
    # 获取新用户ID
    user_id = cursor.lastrowid
    
    # 添加日志记录
    cursor.execute("INSERT INTO logs (user_id, action, details, log_time) VALUES (%s,%s,%s,%s)", 
                   (user_id, '用户注册', f'用户名: {data["username"]}, 是否管理员: {is_admin}', datetime.datetime.now()))
    
    conn.commit()
    conn.close()
    
    return f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
    <meta charset="UTF-8">
    <title>注册成功 - 校园二手物品管理系统</title>
    <style>
        body {{
            font-family: 'Microsoft YaHei', Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background-color: #f0f2f5;
        }}
        .success-container {{
            background-color: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: center;
            max-width: 500px;
        }}
        .success-message {{
            color: #27ae60;
            font-size: 24px;
            margin-bottom: 20px;
        }}
        .success-icon {{
            font-size: 60px;
            margin-bottom: 20px;
            color: #27ae60;
        }}
        .login-btn {{
            display: inline-block;
            padding: 12px 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-decoration: none;
            border-radius: 6px;
            font-weight: 600;
            transition: all 0.3s ease;
        }}
        .login-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
        }}
    </style>
    </head>
    <body>
        <div class="success-container">
            <div class="success-icon">✓</div>
            <div class="success-message">注册成功！</div>
            <p>您的账号已创建完成，请登录系统开始使用。</p>
            <a href="/" class="login-btn">立即登录</a>
        </div>
    </body>
    </html>
    """

@app.route('/add_product', methods=['POST'])
def add_product():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    data = request.form
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (name, description, price, seller_id, location, status) VALUES (%s,%s,%s,%s,%s,%s)",
                   (data['name'], data['description'], data['price'], data['seller_id'], data['location'], '在售'))
    
    # 获取商品ID
    product_id = cursor.lastrowid
    
    # 添加日志记录
    cursor.execute("INSERT INTO logs (user_id, action, details, log_time) VALUES (%s,%s,%s,%s)", 
                   (session['user_id'], '添加商品', f'商品ID: {product_id}, 名称: {data["name"]}, 地点: {data["location"]}', datetime.datetime.now()))
    
    conn.commit()
    conn.close()
    
    return f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
    <meta charset="UTF-8">
    <title>操作成功 - 校园二手物品管理系统</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background-color: #f5f5f5;
        }}
        .success-container {{
            background-color: white;
            padding: 40px;
            border-radius: 5px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: center;
        }}
        .success-message {{
            color: #27ae60;
            font-size: 24px;
            margin-bottom: 20px;
        }}
        .back-btn {{
            display: inline-block;
            padding: 10px 20px;
            background-color: #3498db;
            color: white;
            text-decoration: none;
            border-radius: 3px;
        }}
    </style>
    </head>
    <body>
        <div class="success-container">
            <div class="success-message">商品添加成功！</div>
            <a href="/products" class="back-btn">返回商品列表</a>
        </div>
    </body>
    </html>
    """

@app.route('/buy', methods=['POST'])
def buy_product():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    data = request.form
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 检查商品是否仍在售
    cursor.execute("SELECT status FROM products WHERE product_id = %s", (data['product_id'],))
    product_status = cursor.fetchone()
    
    if product_status and product_status[0] == '在售':
        # 创建订单
        cursor.execute("INSERT INTO orders (buyer_id, product_id, order_time, status) VALUES (%s,%s,%s,%s)", 
                       (data['buyer_id'], data['product_id'], datetime.datetime.now(), '待发货'))
        # 更新商品状态为已售出
        cursor.execute("UPDATE products SET status = '已售出' WHERE product_id = %s", (data['product_id'],))
        
        # 获取商品信息
        cursor.execute("SELECT name, seller_id FROM products WHERE product_id = %s", (data['product_id'],))
        product_info = cursor.fetchone()
        
        # 添加日志记录
        cursor.execute("INSERT INTO logs (user_id, action, details, log_time) VALUES (%s,%s,%s,%s)", 
                       (session['user_id'], '购买商品', f'商品ID: {data["product_id"]}, 名称: {product_info[0]}, 卖家ID: {product_info[1]}', datetime.datetime.now()))
        
        conn.commit()
        conn.close()
        
        return f"""
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
        <meta charset="UTF-8">
        <title>操作成功 - 校园二手物品管理系统</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                background-color: #f5f5f5;
            }}
            .success-container {{
                background-color: white;
                padding: 40px;
                border-radius: 5px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                text-align: center;
            }}
            .success-message {{
                color: #27ae60;
                font-size: 24px;
                margin-bottom: 20px;
            }}
            .back-btn {{
                display: inline-block;
                padding: 10px 20px;
                background-color: #3498db;
                color: white;
                text-decoration: none;
                border-radius: 3px;
            }}
        </style>
        </head>
        <body>
            <div class="success-container">
                <div class="success-message">下单成功！</div>
                <a href="/products" class="back-btn">返回商品列表</a>
            </div>
        </body>
        </html>
        """
    else:
        conn.close()
        return f"""
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
        <meta charset="UTF-8">
        <title>操作失败 - 校园二手物品管理系统</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                background-color: #f5f5f5;
            }}
            .error-container {{
                background-color: white;
                padding: 40px;
                border-radius: 5px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                text-align: center;
            }}
            .error-message {{
                color: #e74c3c;
                font-size: 24px;
                margin-bottom: 20px;
            }}
            .back-btn {{
                display: inline-block;
                padding: 10px 20px;
                background-color: #3498db;
                color: white;
                text-decoration: none;
                border-radius: 3px;
            }}
        </style>
        </head>
        <body>
            <div class="error-container">
                <div class="error-message">商品已被售出，无法购买！</div>
                <a href="/products" class="back-btn">返回商品列表</a>
            </div>
        </body>
        </html>
        """

@app.route('/admin_logs')
def admin_logs():
    # 检查是否是管理员登录
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('products'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 查询所有日志记录，关联用户信息
    cursor.execute("""
    SELECT l.*, u.username 
    FROM logs l 
    JOIN users u ON l.user_id = u.user_id 
    ORDER BY l.log_time DESC
    """)
    logs = cursor.fetchall()
    conn.close()
    
    # 创建管理员日志页面的HTML内容
    html = f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
    <meta charset="UTF-8">
    <title>管理员日志 - 校园二手物品管理系统</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .header {{
            background-color: #333;
            color: white;
            padding: 10px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }}
        .header h1 {{
            margin: 0;
            font-size: 24px;
        }}
        .header a {{
            color: white;
            text-decoration: none;
            margin-left: 15px;
        }}
        .logs-container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        .log-table {{
            width: 100%;
            border-collapse: collapse;
        }}
        .log-table th, .log-table td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        .log-table th {{
            background-color: #f2f2f2;
            font-weight: bold;
        }}
        .log-table tr:hover {{
            background-color: #f5f5f5;
        }}
        .action-badge {{
            display: inline-block;
            padding: 3px 8px;
            border-radius: 3px;
            font-size: 12px;
            font-weight: bold;
        }}
        .action-register {{
            background-color: #e3f2fd;
            color: #1976d2;
        }}
        .action-add {{
            background-color: #e8f5e9;
            color: #388e3c;
        }}
        .action-buy {{
            background-color: #fff3e0;
            color: #f57c00;
        }}
    </style>
    </head>
    <body>
        <div class="header">
            <h1>校园二手物品管理系统</h1>
            <div>
                欢迎管理员, {session['username']} | 
                <a href="/products">商品列表</a> | 
                <a href="/logout">退出登录</a>
            </div>
        </div>
        
        <div class="logs-container">
            <h2>商品买卖日志</h2>
            <table class="log-table">
                <thead>
                    <tr>
                        <th>日志ID</th>
                        <th>操作用户</th>
                        <th>操作类型</th>
                        <th>详细信息</th>
                        <th>操作时间</th>
                    </tr>
                </thead>
                <tbody>
    """
    
    # 添加日志记录行
    for log in logs:
        # 根据操作类型设置徽章样式
        action_class = ''
        if '注册' in log[2]:
            action_class = 'action-register'
        elif '添加商品' in log[2]:
            action_class = 'action-add'
        elif '购买商品' in log[2]:
            action_class = 'action-buy'
        
        html += f"""
                    <tr>
                        <td>{log[0]}</td>
                        <td>{log[5]}</td>
                        <td><span class="action-badge {action_class}">{log[2]}</span></td>
                        <td>{log[3] if log[3] else '-'}</td>
                        <td>{log[4]}</td>
                    </tr>
        """
    
    # 结束HTML
    html += """
                </tbody>
            </table>
        </div>
    </body>
    </html>
    """
    
    return html

@app.route('/remove_product', methods=['POST'])
def remove_product():
    # 检查是否是管理员
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('products'))
    
    data = request.form
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 获取商品信息
    cursor.execute("SELECT name, seller_id FROM products WHERE product_id = %s AND status = '在售'", (data['product_id'],))
    product_info = cursor.fetchone()
    
    if product_info:
        # 更新商品状态为已撤销
        cursor.execute("UPDATE products SET status = '已撤销' WHERE product_id = %s", (data['product_id'],))
        
        # 添加日志记录
        cursor.execute("INSERT INTO logs (user_id, action, details, log_time) VALUES (%s,%s,%s,%s)", 
                       (session['user_id'], '撤销商品', f'管理员撤销商品ID: {data["product_id"]}, 名称: {product_info[0]}, 卖家ID: {product_info[1]}', datetime.datetime.now()))
        
        conn.commit()
        conn.close()
        
        return f"""
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
        <meta charset="UTF-8">
        <title>操作成功 - 校园二手物品管理系统</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                background-color: #f5f5f5;
            }}
            .success-container {{
                background-color: white;
                padding: 40px;
                border-radius: 5px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                text-align: center;
            }}
            .success-message {{
                color: #27ae60;
                font-size: 24px;
                margin-bottom: 20px;
            }}
            .back-btn {{
                display: inline-block;
                padding: 10px 20px;
                background-color: #3498db;
                color: white;
                text-decoration: none;
                border-radius: 3px;
            }}
        </style>
        </head>
        <body>
            <div class="success-container">
                <div class="success-message">商品撤销成功！</div>
                <a href="/products" class="back-btn">返回商品列表</a>
            </div>
        </body>
        </html>
        """
    else:
        conn.close()
        return f"""
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
        <meta charset="UTF-8">
        <title>操作失败 - 校园二手物品管理系统</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                background-color: #f5f5f5;
            }}
            .error-container {{
                background-color: white;
                padding: 40px;
                border-radius: 5px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                text-align: center;
            }}
            .error-message {{
                color: #e74c3c;
                font-size: 24px;
                margin-bottom: 20px;
            }}
            .back-btn {{
                display: inline-block;
                padding: 10px 20px;
                background-color: #3498db;
                color: white;
                text-decoration: none;
                border-radius: 3px;
            }}
        </style>
        </head>
        <body>
            <div class="error-container">
                <div class="error-message">商品不存在或已被处理！</div>
                <a href="/products" class="back-btn">返回商品列表</a>
            </div>
        </body>
        </html>
        """

if __name__ == '__main__':
    app.run(debug=True)
