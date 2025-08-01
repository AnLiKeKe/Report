import http.server
import socketserver
from socketserver import ThreadingMixIn
import json
import random
import os
from io import BytesIO
from urllib.parse import urlparse
from datetime import datetime, timedelta
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'report_system'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'your_password')
}

# Database connection function
def get_db_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Database connection failed: {e}")
        return None

class ReportSystemHandler(http.server.SimpleHTTPRequestHandler):
    def send_head(self):
        # 重写send_head设置HTML文件头
        path = self.translate_path(self.path)
        if path.endswith('.html'):
            # 设置HTML响应头
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Expires', '0')
            with open(path, 'rb') as f:
                content = f.read()
                self.send_header('Content-Length', str(len(content)))
                self.end_headers()
                return BytesIO(content)
        return super().send_head()
    def do_GET(self):
        # 记录静态文件请求
        if not self.path.startswith('/api/'):
            print(f"Serving static file: {self.path}")
        if self.path == '/@vite/client':
            # 处理Vite客户端请求，避免404错误
            self.send_response(204)
            self.end_headers()
            return
        elif self.path == '/':
            # 返回报表系统入口页面
            try:
                with open('index.html', 'r', encoding='utf-8') as f:
                    content = f.read()
                encoded_content = content.encode('utf-8')
                content_length = len(encoded_content)
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.send_header('Content-Length', str(content_length))
                self.end_headers()
                self.wfile.write(encoded_content)
            except FileNotFoundError:
                self.send_response(404)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write('<h1>404 - 页面未找到</h1>'.encode('utf-8'))
        elif self.path.startswith('/iqc'):
                # 返回IQC缺陷分析页面
                import time
                start_time = time.time()
                try:
                    self.log_message(f'Start serving iqc.html at {start_time}')
                    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'iqc.html')
                    with open(file_path, 'rb') as f:
                        encoded_content = f.read()
                    read_time = time.time()
                    self.log_message(f'Finished reading iqc.html in {read_time - start_time:.4f}s')
                    content_length = len(encoded_content)
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html; charset=utf-8')
                    self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
                    self.send_header('Pragma', 'no-cache')
                    self.send_header('Expires', '0')
                    self.send_header('Content-Length', str(content_length))
                    self.end_headers()
                    header_time = time.time()
                    self.log_message(f'Headers sent for iqc.html in {header_time - read_time:.4f}s')
                    bytes_written = self.wfile.write(encoded_content)
                    write_time = time.time()
                    self.log_message(f'Completed serving iqc.html in {write_time - start_time:.4f}s (total bytes: {content_length}, bytes written: {bytes_written})')
                except FileNotFoundError:
                    error_time = time.time()
                    self.log_message(f'File not found error serving iqc.html after {error_time - start_time:.4f}s')
                    self.send_response(404)
                    self.send_header('Content-type', 'text/html')
                except Exception as e:
                    error_time = time.time()
                    self.log_message(f'Error serving iqc.html after {error_time - start_time:.4f}s: {str(e)}')
                    self.send_response(500)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(f'<h1>500 - 服务器内部错误: {str(e)}</h1>'.encode('utf-8'))
        elif self.path == '/recycling.html':
                # 返回回收版使用统计报表页面
                import time
                start_time = time.time()
                try:
                    self.log_message(f'Start serving recycling.html at {start_time}')
                    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'recycling.html')
                    with open(file_path, 'rb') as f:
                        content = f.read()
                    read_time = time.time()
                    self.log_message(f'Finished reading recycling.html in {read_time - start_time:.4f}s')
                    content_length = len(content)
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html; charset=utf-8')
                    self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
                    self.send_header('Pragma', 'no-cache')
                    self.send_header('Expires', '0')
                    self.send_header('Content-Length', str(content_length))
                    self.end_headers()
                    header_time = time.time()
                    self.log_message(f'Headers sent for recycling.html in {header_time - read_time:.4f}s')
                    bytes_written = self.wfile.write(content)
                    write_time = time.time()
                    self.log_message(f'Completed serving recycling.html in {write_time - start_time:.4f}s (total bytes: {content_length}, bytes written: {bytes_written})')
                except FileNotFoundError:
                    error_time = time.time()
                    self.log_message(f'File not found error serving recycling.html after {error_time - start_time:.4f}s')
                    self.send_response(404)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write('<h1>404 - IQC报表页面未找到</h1>'.encode('utf-8'))
                except Exception as e:
                    error_time = time.time()
                    self.log_message(f'Error serving recycling.html after {error_time - start_time:.4f}s: {str(e)}')
                    self.send_response(500)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(f'<h1>500 - 服务器内部错误: {str(e)}</h1>'.encode('utf-8'))
        elif self.path.startswith('/recycling'):
            # 返回服务版使用统计报表页面
            if self.path == '/recycling' or 'recycling?' in self.path:
                self.send_recycling_report()
            elif self.path.startswith('/api/recycling'):
                self.handle_recycling_api()
            else:
                super().do_GET()
        elif self.path == '/api/years':
            response = {'years': [2025, 2024, 2023, 2022]}
            response_data = json.dumps(response).encode()
            content_length = len(response_data)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Length', str(content_length))
            self.end_headers()
            self.wfile.write(response_data)
        elif self.path.startswith('/api/recycling'):
            self.handle_recycling_api()
        elif self.path == '/api/db-test':
            # 测试数据库连接
            self.test_db_connection()
        else:
            # 处理其他静态文件
            super().do_GET()
    
    def do_POST(self):
        if self.path == '/api/report':
            self.handle_iqc_report()
        elif self.path == '/api/recycling/report':
            self.handle_recycling_report_api()
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'API endpoint not found'}).encode())

    def handle_iqc_report(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode())
            year = data.get('year', 2025)
            
            # 连接数据库获取真实数据
            conn = get_db_connection()
            if not conn:
                raise Exception("数据库连接失败")
            
            cur = conn.cursor(cursor_factory=RealDictCursor)
            # 执行SQL查询，按年份筛选
            sql = """
                SELECT 
                    DATE_TRUNC('month', l.event_time) AS month,  -- 按月份截断时间
                    CASE WHEN cd.vendor IS NULL THEN 'Unknown' ELSE cd.vendor END AS vendor,  -- 供应商字段，保持原始供应商名称，NULL值转换为'Unknown'
                    CASE 
                        WHEN SUBSTRING(cd.consumable_def_name FROM 4 FOR 2) = '02' THEN 'Quartz'
                        WHEN SUBSTRING(cd.consumable_def_name FROM 4 FOR 2) = '01' THEN 'Soda'
                        ELSE 'Other'  -- 如果不是01或02，可以归类为Other或其他默认值
                    END AS material_type,  -- 区分Quartz和Soda
                    COUNT(*) AS shipped_lot_count,  -- 统计shipped状态的lot数量
                    ROUND(AVG(
                        (SELECT COUNT(aafi.sno)::float
                         FROM analyze_aoi_field_item aafi
                         LEFT JOIN analyze_aoi_field aaf ON aaf.id = aafi.af_id
                         WHERE aafi.kind IN ('A1','A2','A3','A4')
                         AND aaf.process_flow_seq_name = 'C4010'
                         AND aaf.order_no = l.lot_name)
                    )::numeric, 3) AS avg_black,  -- 计算black的平均值
                    ROUND(AVG(
                        (SELECT COUNT(aafi.sno)::float
                         FROM analyze_aoi_field_item aafi
                         LEFT JOIN analyze_aoi_field aaf ON aaf.id = aafi.af_id
                         WHERE aafi.kind IN ('B1','B2','B3','B4')
                         AND aaf.process_flow_seq_name = 'C4010'
                         AND aaf.order_no = l.lot_name)
                    )::numeric, 3) AS avg_white   -- 计算white的平均值
                FROM lot l
                LEFT JOIN consumable_def cd ON l.material_def_id = cd.consumable_def_name  -- 添加关联条件
                WHERE l.lot_state = 'Shipped'
                    AND EXTRACT(YEAR FROM l.event_time) = %s
                GROUP BY DATE_TRUNC('month', l.event_time), CASE WHEN cd.vendor IS NULL THEN 'Unknown' ELSE cd.vendor END,
                         CASE 
                             WHEN SUBSTRING(cd.consumable_def_name FROM 4 FOR 2) = '02' THEN 'Quartz'
                             WHEN SUBSTRING(cd.consumable_def_name FROM 4 FOR 2) = '01' THEN 'Soda'
                             ELSE 'Other'
                         END;  -- 按月份、vendor和material_type分组
            """
            cur.execute(sql, (year,))
            results = cur.fetchall()
            conn.close()
            
            # 处理查询结果，按材料类型和供应商分组
            material_data = {
                'Quartz': {},
                'Soda': {},
                'Other': {}
            }
            
            # 收集所有供应商
            vendors = set()
            
            for row in results:
                month = row['month'].month  # 提取月份
                material_type = row['material_type']
                vendor = row['vendor']
                vendors.add(vendor)
                
                # 初始化该材料类型和月份的供应商数据
                if month not in material_data[material_type]:
                    material_data[material_type][month] = {
                        'month': month,
                        'production': 0,
                        'white_defect': 0.0,
                        'black_defect': 0.0,
                        'vendors': {}
                    }
                
                # 初始化供应商数据
                if vendor not in material_data[material_type][month]['vendors']:
                    material_data[material_type][month]['vendors'][vendor] = {
                        'production': 0,
                        'white_defect': 0.0,
                        'black_defect': 0.0
                    }
                
                # 累加供应商数据
                material_data[material_type][month]['vendors'][vendor]['production'] += float(row['shipped_lot_count'])
                material_data[material_type][month]['vendors'][vendor]['white_defect'] += float(row['avg_white'])
                material_data[material_type][month]['vendors'][vendor]['black_defect'] += float(row['avg_black'])
                
                # 累加总数据
                material_data[material_type][month]['production'] += float(row['shipped_lot_count'])
                material_data[material_type][month]['white_defect'] += float(row['avg_white'])
                material_data[material_type][month]['black_defect'] += float(row['avg_black'])
            
            # 转换供应商集合为列表
            vendors = sorted(list(vendors))
            
            # 准备返回数据
            report_data = {
                'vendors': vendors,  # 所有供应商列表
                'quartz': {
                    'monthly_data': [],
                    'avg_production': 0,
                    'avg_white_defect': 0,
                    'avg_black_defect': 0
                },
                'soda': {
                    'monthly_data': [],
                    'avg_production': 0,
                    'avg_white_defect': 0,
                    'avg_black_defect': 0
                }
            }
            
            # 处理Quartz数据
            total_quartz_production = 0
            total_quartz_white = 0
            total_quartz_black = 0
            
            for month in range(1, 13):
                if month in material_data['Quartz']:
                    data = material_data['Quartz'][month].copy()
                    # 计算平均缺陷值（基于所有供应商的平均值）
                    vendor_count = len(data['vendors'])
                    data['white_defect'] = round(data['white_defect'] / vendor_count, 2) if vendor_count > 0 else 0
                    data['black_defect'] = round(data['black_defect'] / vendor_count, 2) if vendor_count > 0 else 0
                    report_data['quartz']['monthly_data'].append(data)
                    total_quartz_production += data['production']
                    total_quartz_white += data['white_defect']
                    total_quartz_black += data['black_defect']
                else:
                    report_data['quartz']['monthly_data'].append({
                        'month': month,
                        'production': 0,
                        'white_defect': 0,
                        'black_defect': 0,
                        'vendors': {}
                    })
            
            # 计算Quartz平均值（按实际有数据的月份数平均）
            quartz_month_count = sum(1 for data in report_data['quartz']['monthly_data'] if data['production'] > 0 or data['white_defect'] > 0 or data['black_defect'] > 0)
            report_data['quartz']['avg_production'] = round(total_quartz_production / quartz_month_count) if total_quartz_production and quartz_month_count > 0 else 0
            report_data['quartz']['avg_white_defect'] = round(total_quartz_white / quartz_month_count, 2) if total_quartz_white and quartz_month_count > 0 else 0
            report_data['quartz']['avg_black_defect'] = round(total_quartz_black / quartz_month_count, 2) if total_quartz_black and quartz_month_count > 0 else 0
            
            # 添加供应商详细数据
            report_data['quartz']['vendor_data'] = {}
            # 为每个供应商计算平均值
            report_data['quartz']['vendor_averages'] = {}
            for vendor in vendors:
                report_data['quartz']['vendor_data'][vendor] = []
                vendor_total_production = 0
                vendor_total_white = 0
                vendor_total_black = 0
                vendor_month_count = 0
                
                for month in range(1, 13):
                    if month in material_data['Quartz'] and vendor in material_data['Quartz'][month]['vendors']:
                        vendor_data = material_data['Quartz'][month]['vendors'][vendor]
                        report_data['quartz']['vendor_data'][vendor].append({
                            'month': month,
                            'production': vendor_data['production'],
                            'white_defect': vendor_data['white_defect'],
                            'black_defect': vendor_data['black_defect']
                        })
                        vendor_total_production += vendor_data['production']
                        vendor_total_white += vendor_data['white_defect']
                        vendor_total_black += vendor_data['black_defect']
                        vendor_month_count += 1
                    else:
                        report_data['quartz']['vendor_data'][vendor].append({
                            'month': month,
                            'production': 0,
                            'white_defect': 0,
                            'black_defect': 0
                        })
                
                # 计算该供应商的平均值
                report_data['quartz']['vendor_averages'][vendor] = {
                    'avg_production': round(vendor_total_production / vendor_month_count) if vendor_total_production and vendor_month_count > 0 else 0,
                    'avg_white_defect': round(vendor_total_white / vendor_month_count, 2) if vendor_total_white and vendor_month_count > 0 else 0,
                    'avg_black_defect': round(vendor_total_black / vendor_month_count, 2) if vendor_total_black and vendor_month_count > 0 else 0
                }
            
            # 处理Soda数据
            total_soda_production = 0
            total_soda_white = 0
            total_soda_black = 0
            
            for month in range(1, 13):
                if month in material_data['Soda']:
                    data = material_data['Soda'][month].copy()
                    # 计算平均缺陷值（基于所有供应商的平均值）
                    vendor_count = len(data['vendors'])
                    data['white_defect'] = round(data['white_defect'] / vendor_count, 2) if vendor_count > 0 else 0
                    data['black_defect'] = round(data['black_defect'] / vendor_count, 2) if vendor_count > 0 else 0
                    report_data['soda']['monthly_data'].append(data)
                    total_soda_production += data['production']
                    total_soda_white += data['white_defect']
                    total_soda_black += data['black_defect']
                else:
                    report_data['soda']['monthly_data'].append({
                        'month': month,
                        'production': 0,
                        'white_defect': 0,
                        'black_defect': 0,
                        'vendors': {}
                    })
            
            # 计算Soda平均值（按实际有数据的月份数平均）
            soda_month_count = sum(1 for data in report_data['soda']['monthly_data'] if data['production'] > 0 or data['white_defect'] > 0 or data['black_defect'] > 0)
            report_data['soda']['avg_production'] = round(total_soda_production / soda_month_count) if total_soda_production and soda_month_count > 0 else 0
            report_data['soda']['avg_white_defect'] = round(total_soda_white / soda_month_count, 2) if total_soda_white and soda_month_count > 0 else 0
            report_data['soda']['avg_black_defect'] = round(total_soda_black / soda_month_count, 2) if total_soda_black and soda_month_count > 0 else 0
            
            # 添加供应商详细数据
            report_data['soda']['vendor_data'] = {}
            # 为每个供应商计算平均值
            report_data['soda']['vendor_averages'] = {}
            for vendor in vendors:
                report_data['soda']['vendor_data'][vendor] = []
                vendor_total_production = 0
                vendor_total_white = 0
                vendor_total_black = 0
                vendor_month_count = 0
                
                for month in range(1, 13):
                    if month in material_data['Soda'] and vendor in material_data['Soda'][month]['vendors']:
                        vendor_data = material_data['Soda'][month]['vendors'][vendor]
                        report_data['soda']['vendor_data'][vendor].append({
                            'month': month,
                            'production': vendor_data['production'],
                            'white_defect': vendor_data['white_defect'],
                            'black_defect': vendor_data['black_defect']
                        })
                        vendor_total_production += vendor_data['production']
                        vendor_total_white += vendor_data['white_defect']
                        vendor_total_black += vendor_data['black_defect']
                        vendor_month_count += 1
                    else:
                        report_data['soda']['vendor_data'][vendor].append({
                            'month': month,
                            'production': 0,
                            'white_defect': 0,
                            'black_defect': 0
                        })
                
                # 计算该供应商的平均值
                report_data['soda']['vendor_averages'][vendor] = {
                    'avg_production': round(vendor_total_production / vendor_month_count) if vendor_total_production and vendor_month_count > 0 else 0,
                    'avg_white_defect': round(vendor_total_white / vendor_month_count, 2) if vendor_total_white and vendor_month_count > 0 else 0,
                    'avg_black_defect': round(vendor_total_black / vendor_month_count, 2) if vendor_total_black and vendor_month_count > 0 else 0
                }
            
            # 可以选择是否包含Other类型的数据
            # report_data['other'] = {...}
            
            response_data = json.dumps(report_data).encode()
            content_length = len(response_data)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.send_header('Content-Length', str(content_length))
            self.end_headers()
            self.wfile.write(response_data)
            
        except Exception as e:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())

    def handle_recycling_report_api(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode())
            year = data.get('year', 2024)
            
            # 生成回收版使用统计数据
            recycling_data = []
            total_recycled = 0
            total_used = 0
            
            for month in range(1, 13):
                recycled_count = random.randint(100, 300)
                used_count = random.randint(80, recycled_count)
                
                recycling_data.append({
                    'month': month,
                    'recycled': recycled_count,
                    'used': used_count,
                    'rate': round((used_count / recycled_count) * 100, 2)
                })
                
                total_recycled += recycled_count
                total_used += used_count
            
            report_data = {
                'data': recycling_data,
                'total_recycled': total_recycled,
                'total_used': total_used,
                'avg_rate': round((total_used / total_recycled) * 100, 2)
            }
            
            response_data = json.dumps(report_data).encode()
            content_length = len(response_data)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.send_header('Content-Length', str(content_length))
            self.end_headers()
            self.wfile.write(response_data)
            
        except Exception as e:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())

    def test_db_connection(self):
        """测试数据库连接"""
        try:
            conn = get_db_connection()
            if conn:
                conn.close()
                result = {'status': 'success', 'message': '数据库连接成功'}
            else:
                result = {'status': 'error', 'message': '数据库连接失败'}
                
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'error', 'message': str(e)}).encode())

    def handle_recycling_api(self):
        """处理服务版使用统计报表API请求"""
        try:
            print("收到回收版报表API请求")
            
            # 解析查询参数
            parsed_url = urlparse(self.path)
            query_params = {}
            if parsed_url.query:
                from urllib.parse import parse_qs
                query_params = parse_qs(parsed_url.query)
            
            # 处理查询参数
            filters = {}
            if 'customer' in query_params:
                filters['customer'] = query_params['customer'][0]
            if 'supplier' in query_params:
                filters['supplier'] = query_params['supplier'][0]
            if 'orderType' in query_params:
                filters['orderType'] = query_params['orderType'][0]
            if 'year' in query_params:
                filters['year'] = int(query_params['year'][0])
            
            print(f"查询参数: {filters}")
            
            # 强制使用真实数据，不再回退到模拟数据
            try:
                report_data = self.get_real_recycling_data(filters)
                print("成功获取真实数据库数据")
            except Exception as e:
                print(f"获取真实数据失败: {e}")
                raise e
            
            print(f"获取到数据: {len(report_data.get('data', []))} 条记录")
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            response_data = json.dumps(report_data, ensure_ascii=False, default=str)
            encoded_data = response_data.encode('utf-8')
            content_length = len(encoded_data)
            self.send_header('Content-Length', str(content_length))
            print(f"响应数据大小: {content_length} 字节")
            self.wfile.write(encoded_data)
            print("响应发送完成")
            
        except Exception as e:
            print(f"处理请求时发生错误: {str(e)}")
            import traceback
            traceback.print_exc()
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())

    def get_real_recycling_data(self, filters):
        """从10.10.102.129数据库获取真实的服务版使用统计报表数据"""
        # 强制使用真实数据库配置
        db_config = {
            'host': '10.10.102.129',
            'port': 5432,
            'database': 'mes_qingyi',
            'user': 'mes_qingyi',
            'password': 'mes_qingyi'
        }
        
        try:
            print(f"正在连接数据库: {db_config['host']}/{db_config['database']}")
            # 建立数据库连接
            conn = psycopg2.connect(**db_config)
            cur = conn.cursor(cursor_factory=RealDictCursor)
            
            # 构建SQL查询 - 从真实mes_qingyi数据库查询
            sql_query = """
            SELECT 
                l.customer_name,
                l.lot_name,
                l.model_id,
                (CASE 
                    WHEN (SELECT equipment_name FROM lot_engineer_setting les WHERE les.lot_name = l.lot_name AND les.process_seq_name = 'A2020') IS NOT NULL AND (SELECT equipment_name FROM lot_engineer_setting les WHERE les.lot_name = l.lot_name AND les.process_seq_name = 'A2020') <> '' 
                     AND (SELECT equipment_name FROM lot_engineer_setting les WHERE les.lot_name = l.lot_name AND les.process_seq_name = 'A2022') IS NOT NULL AND (SELECT equipment_name FROM lot_engineer_setting les WHERE les.lot_name = l.lot_name AND les.process_seq_name = 'A2022') <> '' 
                    THEN (SELECT equipment_name FROM lot_engineer_setting les WHERE les.lot_name = l.lot_name AND les.process_seq_name = 'A2020') || '/' || (SELECT equipment_name FROM lot_engineer_setting les WHERE les.lot_name = l.lot_name AND les.process_seq_name = 'A2022')
                    WHEN (SELECT equipment_name FROM lot_engineer_setting les WHERE les.lot_name = l.lot_name AND les.process_seq_name = 'A2020') IS NOT NULL AND (SELECT equipment_name FROM lot_engineer_setting les WHERE les.lot_name = l.lot_name AND les.process_seq_name = 'A2020') <> '' 
                    THEN (SELECT equipment_name FROM lot_engineer_setting les WHERE les.lot_name = l.lot_name AND les.process_seq_name = 'A2020')
                    WHEN (SELECT equipment_name FROM lot_engineer_setting les WHERE les.lot_name = l.lot_name AND les.process_seq_name = 'A2022') IS NOT NULL AND (SELECT equipment_name FROM lot_engineer_setting les WHERE les.lot_name = l.lot_name AND les.process_seq_name = 'A2022') <> '' 
                    THEN (SELECT equipment_name FROM lot_engineer_setting les WHERE les.lot_name = l.lot_name AND les.process_seq_name = 'A2022')
                    ELSE NULL 
                 END) AS equipment,
                l.cd,
                l.process_layer,
                (CASE 
                WHEN ((SELECT htm_no from erp_cam_design_param ecdp where ecdp.lot_name = l.lot_name order by ecdp.htm_no desc limit 1) = 2 )
                THEN CONCAT(
                    TO_CHAR((SELECT event_time FROM lot_history lh WHERE lh.lot_name = l.lot_name AND lh.process_seq_name = 'A2020' and lh.lot_process_state = 'Run' order by lh.event_time limit 1), 'YYYY-MM-DD HH24:MI:SS'),
                    ';',
                    TO_CHAR((SELECT event_time FROM lot_history lh WHERE lh.lot_name = l.lot_name AND lh.process_seq_name = 'A2022' and lh.lot_process_state = 'Run' order by lh.event_time limit 1), 'YYYY-MM-DD HH24:MI:SS')
                )
                ELSE TO_CHAR((SELECT event_time FROM lot_history lh WHERE lh.lot_name = l.lot_name AND lh.process_seq_name = 'A2020' and lh.lot_process_state = 'Run' order by lh.event_time limit 1), 'YYYY-MM-DD HH24:MI:SS')
             END) AS locktime,
                l.material_id,
                cd.vendor,
                l.lot_type,
                l.product_size as product_size,
				(CASE 
        		WHEN ((SELECT htm_no FROM erp_cam_design_param ecdp WHERE ecdp.lot_name = l.lot_name ORDER BY ecdp.htm_no DESC LIMIT 1) = 2)
        		THEN 
           		 (SELECT count(aafi.sno)::text 
           	 	 FROM analyze_aoi_field_item aafi 
            	 LEFT JOIN analyze_aoi_field aaf ON aaf.id = aafi.af_id 
            	 WHERE aafi.kind IN ('A1','A2','A3','A4') 
            	   AND aaf.process_flow_seq_name = 'C4010' 
            	   AND l.lot_name = aaf.order_no)
          	  || ';' || 
          	  (SELECT count(aafi.sno)::text 
            	 FROM analyze_aoi_field_item aafi 
           	  LEFT JOIN analyze_aoi_field aaf ON aaf.id = aafi.af_id 
           	  WHERE aafi.kind IN ('A1','A2','A3','A4') 
            	   AND aaf.process_flow_seq_name = 'C4017' 
            	   AND l.lot_name = aaf.order_no)
       		 ELSE 
            (SELECT count(aafi.sno)::text 
             FROM analyze_aoi_field_item aafi 
             LEFT JOIN analyze_aoi_field aaf ON aaf.id = aafi.af_id 
             WHERE aafi.kind IN ('A1','A2','A3','A4') 
               AND aaf.process_flow_seq_name = 'C4010' 
               AND l.lot_name = aaf.order_no)
    		END) AS black,
            	(CASE 
        		WHEN ((SELECT htm_no FROM erp_cam_design_param ecdp WHERE ecdp.lot_name = l.lot_name ORDER BY ecdp.htm_no DESC LIMIT 1) = 2)
        		THEN 
           		 (SELECT count(aafi.sno)::text 
           	 	 FROM analyze_aoi_field_item aafi 
            	 LEFT JOIN analyze_aoi_field aaf ON aaf.id = aafi.af_id 
            	 WHERE aafi.kind IN ('B1','B2','B3','B4') 
            	   AND aaf.process_flow_seq_name = 'C4010' 
            	   AND l.lot_name = aaf.order_no)
          	  || ';' || 
          	  (SELECT count(aafi.sno)::text 
            	 FROM analyze_aoi_field_item aafi 
           	  LEFT JOIN analyze_aoi_field aaf ON aaf.id = aafi.af_id 
           	  WHERE aafi.kind IN ('B1','B2','B3','B4') 
            	   AND aaf.process_flow_seq_name = 'C4017' 
            	   AND l.lot_name = aaf.order_no)
       		 ELSE 
            (SELECT count(aafi.sno)::text 
             FROM analyze_aoi_field_item aafi 
             LEFT JOIN analyze_aoi_field aaf ON aaf.id = aafi.af_id 
             WHERE aafi.kind IN ('B1','B2','B3','B4') 
               AND aaf.process_flow_seq_name = 'C4010' 
               AND l.lot_name = aaf.order_no)
    		END)  AS white,
                l.event_time as repairtime,
                l.product_type
            FROM 
                lot l 
                INNER JOIN consumable_def cd ON l.material_def_id = cd.consumable_def_name
            WHERE 
                cd.description LIKE '%%R%%'
                AND cd.consumable_type = '主原材料'
                AND l.material_id IS NOT NULL
                AND l.lot_name IS NOT NULL
                AND l.lot_name != ''
            ORDER BY locktime desc
            """
            
            # 移除动态过滤条件以解决参数不匹配问题
            conditions = []
            params = []
            
            # 添加WHERE子句
            if conditions:
                sql_query += " AND " + " AND ".join(conditions)
            
            # 执行查询
            cur.execute(sql_query, params)
            rows = cur.fetchall()
            
            # 处理查询结果
            data = []
            for row in rows:
                try:
                    row_dict = dict(row)
                    data.append({
                        'customer': str(row_dict.get('customer_name', '') or ''),
                        'processNumber': str(row_dict.get('lot_name', '') or ''),
                        'model': str(row_dict.get('model_id', '') or ''),
                        'equipment': str(row_dict.get('equipment', '') or ''),
                        'cd': str(row_dict.get('cd', '') or ''),
                        'layer': str(row_dict.get('process_layer', '') or ''),
                        'lockTime': str(row_dict.get('locktime', '') or '') ,
                        'batchNumber': str(row_dict.get('material_id', '') or ''),
                        'supplier': str(row_dict.get('vendor', '') or ''),
                        'orderType': str(row_dict.get('lot_type', '') or ''),
                        'size': str(row_dict.get('product_size', '0')) + 'mm',
                        'blackDefect': str(row_dict.get('black', '') or ''),
                        'whiteDefect': str(row_dict.get('white', '') or ''),
                        'repairTime': 0,
                        'judgeType': '',
                        'glassSource': '',
                        'polishSupplier': '',
                        'chromeSupplier': '',
                        'glueSupplier': '',
                        'recycleStatus': '',
                        'reprocessPlan': '',
                        'recycleBatch':  '',
                        'factory': 'FS',
                        'year': int(row_dict.get('create_date').year) if row_dict.get('create_date') else datetime.now().year
                    })
                except Exception as e:
                    print(f"处理行数据时出错: {e}")
                    continue
            
            # 关闭数据库连接
            cur.close()
            conn.close()
            
            return {
                'data': data,
                'total': len(data),
                'filters': filters
            }
            
        except Exception as e:
                print(f"获取真实数据失败: {e}")
                raise e  # 不再回退到模拟数据，直接抛出异常

    def generate_random_date(self):
        """生成随机日期"""
        start_date = int(datetime(2024, 1, 1).timestamp())
        end_date = int(datetime.now().timestamp())
        random_timestamp = random.randint(start_date, end_date)
        return datetime.fromtimestamp(random_timestamp).strftime('%Y-%m-%d')

    def do_OPTIONS(self):
        """处理预检请求"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def send_recycling_report(self):
        """返回服务版使用统计报表页面"""
        try:
            file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'recycling.html')
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
        except FileNotFoundError:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write('<h1>404 - 服务版报表页面未找到</h1>'.encode('utf-8'))
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(f'<h1>500 - 服务器内部错误: {str(e)}</h1>'.encode('utf-8'))

class ThreadedHTTPServer(ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True

if __name__ == '__main__':
    PORT = 8000
    Handler = ReportSystemHandler
    with ThreadedHTTPServer(('', PORT), Handler) as httpd:
        print(f"服务器运行在 http://localhost:{PORT}")
        print("按 Ctrl+C 停止服务器")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n服务器已停止")