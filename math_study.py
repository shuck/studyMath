import random
from fpdf import FPDF
import datetime

def generate_math_problems(num_problems=100):
    # 预先生成乘法口诀表范围内的除法题示例
    multiplication_table_divisions = []
    for divisor in range(2, 10):
        for quotient in range(2, 10):
            dividend = divisor * quotient
            if 2 <= dividend <= 81:
                multiplication_table_divisions.append((dividend, divisor, quotient))

    """生成 100 以内加减法和 2、3、4 乘法题目"""
    problems = []
    seen_problems = set()  # 用于记录已生成的题目

    # 定义题目类型及其概率权重
    problem_types = [
        ('two_num_add', 10),    # 两位数加法
        ('two_num_add_fill', 5),# 两位数加法 (填空)
        ('two_num_sub', 10),    # 两位数减法
        ('two_num_sub_fill', 5),# 两位数减法 (填空)
        ('multiply', 20),       # 乘法
        ('multiply_fill', 13),  # 乘法 (填空)
        ('triple_add', 0),      # 三个数连加
        ('triple_sub', 0),      # 三个数连减
        ('mixed_three', 2),     # 三个数混合连加减
        ('comparison_expr', 1), # 算式比较
        ('compare_num_expr', 1),# 算式与数字比较
        ('divide', 18),         # 除法
        ('divide_fill', 15)     # 除法 (填空)
    ]

    # 创建题型队列
    type_queue = []
    for op_type, count in problem_types:
        if count > 0:
            type_queue.extend([op_type] * count)
    
    # 随机打乱题型顺序
    random.shuffle(type_queue)
    
    # 循环使用队列，确保题型多样
    queue_index = 0
    while len(problems) < num_problems:
        # 如果队列用完，重新打乱
        if queue_index >= len(type_queue):
            random.shuffle(type_queue)
            queue_index = 0
        
        operation = type_queue[queue_index]
        queue_index += 1  # 无论成功与否都移动到下一个

        problem = None
        attempts = 0
        max_attempts = 10  # 降低尝试次数，避免卡住
        
        while problem is None or problem in seen_problems:
            attempts += 1
            if attempts > max_attempts:
                break  # 尝试几次后就放弃，移动到下一个题型
            
            if operation == 'two_num_add':
                a = random.randint(0, 99)
                b = random.randint(0, 100 - a) if a < 100 else 0
                problem = f"{a} + {b} ="
            
            elif operation == 'two_num_add_fill':
                fill_position = random.choice(['first', 'second'])
                a = random.randint(0, 99)
                b = random.randint(0, 100 - a) if a < 100 else 0
                if fill_position == 'first':
                    problem = f"(    ) + {b} = {a + b}"
                else:
                    problem = f"{a} + (    ) = {a + b}"

            elif operation == 'two_num_sub':
                a = random.randint(1, 100)
                b = random.randint(0, a)
                problem = f"{a} - {b} ="

            elif operation == 'two_num_sub_fill':
                fill_position = random.choice(['first', 'second'])
                a = random.randint(1, 100)
                b = random.randint(0, a)
                if fill_position == 'first':
                    problem = f"(    ) - {b} = {a - b}"
                else:
                    problem = f"{a} - (    ) = {a - b}"
                
            elif operation == 'multiply':
                multiplier = random.randint(1, 9)
                multiplicand = random.randint(1, 9)
                problem = f"{multiplicand} × {multiplier} ="
            
            elif operation == 'multiply_fill':
                fill_position = random.choice(['first', 'second'])
                multiplier = random.randint(1, 9)
                multiplicand = random.randint(1, 9)
                result = multiplicand * multiplier
                if fill_position == 'first':
                    problem = f"{multiplicand} × (    ) = {result}"
                else:
                    problem = f"(    ) × {multiplier} = {result}"

            elif operation == 'divide':
                if not multiplication_table_divisions:
                    break
                dividend, divisor, quotient = random.choice(multiplication_table_divisions)
                problem = f"{dividend} ÷ {divisor} ="
                
            elif operation == 'divide_fill':
                if not multiplication_table_divisions:
                    break
                fill_position = random.choice(['dividend', 'divisor', 'quotient'])
                dividend, divisor, quotient = random.choice(multiplication_table_divisions)
                if fill_position == 'dividend':
                    problem = f"____ ÷ {divisor} = {quotient}"
                elif fill_position == 'divisor':
                    problem = f"{dividend} ÷ ____ = {quotient}"
                else:
                    problem = f"{dividend} ÷ {divisor} = ____"
                
            elif operation == 'triple_add':
                a = random.randint(1, 50)
                b = random.randint(1, min(50, 99 - a))
                c = random.randint(1, min(30, 100 - a - b))
                problem = f"{a} + {b} + {c} ="
                
            elif operation == 'triple_sub':
                a = random.randint(20, 80)
                b = random.randint(1, min(30, a - 1))
                c = random.randint(1, min(30, a - b))
                problem = f"{a} - {b} - {c} ="
                
            elif operation == 'mixed_three':
                pattern_type = random.choice(['+-', '-+'])
                if pattern_type == '+-':
                    a = random.randint(1, 70)
                    b = random.randint(1, min(30, 100 - a))
                    c = random.randint(1, min(30, a + b))
                    problem = f"{a} + {b} - {c} ="
                else:
                    a = random.randint(10, 70)
                    b = random.randint(1, min(30, a))
                    c_max = min(30, 100 - (a - b))
                    c = random.randint(1, c_max) if c_max > 0 else 0
                    problem = f"{a} - {b} + {c} =" if c_max > 0 else f"{a} - {b} ="

            elif operation == 'comparison_expr':
                expr_type = random.choice(['add_add', 'add_sub', 'sub_add', 'mult_mult', 'add_mult', 'div_div', 'add_div'])
                
                if expr_type == 'add_add':
                    a1 = random.randint(0, 99)
                    b1 = random.randint(0, 100 - a1) if a1 < 100 else 0
                    expr1 = f"{a1} + {b1}"
                    a2 = random.randint(0, 99)
                    b2 = random.randint(0, 100 - a2) if a2 < 100 else 0
                    expr2 = f"{a2} + {b2}"
                elif expr_type == 'add_sub':
                    a1 = random.randint(0, 99)
                    b1 = random.randint(0, 100 - a1) if a1 < 100 else 0
                    expr1 = f"{a1} + {b1}"
                    a2 = random.randint(1, 100)
                    b2 = random.randint(0, a2)
                    expr2 = f"{a2} - {b2}"
                elif expr_type == 'sub_add':
                    a1 = random.randint(1, 100)
                    b1 = random.randint(0, a1)
                    expr1 = f"{a1} - {b1}"
                    a2 = random.randint(0, 99)
                    b2 = random.randint(0, 100 - a2) if a2 < 100 else 0
                    expr2 = f"{a2} + {b2}"
                elif expr_type == 'mult_mult':
                    mult1 = random.randint(1, 9)
                    mult2 = random.randint(1, 9)
                    num1 = random.randint(1, 9)
                    num2 = random.randint(1, 9)
                    expr1 = f"{num1} × {mult1}"
                    expr2 = f"{num2} × {mult2}"
                elif expr_type == 'div_div':
                    if not multiplication_table_divisions:
                        break
                    dividend1, divisor1, quotient1 = random.choice(multiplication_table_divisions)
                    dividend2, divisor2, quotient2 = random.choice(multiplication_table_divisions)
                    expr1 = f"{dividend1} ÷ {divisor1}"
                    expr2 = f"{dividend2} ÷ {divisor2}"
                elif expr_type == 'add_div':
                    a1 = random.randint(1, 80)
                    b1 = random.randint(1, min(20, 99 - a1))
                    expr1 = f"{a1} + {b1}"
                    if not multiplication_table_divisions:
                        break
                    dividend, divisor, quotient = random.choice(multiplication_table_divisions)
                    expr2 = f"{dividend} ÷ {divisor}"
                else:
                    a1 = random.randint(0, 99)
                    b1 = random.randint(1, 100 - a1) if a1 < 100 else 0
                    expr1 = f"{a1} + {b1}"
                    mult = random.randint(1, 9)
                    num = random.randint(1, 9)
                    expr2 = f"{num} × {mult}"
                problem = f"{expr1} ◯ {expr2}"    

            elif operation == 'compare_num_expr':
                num_on_left = random.choice([True, False])
                expr_type = random.choice(['add', 'sub', 'mult', 'div'])
                
                if expr_type == 'add':
                    a = random.randint(0, 99)
                    b = random.randint(1, 100 - a) if a < 100 else 0
                    expr = f"{a} + {b}"
                    val = a + b
                elif expr_type == 'sub':
                    a = random.randint(1, 100)
                    b = random.randint(0, a)
                    expr = f"{a} - {b}"
                    val = a - b
                elif expr_type == 'mult':
                    mult = random.randint(1, 9)
                    num = random.randint(1, 9)
                    expr = f"{num} × {mult}"
                    val = num * mult
                else:
                    if not multiplication_table_divisions:
                        break
                    dividend, divisor, quotient = random.choice(multiplication_table_divisions)
                    expr = f"{dividend} ÷ {divisor}"
                    val = quotient
                    
                variation = random.choice([0, random.randint(1, 3), -random.randint(1, 3)])
                num_val = val + variation
                
                if num_on_left:
                    problem = f"{num_val} ○ {expr}"
                else:
                    problem = f"{expr} ○ {num_val}"

            if problem and problem not in seen_problems:
                problems.append(problem)
                seen_problems.add(problem)
                break  # 生成成功后退出内层循环
    
    # 生成 2 道万以内竖式题目
    vertical_problems = []
    
    va_num1 = random.randint(1000, 8999)
    va_num2 = random.randint(100, 9999 - va_num1)
    vertical_problems.append({'type': 'add', 'num1': va_num1, 'num2': va_num2})
    
    vs_num1 = random.randint(2000, 9999)
    vs_num2 = random.randint(100, vs_num1)
    vertical_problems.append({'type': 'sub', 'num1': vs_num1, 'num2': vs_num2})
    
    return problems, vertical_problems


