import http.server
import socketserver
import json
import urllib.parse
from datetime import datetime
import os

# 模拟数据
MOCK_DATA = [
    {"month": "2024-01", "total_items": 1250, "pass_count": 1187, "fail_count": 63, "pass_rate": 95.0, "fail_rate": 5.0},
    {"month": "2024-02", "total_items": 1320, "pass_count": 1254, "fail_count": 66, "pass_rate": 95.0, "fail_rate": 5.0},
    {"month": "2024-03", "total_items": 1410, "pass_count": 1354, "fail_count": 56, "pass_rate": 96.0, "fail_rate": 4.0},
    {"month": "2024-04", "total_items": 1380, "pass_count": 1311, "fail_count": 69, "pass_rate": 95.0, "fail_rate": 5.0},
    {"month": "2024-05", "total_items": 1450, "pass_count": 1395, "fail_count": 55, "pass_rate": 96.2, "fail_rate": 3.8},
    {"month": "2024-06", "total_items": 1520, "pass_count": 1444, "fail_count": 76, "pass_rate": 95.0, "fail_rate": 5.0},
    {"month": "2024-07", "total_items": 1480, "pass_count": 1421, "fail_count": 59, "pass_rate": 96.0, "fail_rate": 4.0},
    {"month": "2024-08", "total_items": 1550, "pass_count": 1472, "fail_count": 78, "pass_rate": 95.0, "fail_rate": 5.0},
    {"month": "2024-09", "total_items": 1610, "pass_count": 1537, "fail_count": 73, "pass_rate": 95.5, "fail_rate": 4.5},
    {"month": "2024-10", "total_items": 1580, "pass_count": 1517, "fail_count": 63, "pass_rate": 96.0, "fail_rate": 4.0},
    {"month": "2024-11", "total_items": 1650, "pass_count": 1584, "fail_count": 66, "pass_rate": 96.0, "fail_rate": 4.0},
    {"month": "2024-12", "total_items": 1720, "pass_count": 1634, "fail_count": 86, "pass_rate": 95.0, "fail_rate": 5.0},
    {"month": "2023-01", "total_items": 1200, "pass_count": 1140, "fail_count": 60, "pass_rate": 95.0, "fail_rate": 5.0},
    {"month": "2023-02", "total_items": 1180, "pass_count": 1121, "fail_count": 59, "pass_rate": 95.0, "fail_rate": 5.0},
    {"month": "2023-03", "total_items": 1250, "pass_count": 1200, "fail_count": 50, "pass_rate": 96.0, "fail_rate": 4.0},
]

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/years':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            years = list(set([int(item["month"].split("-")[0]) for item in MOCK_DATA]))
            years.sort(reverse=True)
            self.wfile.write(json.dumps({"years": years}).encode())
            
        elif self.path.startswith('/api/report'):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # 解析查询参数
            if '?' in self.path:
                query = urllib.parse.parse_qs(self.path.split('?')[1])
                year = int(query.get('year', [2024])[0])
            else:
                year = 2024
            
            year_str = str(year)
            year_data = [item for item in MOCK_DATA if item["month"].startswith(year_str)]
            
            if year_data:
                total_items = sum(item["total_items"] for item in year_data)
                total_pass = sum(item["pass_count"] for item in year_data)
                total_fail = sum(item["fail_count"] for item in year_data)
                
                response = {
                    "year": year,
                    "total_items": total_items,
                    "total_pass": total_pass,
                    "total_fail": total_fail,
                    "overall_pass_rate": round((total_pass / total_items) * 100, 2),
                    "overall_fail_rate": round((total_fail / total_items) * 100, 2),
                    "monthly_data": year_data
                }
            else:
                response = {
                    "year": year,
                    "total_items": 0,
                    "total_pass": 0,
                    "total_fail": 0,
                    "overall_pass_rate": 0,
                    "overall_fail_rate": 0,
                    "monthly_data": []
                }
            
            self.wfile.write(json.dumps(response).encode())
            
        else:
            # 处理静态文件
            if self.path == '/':
                self.path = '/index.html'
            super().do_GET()
    
    def do_POST(self):
        if self.path == '/api/report':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            year = data.get('year', 2024)
            year_str = str(year)
            year_data = [item for item in MOCK_DATA if item["month"].startswith(year_str)]
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            if year_data:
                total_items = sum(item["total_items"] for item in year_data)
                total_pass = sum(item["pass_count"] for item in year_data)
                total_fail = sum(item["fail_count"] for item in year_data)
                
                response = {
                    "year": year,
                    "total_items": total_items,
                    "total_pass": total_pass,
                    "total_fail": total_fail,
                    "overall_pass_rate": round((total_pass / total_items) * 100, 2),
                    "overall_fail_rate": round((total_fail / total_items) * 100, 2),
                    "monthly_data": year_data
                }
            else:
                response = {
                    "year": year,
                    "total_items": 0,
                    "total_pass": 0,
                    "total_fail": 0,
                    "overall_pass_rate": 0,
                    "overall_fail_rate": 0,
                    "monthly_data": []
                }
            
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    PORT = 8000
    Handler = MyHTTPRequestHandler
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"服务器运行在 http://localhost:{PORT}")
        print("按 Ctrl+C 停止服务器")
        httpd.serve_forever()