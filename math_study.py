import random
from fpdf import FPDF
import datetime

def generate_math_problems(num_problems=10):
    # 预先生成乘法口诀表范围内的除法题示例
    multiplication_table_divisions = []
    for divisor in range(2, 10):
        for quotient in range(1, 10):
            dividend = divisor * quotient
            if 10 <= dividend <= 81:
                multiplication_table_divisions.append((dividend, divisor, quotient))

    """生成100以内加减法和2、3、4乘法题目"""
    problems = []
    seen_problems = set()  # 用于记录已生成的题目
     # 定义题目类型及其概率权重
    problem_types = [
        ('two_num_add', 10),    # 两位数加法
        ('two_num_add_fill', 5),# 两位数加法(填空)
        ('two_num_sub', 10),    # 两位数减法
        ('two_num_sub_fill', 5),# 两位数减法(填空)
        ('multiply', 20),       # 乘法
        ('multiply_fill', 13),  # 乘法(填空)
        ('triple_add', 0),     # 三个数连加
        ('triple_sub', 0),     # 三个数连减
        ('mixed_three', 2),     # 三个数混合连加减
        ('comparison_expr', 1), # 算式比较
        ('compare_num_expr', 1), # 算式与数字比较
        ('divide', 18), # 新增
        ('divide_fill', 15) # 新增
    ]

    # 创建题型队列，确保每种题型生成指定数量
    type_queue = []
    for op_type, count in problem_types:
        if count > 0:
            # 将题型添加到队列中
            type_queue.extend([op_type] * count)
    #print(f"题型队列: {type_queue}")
    
    # 随机打乱题型顺序
    random.shuffle(type_queue)
    
    # 生成100道不重复的题目
    for operation in type_queue:
        problem = None
        attempts = 0
        max_attempts = 100  # 防止无限循环
        while problem is None or problem in seen_problems:
            attempts += 1
            if attempts > max_attempts:
                # 如果无法生成新题目，跳过该题型
                break
            
            if operation == 'two_num_add':  # 两位数加法
                # 修正：避免100 + 0问题
                a = random.randint(0, 99)  # a最大99
                b = random.randint(0, 100 - a) if a < 100 else 0
                problem = f"{a} + {b} ="
            
            elif operation == 'two_num_add_fill':  # 两位数加法(填空)
                fill_position = random.choice(['first', 'second'])
                a = random.randint(0, 99)  # a最大99
                b = random.randint(0, 100 - a) if a < 100 else 0
                
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
                a = random.randint(1, 100)  # a最小1
                b = random.randint(0, a)
                
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

            elif operation == 'divide':  # 除法（乘法口诀范围内）
                if not multiplication_table_divisions:
                    continue
                
                dividend, divisor, quotient = random.choice(multiplication_table_divisions)
                problem = f"{dividend} ÷ {divisor} ="
                
            elif operation == 'divide_fill':  # 除法(填空)
                if not multiplication_table_divisions:
                    continue
                
                fill_position = random.choice(['dividend', 'divisor', 'quotient'])
                dividend, divisor, quotient = random.choice(multiplication_table_divisions)
                
                if fill_position == 'dividend':   # 填空被除数
                    problem = f"____ ÷ {divisor} = {quotient}"
                elif fill_position == 'divisor':  # 填空除数
                    problem = f"{dividend} ÷ ____ = {quotient}"
                else:  # 填空商
                    problem = f"{dividend} ÷ {divisor} = ____"
                
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

            elif operation == 'comparison_expr':  # 算式比较
                # 随机生成两个算式
                expr_type = random.choice(['add_add', 'add_sub', 'sub_add', 'mult_mult', 'add_mult', 'div_div', 'add_div'])
                
                if expr_type == 'add_add':  # 加法 vs 加法
                    a1 = random.randint(0, 99)
                    b1 = random.randint(0, 100 - a1) if a1 < 100 else 0
                    expr1 = f"{a1} + {b1}"
                    val1 = a1 + b1
                    
                    a2 = random.randint(0, 99)
                    b2 = random.randint(0, 100 - a2) if a2 < 100 else 0
                    expr2 = f"{a2} + {b2}"
                    val2 = a2 + b2
                    
                elif expr_type == 'add_sub':  # 加法 vs 减法
                    a1 = random.randint(0, 99)
                    b1 = random.randint(0, 100 - a1) if a1 < 100 else 0
                    expr1 = f"{a1} + {b1}"
                    val1 = a1 + b1
                    
                    a2 = random.randint(1, 100)
                    b2 = random.randint(0, a2)
                    expr2 = f"{a2} - {b2}"
                    val2 = a2 - b2
                    
                elif expr_type == 'sub_add':  # 减法 vs 加法
                    a1 = random.randint(1, 100)
                    b1 = random.randint(0, a1)
                    expr1 = f"{a1} - {b1}"
                    val1 = a1 - b1
                    
                    a2 = random.randint(0, 99)
                    b2 = random.randint(0, 100 - a2) if a2 < 100 else 0
                    expr2 = f"{a2} + {b2}"
                    val2 = a2 + b2
                    
                elif expr_type == 'mult_mult':  # 乘法 vs 乘法
                    mult1 = random.randint(1, 9)
                    mult2 = random.randint(1, 9)
                    num1 = random.randint(1, 9)
                    num2 = random.randint(1, 9)
                    expr1 = f"{num1} × {mult1}"
                    val1 = num1 * mult1
                    expr2 = f"{num2} × {mult2}"
                    val2 = num2 * mult2
                
                elif expr_type == 'div_div':  # 除法 vs 除法
                    if not multiplication_table_divisions:
                        continue
                    
                    dividend1, divisor1, quotient1 = random.choice(multiplication_table_divisions)
                    dividend2, divisor2, quotient2 = random.choice(multiplication_table_divisions)
                    
                    expr1 = f"{dividend1} ÷ {divisor1}"
                    expr2 = f"{dividend2} ÷ {divisor2}"
                    
                elif expr_type == 'add_div':  # 加法 vs 除法
                    a1 = random.randint(1, 80)
                    b1 = random.randint(1, min(20, 99 - a1))
                    expr1 = f"{a1} + {b1}"
                    
                    if not multiplication_table_divisions:
                        continue
                    
                    dividend, divisor, quotient = random.choice(multiplication_table_divisions)
                    expr2 = f"{dividend} ÷ {divisor}"
                    
                else:  # add_mult: 加法 vs 乘法
                    a1 = random.randint(0, 99)
                    b1 = random.randint(1, 100 - a1) if a1 < 100 else 0
                    expr1 = f"{a1} + {b1}"
                    val1 = a1 + b1
                    
                    mult = random.randint(1, 9)
                    num = random.randint(1, 9)
                    expr2 = f"{num} × {mult}"
                    val2 = num * mult

                problem = f"{expr1} ◯ {expr2}"    

            elif operation == 'compare_num_expr':  # 算式与数字比较
                num_on_left = random.choice([True, False])
                expr_type = random.choice(['add', 'sub', 'mult', 'div'])
                
                if expr_type == 'add':  # 加法
                    a = random.randint(0, 99)
                    b = random.randint(1, 100 - a) if a < 100 else 0
                    expr = f"{a} + {b}"
                    val = a + b
                    
                elif expr_type == 'sub':  # 减法
                    a = random.randint(1, 100)
                    b = random.randint(0, a)
                    expr = f"{a} - {b}"
                    val = a - b
                    
                elif expr_type == 'mult':   # 乘法
                    mult = random.randint(1, 9)
                    num = random.randint(1, 9)
                    expr = f"{num} × {mult}"
                    val = num * mult
                
                else:  # 除法
                    if not multiplication_table_divisions:
                        continue
                    
                    dividend, divisor, quotient = random.choice(multiplication_table_divisions)
                    expr = f"{dividend} ÷ {divisor}"
                    val = quotient
                    
                variation = random.choice([0, random.randint(1, 3), -random.randint(1, 3)])
                num_val = val + variation
                
                # 使用圆形符号 ○ 作为填空位置
                if num_on_left:
                    problem = f"{num_val} ○ {expr}"
                else:
                    problem = f"{expr} ○ {num_val}"

        if problem and problem not in seen_problems:
            problems.append(problem)
            seen_problems.add(problem)
    
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
    pdf.set_auto_page_break(False)  # 禁用自动分页
    
    # 使用系统默认字体
    pdf.set_font("NotoSansSC", size=10)
    #pdf.set_left_margin(20)
    
    # 标题
    """ pdf.set_font("NotoSansSC", "B", 16)
    pdf.cell(0, 15, "小学数学练习题", ln=True, align="C") """
    
    # 日期和难度信息
    pdf.set_font("NotoSansSC", "", 15)
    today = datetime.datetime.now().strftime("%Y年%m月%d日")
    pdf.cell(0, 8, f"姓名：________________        日期：________________        用时：________________", ln=True)
    pdf.ln(7)
    
    # 说明文字
    """ pdf.set_font("NotoSansSC", "", 10)
    pdf.cell(0, 6, "题目范围: 100以内加减法, 2、3、4的乘法", ln=True)
    pdf.cell(0, 6, "建议时间: 20分钟", ln=True)
    pdf.ln(10) """
    
# 添加题目（一行四列布局）
    pdf.set_font("NotoSansSC", "", 13)
    
    # 定义四列的宽度和位置
    col_width = 45  # 每列宽度
    left_margin = 10  # 左边距
    spacing = 5  # 列间距
    row_height = 8  # 行高
    bottom_margin = 10.5  # 下边距
    
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
        if (i + 1) < rows_needed:
            pdf.ln(bottom_margin)  # 行间距
        
        # 每5行增加额外间距
        """ if (i + 1) % 5 == 0:
            pdf.ln(1) """
    
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