import os
import subprocess
import codecs

def read_file(path):
    with codecs.open(path, 'r', 'utf-8') as f:
        return f.read()

def main():
    tech_html = read_file('Technical_Report.html')
    
    # Extract body content from Technical_Report.html
    body_start = tech_html.find('<div class="container">')
    if body_start == -1:
        body_start = tech_html.find('<body>') + 6
    body_end = tech_html.find('</body>')
    
    tech_body = tech_html[body_start:body_end]

    html_content = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <title>AIoT HW4 - Final Report</title>
    <style>
        body {{
            font-family: "Microsoft JhengHei", sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            background-color: #fff;
            padding: 40px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            border-radius: 8px;
        }}
        h1 {{
            text-align: center;
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
            margin-top: 50px;
        }}
        h2 {{
            color: #2980b9;
            border-left: 5px solid #3498db;
            padding-left: 10px;
            margin-top: 30px;
            page-break-after: avoid;
        }}
        img {{
            max-width: 100%;
            border: 1px solid #ccc;
            margin-bottom: 20px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: center;
        }}
        th {{
            background-color: #3498db;
            color: white;
        }}
        .page-break {{
            page-break-before: always;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Part 1. Raspberry Pi 4 執行截圖</h1>
        <p>在 Raspberry Pi 4 上成功執行 test.py 與 carema.py：</p>
        
        <div style="display: flex; gap: 20px; justify-content: center; align-items: flex-start; margin-bottom: 20px;">
            <div style="flex: 1; text-align: center;">
                <h2 style="margin-top: 0; border: none; padding: 0;">test.py 執行截圖</h2>
                <img src="IMG20260512111623.jpg" alt="test.py execution" style="max-height: 350px; width: auto; object-fit: contain;">
            </div>
            <div style="flex: 1; text-align: center;">
                <h2 style="margin-top: 0; border: none; padding: 0;">carema.py 執行截圖</h2>
                <img src="IMG20260512111521.jpg" alt="carema.py execution" style="max-height: 350px; width: auto; object-fit: contain;">
            </div>
        </div>

        <div class="page-break"></div>

        <!-- Part 3 內容 -->
        {tech_body}

    </div>
</body>
</html>
"""

    with codecs.open('Final_Report.html', 'w', 'utf-8') as f:
        f.write(html_content)
    print("Final_Report.html generated successfully.")

if __name__ == '__main__':
    main()