def create_math_pdf(problems, vertical_problems, filename="Math_Problems.pdf"):
    """创建包含数学题目的 PDF"""
    pdf = FPDF()
    pdf.add_page()
    
    pdf.add_font("NotoSansSC", "", "D://kousuan//studyMath//NotoSansSC-6.ttf", uni=True)
    pdf.add_font("NotoSansSC", "B", "D://kousuan//studyMath//Noto-Sans-SC-Bold-2.ttf", uni=True)

    pdf.set_auto_page_break(False)
    pdf.set_margins(20, 15, 20)
    
    # 【修改】添加 align="C" 使姓名行居中
    pdf.set_font("NotoSansSC", "", 14)
    pdf.cell(0, 8, f"姓名：________________    日期：________________    用时：________________", ln=True, align="C")
    pdf.ln(5)
    
    pdf.set_font("NotoSansSC", "", 13)
    
    col_width = 45
    left_margin = 20
    spacing = 5
    row_height = 9
    bottom_margin = 10
    
    col_positions = [
        left_margin,
        left_margin + col_width + spacing,
        left_margin + (col_width + spacing) * 2,
        left_margin + (col_width + spacing) * 3,
        left_margin + (col_width + spacing) * 4
    ]
    
    problem_count = len(problems)
    rows_needed = (problem_count + 4) // 5
    
    last_row_y = pdf.get_y()
    
    for i in range(rows_needed):
        y_position = pdf.get_y()
        
        if y_position > 190:
            break
        
        for col in range(5):
            idx = i * 5 + col
            if idx < problem_count:
                pdf.set_xy(col_positions[col], y_position)
                pdf.cell(col_width, row_height, f"{problems[idx]}", border=0)
        
        last_row_y = y_position + row_height
        
        if (i + 1) < rows_needed:
            pdf.ln(bottom_margin)
    
    # 添加竖式计算题目
    if vertical_problems:
        pdf.set_y(last_row_y + 10)
        
        current_y = pdf.get_y()
        pdf.line(15, current_y, 195, current_y)
        pdf.ln(2)
        
        pdf.set_font("NotoSansSC", "B", 14)
        pdf.cell(0, 7, "竖式计算：", ln=True, align="L")
        pdf.ln(3)
        
        pdf.set_font("NotoSansSC", "", 15)
        
        page_width = pdf.w
        vertical_start_y = pdf.get_y()
        
        for i, prob in enumerate(vertical_problems):
            if i == 0:
                base_x = 40
            else:
                base_x = 130
            
            start_y = vertical_start_y
            
            n1 = str(prob['num1'])
            n2 = str(prob['num2'])
            op = "+" if prob['type'] == 'add' else "-"
            line2_text = f"{op} {n2}"
            
            max_width = max(len(n1), len(line2_text)) * 5
            
            pdf.set_xy(base_x, start_y)
            pdf.cell(max_width, 7, n1, border=0, align="R")
            
            pdf.set_xy(base_x, start_y + 7)
            pdf.cell(max_width, 7, line2_text, border=0, align="R")
            
            line_y = start_y + 14
            pdf.line(base_x, line_y, base_x + max_width, line_y)
        
        pdf.set_y(vertical_start_y + 45)

    pdf.output(filename)
    return filename


