import pymysql

# 数据库连接配置
config = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'charset': 'utf8mb4'
}

# 读取SQL文件内容
with open('database.sql', 'r', encoding='utf-8') as f:
    sql_commands = f.read()

# 分割SQL命令
commands = sql_commands.split(';')

# 连接到MySQL服务器
connection = pymysql.connect(**config)
cursor = connection.cursor()

try:
    # 执行每个SQL命令
    for command in commands:
        command = command.strip()
        if command:
            # 如果是创建数据库的命令，需要特殊处理
            if command.lower().startswith('create database'):
                # 先选择默认数据库
                cursor.execute('USE mysql')
                cursor.execute(command)
            # 如果是使用数据库的命令
            elif command.lower().startswith('use'):
                cursor.execute(command)
            else:
                cursor.execute(command)
    
    print("数据库和表创建成功！")
    
    # 创建一个管理员用户（默认账号密码）
    cursor.execute("""
    INSERT INTO users (username, password, phone, email, address, is_admin) 
    VALUES ('admin', 'admin123', '13800138000', 'admin@example.com', '管理员办公室', TRUE)
    """)
    
    # 创建一个测试用户
    cursor.execute("""
    INSERT INTO users (username, password, phone, email, address, is_admin) 
    VALUES ('testuser', '123456', '13900139000', 'test@example.com', '学生宿舍', FALSE)
    """)
    
    connection.commit()
    print("默认用户创建成功：")
    print("  管理员账号：admin，密码：admin123")
    print("  测试账号：testuser，密码：123456")
    
    # 创建一些测试商品数据
    cursor.execute("""
    INSERT INTO products (name, description, price, seller_id, location, status) 
    VALUES ('全新笔记本电脑', '未拆封的笔记本电脑，配置高', 5999.00, 1, '教学楼A区', '在售')
    """)
    
    cursor.execute("""
    INSERT INTO products (name, description, price, seller_id, location, status) 
    VALUES ('二手教材', '九成新的专业教材，无笔记', 50.00, 2, '图书馆', '在售')
    """)
    
    connection.commit()
    print("测试商品数据创建成功")
    
except Exception as e:
    print(f"执行SQL时出错：{e}")
    connection.rollback()
finally:
    # 关闭连接
    cursor.close()
    connection.close()