import requests
import json

# API请求参数
url = 'http://localhost:8003/api/report'
headers = {'Content-Type': 'application/json'}
data = {'year': 2025}

# 发送POST请求
response = requests.post(url, headers=headers, data=json.dumps(data))

# 检查响应状态
if response.status_code == 200:
    report_data = response.json()
    # 查找ULC供应商数据
    ulc_data_quartz = report_data['quartz']['vendor_data'].get('ULC', None)
    ulc_data_soda = report_data['soda']['vendor_data'].get('ULC', None)
    
    if ulc_data_quartz or ulc_data_soda:
        print('2025年ULC供应商各月生产数据:')
        
        # 处理Quartz数据
        if ulc_data_quartz:
            print('Quartz材料:')
            total_quartz = 0
            month_count_quartz = 0
            for month_data in ulc_data_quartz:
                if month_data['production'] > 0:
                    print(f"{month_data['month']}月: {month_data['production']}")
                    total_quartz += month_data['production']
                    month_count_quartz += 1
            if month_count_quartz > 0:
                avg_quartz = total_quartz / month_count_quartz
                print(f'Quartz平均月生产数: {avg_quartz:.2f}')
            else:
                print('Quartz无生产数据')
        
        # 处理Soda数据
        if ulc_data_soda:
            print('\nSoda材料:')
            total_soda = 0
            month_count_soda = 0
            for month_data in ulc_data_soda:
                if month_data['production'] > 0:
                    print(f"{month_data['month']}月: {month_data['production']}")
                    total_soda += month_data['production']
                    month_count_soda += 1
            if month_count_soda > 0:
                avg_soda = total_soda / month_count_soda
                print(f'Soda平均月生产数: {avg_soda:.2f}')
            else:
                print('Soda无生产数据')
        
        # 计算总平均值
        total_all = (total_quartz if ulc_data_quartz else 0) + (total_soda if ulc_data_soda else 0)
        month_count_all = (month_count_quartz if ulc_data_quartz else 0) + (month_count_soda if ulc_data_soda else 0)
        if month_count_all > 0:
            avg_all = total_all / month_count_all
            print(f'\n总平均月生产数: {avg_all:.2f}')
    else:
        print('未找到ULC供应商数据')
else:
    print(f'API请求失败，状态码: {response.status_code}')