def main():
    print("数学题生成器 (带 PDF 导出功能)")
    print("支持：100 以内加减法，乘法口诀，万以内竖式")
    
    try:
        num_problems = int(input("\n请输入要生成的题目数量 (建议 20-50): "))
        if num_problems < 1:
            num_problems = 100
    except ValueError:
        num_problems = 100
    
    filename = input("输入 PDF 文件名 (回车使用默认名称): ").strip()
    if not filename:
        filename = f"Math_Problems_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    elif not filename.lower().endswith('.pdf'):
        filename += '.pdf'
    
    problems, vertical_problems = generate_math_problems(num_problems)
    
    # 打印题目类型统计
    type_count = {}
    for p in problems:
        if '◯' in p and p.count('+') + p.count('-') + p.count('×') + p.count('÷') > 1:
            t = '算式比较'
        elif '◯' in p:
            t = '算式与数字比较'
        elif '____' in p and '÷' in p:
            t = '除法填空'
        elif '÷' in p:
            t = '除法'
        elif '(' in p and '×' in p:
            t = '乘法填空'
        elif '×' in p:
            t = '乘法'
        elif '(' in p and '-' in p:
            t = '减法填空'
        elif '-' in p:
            t = '减法'
        elif '(' in p and '+' in p:
            t = '加法填空'
        elif '+' in p:
            t = '加法'
        else:
            t = '其他'
        type_count[t] = type_count.get(t, 0) + 1
    
    print(f"\n题目类型统计:")
    for t, c in sorted(type_count.items()):
        print(f"  {t}: {c}道")
    print(f"  竖式计算：2 道")
    
    print(f"\n正在生成 {num_problems} 道普通题目 + 2 道竖式题目并创建 PDF...")
    
    pdf_file = create_math_pdf(problems, vertical_problems, filename)
    
    print(f"\n生成完成！PDF 文件已保存为：{pdf_file}")
    print("温馨提示：请确保已安装支持中文的 Noto Sans SC 字体，或替换为其他中文字体")


if __name__ == "__main__":
    main()