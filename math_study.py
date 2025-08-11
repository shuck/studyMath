import random
from fpdf import FPDF
import datetime

def generate_math_problems(num_problems=10):
    """生成100以内加减法和2、3、4乘法题目"""
    problems = []
     # 定义题目类型及其概率权重
    problem_types = [
        ('two_num_add', 0.20),    # 两位数加法
        ('two_num_add_fill', 0.05),# 两位数加法(填空)
        ('two_num_sub', 0.20),    # 两位数减法
        ('two_num_sub_fill', 0.05),# 两位数减法(填空)
        ('multiply', 0.40),       # 乘法
        ('multiply_fill', 0.05),  # 乘法(填空)
        ('triple_add', 0),     # 三个数连加
        ('triple_sub', 0),     # 三个数连减
        ('mixed_three', 0.05)     # 三个数混合连加减
    ]
    
    for _ in range(num_problems):  # 生成100道题
        # 随机选择题目类型
        op_types = [pt[0] for pt in problem_types]
        weights = [pt[1] for pt in problem_types]
        operation = random.choices(op_types, weights=weights)[0]
        
        if operation == 'two_num_add':  # 两位数加法
            # 修正：避免100 + 0问题
            a = random.randint(0, 99)  # a最大99
            b = random.randint(0, 100 - a) if a < 100 else 0
            problem = f"{a} + {b} ="
        
        elif operation == 'two_num_add_fill':  # 两位数加法(填空)
            fill_position = random.choice(['first', 'second'])
            a = random.randint(5, 99)
            b = random.randint(1, min(30, 100 - a))
            
            if fill_position == 'first':   # 填空加数
                problem = f"(    ) + {b} = {a + b}"
            else:  # 填空被加数
                problem = f"{a} + (    ) = {a + b}"

        elif operation == 'two_num_sub':  # 两位数减法
            # 修正：避免0 - 0问题
            a = random.randint(1, 100)  # a最小1
            b = random.randint(0, a)
            problem = f"{a} - {b} ="

        elif operation == 'two_num_sub_fill':  # 两位数减法(填空)
            fill_position = random.choice(['first', 'second'])
            a = random.randint(15, 100)
            b = random.randint(1, min(30, a))
            
            if fill_position == 'first':   # 填空被减数
                problem = f"(    ) - {b} = {a - b}"
            else:  # 填空减数
                problem = f"{a} - (    ) = {a - b}"
            
        elif operation == 'multiply':  # 乘法 (限2、3、4)
            multiplier = random.randint(1, 9)  # 限制乘数为1-9
            multiplicand = random.randint(1, 9)  # 限制积不超过100
            problem = f"{multiplicand} × {multiplier} ="
        
        elif operation == 'multiply_fill':  # 乘法(填空)
            fill_position = random.choice(['first', 'second'])
            multiplier = random.randint(1, 9)
            multiplicand = random.randint(1, 9)  # 被乘数不为0
            result = multiplicand * multiplier
            
            if fill_position == 'first':   # 填空乘数
                problem = f"{multiplicand} × (    ) = {result}"
            else:  # 填空被乘数
                problem = f"(    ) × {multiplier} = {result}"
            
        elif operation == 'triple_add':  # 三个数连加
            # 修正：确保总和不超过100
            a = random.randint(1, 50)
            b = random.randint(1, min(50, 99 - a))  # 限制b的范围
            c = random.randint(1, min(30, 100 - a - b))  # 限制c的范围
            problem = f"{a} + {b} + {c} ="
            
        elif operation == 'triple_sub':  # 三个数连减
            # 确保每一步结果非负
            a = random.randint(20, 80)
            b = random.randint(1, min(30, a - 1))  # 限制b的范围
            c = random.randint(1, min(30, a - b))  # 限制c的范围
            problem = f"{a} - {b} - {c} ="
            
        elif operation == 'mixed_three':  # 三个数混合连加减
            # 重构：更安全的生成策略
            pattern_type = random.choice(['+-', '-+'])
            
            if pattern_type == '+-':  # a + b - c
                a = random.randint(1, 70)
                b = random.randint(1, min(30, 100 - a))
                # 确保a + b >= c
                c = random.randint(1, min(30, a + b))
                problem = f"{a} + {b} - {c} ="
                
            else:  # a - b + c
                a = random.randint(10, 70)
                b = random.randint(1, min(30, a))  # 确保a >= b
                # 确保结果在100以内
                c_max = min(30, 100 - (a - b))
                c = random.randint(1, c_max) if c_max > 0 else 0
                problem = f"{a} - {b} + {c} =" if c_max > 0 else f"{a} - {b} ="


        problems.append((problem))
    
    return problems

