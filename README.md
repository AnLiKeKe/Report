# Report System

报表系统是一个基于Python的Web应用程序，用于展示和分析生产数据。该系统包含多个报表模块，提供直观的数据可视化和统计分析功能。

## 功能特性

1. **IQC缺陷分析报表**
   - 提供Quartz和Soda材料的缺陷分析数据
   - 包含月度生产数、白缺陷、黑缺陷等详细统计信息
   - 支持按年份筛选数据
   - 提供供应商维度的数据分析

2. **回收版使用统计报表**
   - 展示回收版的使用情况统计
   - 包含基础信息、缺陷数量等
   - 提供图表和表格两种展示方式

## 项目结构

```
├── server.py          # 主服务器文件，处理API请求和数据逻辑
├── index.html         # 系统入口页面
├── iqc.html           # IQC缺陷分析报表页面
├── recycling.html     # 回收版使用统计报表页面
├── requirements.txt   # Python依赖包列表
├── runtime.txt        # 运行环境配置
└── .env              # 环境变量配置文件
```

## 技术栈

- **后端**: Python 3.11, FastAPI
- **数据库**: PostgreSQL (通过psycopg2连接)
- **前端**: HTML5, CSS3, JavaScript, Vue.js 3
- **图表库**: Chart.js
- **数据处理**: pandas

## 安装与运行

1. 安装依赖包:
   ```bash
   pip install -r requirements.txt
   ```

2. 配置环境变量:
   在`.env`文件中设置数据库连接信息:
   ```
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=report_system
   DB_USER=your_username
   DB_PASSWORD=your_password
   ```

3. 启动服务器:
   ```bash
   python server.py
   ```

4. 访问系统:
   在浏览器中打开 `http://localhost:8000`

## API接口

### IQC缺陷分析
- `POST /api/report` - 获取IQC报表数据
- `GET /api/years` - 获取可用年份列表

### 回收版使用统计
- `POST /api/recycling/report` - 获取回收版使用统计数据
- `GET /api/recycling` - 获取服务版使用统计数据

## 数据说明

- **Quartz材料**: 材料代码以'02'结尾的消耗品
- **Soda材料**: 材料代码以'01'结尾的消耗品
- **缺陷统计**: 包括白点缺陷(AOI检测的B类缺陷)和黑点缺陷(AOI检测的A类缺陷)
- **供应商数据**: 按供应商分组的详细统计数据