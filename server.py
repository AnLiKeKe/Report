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
            response = {'years': [2024, 2023, 2022, 2021]}
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
            year = data.get('year', 2024)
            
            # 生成Quartz数据
            quartz_data = []
            total_quartz_production = 0
            total_quartz_white_defect = 0
            total_quartz_black_defect = 0
            
            # 生成Soda数据
            soda_data = []
            total_soda_production = 0
            total_soda_white_defect = 0
            total_soda_black_defect = 0
            
            for month in range(1, 13):
                # Quartz数据
                quartz_production = random.randint(400, 600)
                quartz_white_defect = random.randint(10, 40)
                quartz_black_defect = random.randint(5, 25)
                
                quartz_data.append({
                    'month': month,
                    'production': quartz_production,
                    'white_defect': quartz_white_defect,
                    'black_defect': quartz_black_defect
                })
                
                total_quartz_production += quartz_production
                total_quartz_white_defect += quartz_white_defect
                total_quartz_black_defect += quartz_black_defect
                
                # Soda数据
                soda_production = random.randint(400, 600)
                soda_white_defect = random.randint(10, 40)
                soda_black_defect = random.randint(5, 25)
                
                soda_data.append({
                    'month': month,
                    'production': soda_production,
                    'white_defect': soda_white_defect,
                    'black_defect': soda_black_defect
                })
                
                total_soda_production += soda_production
                total_soda_white_defect += soda_white_defect
                total_soda_black_defect += soda_black_defect
            
            # 计算平均值
            report_data = {
                'quartz': {
                    'monthly_data': quartz_data,
                    'avg_production': round(total_quartz_production / 12),
                    'avg_white_defect': round(total_quartz_white_defect / 12),
                    'avg_black_defect': round(total_quartz_black_defect / 12)
                },
                'soda': {
                    'monthly_data': soda_data,
                    'avg_production': round(total_soda_production / 12),
                    'avg_white_defect': round(total_soda_white_defect / 12),
                    'avg_black_defect': round(total_soda_black_defect / 12)
                }
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
            ORDER BY l.event_time desc
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
                        'blackDefect':str(row_dict.get('black', '') or ''),
                        'whiteDefect':str(row_dict.get('white', '') or ''),
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
                        'year': row_dict.get('create_date').year if row_dict.get('create_date') else datetime.now().year
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

    def generate_mock_recycling_data(self, filters):
        """生成服务版使用统计报表的模拟数据(当数据库不可用时)"""
        customers = ['客户A', '客户B', '客户C', '客户D', '客户E']
        suppliers = ['供应商1', '供应商2', '供应商3', '供应商4', '供应商5']
        order_types = ['标准订单', '加急订单', '特殊订单', '批量订单']
        equipment_list = ['设备A', '设备B', '设备C', '设备D', '设备E']
        factories = ['工厂1', '工厂2', '工厂3', '工厂4', '工厂5']
        
        # 应用过滤器
        filtered_customers = [c for c in customers if not filters.get('customer') or c == filters['customer']]
        filtered_suppliers = [s for s in suppliers if not filters.get('supplier') or s == filters['supplier']]
        filtered_order_types = [t for t in order_types if not filters.get('orderType') or t == filters['orderType']]
        
        data = []
        
        for i in range(50):
            customer = random.choice(filtered_customers) if filtered_customers else customers[0]
            supplier = random.choice(filtered_suppliers) if filtered_suppliers else suppliers[0]
            order_type = random.choice(filtered_order_types) if filtered_order_types else order_types[0]
            
            data.append({
                'customer': customer,
                'processNumber': f'PR{str(i + 1).zfill(6)}',
                'model': f'MOD{str(random.randint(1000, 9999))}',
                'equipment': random.choice(equipment_list),
                'cd': round(random.uniform(10, 100), 1),
                'layer': f'L{random.randint(1, 5)}',
                'lockTime': self.generate_random_date(),
                'batchNumber': f'BN{str(random.randint(10000, 99999))}',
                'supplier': supplier,
                'orderType': order_type,
                'size': f'{random.randint(50, 150)}x{random.randint(50, 150)}',
                'blackDefect': random.randint(0, 20),
                'whiteDefect': random.randint(0, 15),
                'repairTime': round(random.uniform(0.5, 5.0), 1),
                'judgeType': random.choice(['合格', '不合格', '待检']),
                'glassSource': random.choice(['供应商1', '供应商2', '自产']),
                'polishSupplier': random.choice(['抛光厂A', '抛光厂B', '抛光厂C']),
                'chromeSupplier': random.choice(['镀铬厂X', '镀铬厂Y']),
                'glueSupplier': random.choice(['涂胶厂1', '涂胶厂2', '涂胶厂3']),
                'recycleStatus': random.choice(['已回收', '未回收', '部分回收']),
                'reprocessPlan': random.choice(['重新加工', '报废处理', '降级使用']),
                'recycleBatch': f'RB{str(random.randint(1000, 9999))}',
                'factory': random.choice(factories)
            })
        
        return {
            'data': data,
            'total': len(data),
            'filters': filters
        }

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