def create_math_pdf(problems, filename="Math_Problems.pdf"):
    """创建包含数学题目的PDF"""
    pdf = FPDF()
    pdf.add_page()
    
    # 设置PDF字体
    pdf.add_font("NotoSansSC", "", "D://kousuan//studyMath//NotoSansSC-6.ttf", uni=True)
    pdf.add_font("NotoSansSC", "B", "D://kousuan//studyMath//Noto-Sans-SC-Bold-2.ttf", uni=True)

    # 设置紧凑的页边距（上下左右均为5mm）
    #pdf.set_margins(5, 5, 5)
    #pdf.set_auto_page_break(False)  # 禁用自动分页
    
    # 使用系统默认字体
    pdf.set_font("NotoSansSC", size=10)
    
    # 标题
    """ pdf.set_font("NotoSansSC", "B", 16)
    pdf.cell(0, 15, "小学数学练习题", ln=True, align="C") """
    
    # 日期和难度信息
    pdf.set_font("NotoSansSC", "", 10)
    today = datetime.datetime.now().strftime("%Y年%m月%d日")
    pdf.cell(0, 8, f"日期：________________        姓名：________________ ", ln=True)
    pdf.ln(5)
    
    # 说明文字
    """ pdf.set_font("NotoSansSC", "", 10)
    pdf.cell(0, 6, "题目范围: 100以内加减法, 2、3、4的乘法", ln=True)
    pdf.cell(0, 6, "建议时间: 20分钟", ln=True)
    pdf.ln(10) """
    
# 添加题目（一行四列布局）
    pdf.set_font("NotoSansSC", "", 14)
    
    # 定义四列的宽度和位置
    col_width = 45  # 每列宽度
    left_margin = 10  # 左边距
    spacing = 4  # 列间距
    row_height = 8  # 行高
    
    # 计算列坐标
    col_positions = [
        left_margin,
        left_margin + col_width + spacing,
        left_margin + (col_width + spacing) * 2,
        left_margin + (col_width + spacing) * 3
    ]
    
    # 添加题目
    problem_count = len(problems)
    rows_needed = (problem_count + 3) // 4  # 计算所需行数
    
    for i in range(rows_needed):
        y_position = pdf.get_y()
        
        # 添加一行四列
        for col in range(4):
            idx = i * 4 + col
            if idx < problem_count:
                pdf.set_xy(col_positions[col], y_position)
                pdf.cell(col_width, row_height, f"{problems[idx]}", border=0)
        
        pdf.ln(row_height + 2)  # 行间距
        
        # 每5行增加额外间距
        #if (i + 1) % 5 == 0:
        #    pdf.ln(5)
    
    # 保存文件
    pdf.output(filename)
    return filename

def main():
    print("数学题生成器 (带PDF导出功能)")
    print("支持: 100以内加减法, 乘法口诀")
    
    try:
        num_problems = int(input("\n请输入要生成的题目数量 (建议20-50): "))
        if num_problems < 1:
            num_problems = 100
    except ValueError:
        num_problems = 100
    
    filename = input("输入PDF文件名 (回车使用默认名称): ").strip()
    if not filename:
        filename = f"Math_Problems_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    elif not filename.lower().endswith('.pdf'):
        filename += '.pdf'
    
    # 生成题目
    problems = generate_math_problems(num_problems)
    
    print(f"\n正在生成 {num_problems} 道题目并创建PDF...")
    
    # 创建PDF
    pdf_file = create_math_pdf(problems, filename)
    
    print(f"\n生成完成! PDF文件已保存为: {pdf_file}")
    print("温馨提示: 请确保已安装支持中文的Noto Sans SC字体，或替换为其他中文字体")

if __name__ == "__main__":
    main()