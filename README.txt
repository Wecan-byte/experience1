# 校园二手物品管理系统（简易版）

### 💡 项目说明
这是一个基于 Python Flask + MySQL 的简易校园二手物品管理系统，适合初学者学习。

### 📁 文件结构
- **database.sql**：MySQL 建表文件，可在 Navicat 中直接运行。
- **app.py**：Flask 后端服务文件，负责注册、添加商品、购买功能。
- **index.html**：前端页面，提供表单界面进行操作。
- **README.txt**：使用说明。

### ⚙️ 部署步骤
1. 打开 Navicat，新建数据库 `campus_used_goods`，运行 `database.sql`。
2. 安装依赖：`pip install flask pymysql`
3. 运行后端：`python app.py`
4. 打开浏览器访问：http://127.0.0.1:5000
5. 即可在页面中注册、添加商品、购买商品。
