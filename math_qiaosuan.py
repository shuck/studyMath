# file: d:\kousuan\studyMath\math_qiaosuan.py
import random
from fpdf import FPDF
import datetime

def generate_qiaosuan_problems(total_problems=10):
    """
    生成 3 位数加减法巧算题目
    加法巧算：第二个数接近整百/整十（多一点或少一点）
    减法巧算：减数接近整百/整十（多一点或少一点）
    """
    # 加法和减法各占一半
    num_add = total_problems // 2
    num_sub = total_problems - num_add  # 确保总数正确
    
    add_problems = []
    sub_problems = []
    seen_add = set()
    seen_sub = set()
    
    # 生成加法巧算题目（3 位数凑整法）
    while len(add_problems) < num_add:
        # 第一个数：3 位数
        a = random.randint(101, 899)
        
        # 第二个数：接近整百或整十（多一点或少一点）
        choice = random.choice(['near_hundred', 'near_ten'])
        
        if choice == 'near_hundred':
            # 接近整百（如 198, 202, 297, 303 等）
            base_hundred = random.randint(2, 8) * 100
            offset = random.choice([-3, -2, -1, 1, 2, 3])  # 多一点或少一点
            b = base_hundred + offset
        else:
            # 接近整十（如 198, 202, 189, 211 等）
            base_ten = random.randint(2, 9) * 10
            offset = random.choice([-3, -2, -1, 1, 2, 3])  # 多一点或少一点
            b = base_ten + offset
        
        # 确保第二个数是正数且合理
        if b < 10 or b > 500:
            continue
        
        # 确保和在 1000 以内
        if a + b > 1000:
            continue
        
        problem = f"{a} + {b} ="
        if problem not in seen_add:
            add_problems.append(problem)
            seen_add.add(problem)
    
    # 生成减法巧算题目（3 位数凑整法）
    while len(sub_problems) < num_sub:
        # 被减数：3 位数
        a = random.randint(301, 999)
        
        # 减数：接近整百或整十（多一点或少一点）
        choice = random.choice(['near_hundred', 'near_ten'])
        
        if choice == 'near_hundred':
            # 接近整百（如 198, 202, 297, 303 等）
            base_hundred = random.randint(1, 7) * 100
            offset = random.choice([-3, -2, -1, 1, 2, 3])  # 多一点或少一点
            b = base_hundred + offset
        else:
            # 接近整十（如 198, 202, 189, 211 等）
            base_ten = random.randint(2, 9) * 10
            offset = random.choice([-3, -2, -1, 1, 2, 3])  # 多一点或少一点
            b = base_ten + offset
        
        # 确保第二个数是正数且合理
        if b < 10 or b > 500:
            continue
        
        # 确保结果为正且大于 100
        if a - b < 100:
            continue
        
        problem = f"{a} - {b} ="
        if problem not in seen_sub:
            sub_problems.append(problem)
            seen_sub.add(problem)
    
    return add_problems, sub_problems


def create_qiaosuan_pdf(add_problems, sub_problems, filename="Math_QiaoSuan.pdf"):
    """创建巧算练习 PDF"""
    pdf = FPDF()
    pdf.add_page()
    
    # 添加中文字体
    pdf.add_font("NotoSansSC", "", "D://kousuan//studyMath//NotoSansSC-6.ttf", uni=True)
    pdf.add_font("NotoSansSC", "B", "D://kousuan//studyMath//Noto-Sans-SC-Bold-2.ttf", uni=True)
    
    pdf.set_auto_page_break(False)
    pdf.set_margins(20, 20, 20)
    
    # 标题
    pdf.set_font("NotoSansSC", "B", 18)
    pdf.cell(0, 10, "加减法巧算练习", ln=True, align="C")
    pdf.ln(5)
    
    # 姓名行
    pdf.set_font("NotoSansSC", "", 14)
    pdf.cell(0, 8, f"姓名：________________    日期：________________    用时：________________", ln=True, align="C")
    pdf.ln(15)
    
    # 题目布局参数
    left_margin = 20
    right_margin = 20
    page_width = pdf.w
    content_width = page_width - left_margin - right_margin
    
    # 左右两列的起始位置（左边居左，右边居左）
    left_x = left_margin
    right_x = left_margin + content_width * 0.5 + 10  # 右列起始位置
    
    # 行间距（留出足够空白做题）
    row_height = 40  # 上下留出足够空白
    font_size = 16
    
    pdf.set_font("NotoSansSC", "", font_size)
    
    # 合并题目为连续列表（左加右减交替，题号连续）
    all_problems = []
    for i in range(max(len(add_problems), len(sub_problems))):
        if i < len(add_problems):
            all_problems.append(('add', add_problems[i]))
        if i < len(sub_problems):
            all_problems.append(('sub', sub_problems[i]))
    
    start_y = pdf.get_y()
    problem_num = 1
    current_page = 1
    
    for i, (prob_type, problem) in enumerate(all_problems):
        # 计算当前行和列
        row = i // 2
        col = i % 2  # 0=左列，1=右列
        
        y_position = start_y + row * row_height
        
        # 检查是否需要换页
        if y_position > 250:
            pdf.add_page()
            current_page += 1
            start_y = 20
            y_position = start_y
            row = 0
        
        # 确定 X 位置
        if col == 0:
            x_position = left_x
        else:
            x_position = right_x
        
        # 【修改】题号用中文括号，去掉后面的点，如（1）（2）
        text = f"（{problem_num}）{problem}"
        
        pdf.set_xy(x_position, y_position)
        pdf.cell(0, 10, text, border=0)
        
        problem_num += 1
    
    pdf.output(filename)
    return filename


def main():
    print("=" * 50)
    print("    3 位数加减法巧算练习生成器")
    print("=" * 50)
    
    try:
        # 直接输入总题数
        total_problems = int(input("\n请输入要生成的题目总数 (建议 10-20): "))
        if total_problems < 2:
            total_problems = 10
        if total_problems > 30:
            total_problems = 30
    except ValueError:
        total_problems = 10
    
    filename = input("输入 PDF 文件名 (回车使用默认名称): ").strip()
    if not filename:
        filename = f"Math_QiaoSuan_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    elif not filename.lower().endswith('.pdf'):
        filename += '.pdf'
    
    print(f"\n正在生成 {total_problems} 道 3 位数巧算题目...")
    
    add_problems, sub_problems = generate_qiaosuan_problems(total_problems)
    
    pdf_file = create_qiaosuan_pdf(add_problems, sub_problems, filename)
    
    print(f"\n✅ 生成完成！PDF 文件已保存为：{pdf_file}")
    print(f"   （加法 {len(add_problems)} 道 + 减法 {len(sub_problems)} 道 = 共 {len(add_problems)+len(sub_problems)} 道）")
    print("\n📋 题目预览:")
    print("-" * 60)
    problem_num = 1
    for i in range(max(len(add_problems), len(sub_problems))):
        line = ""
        if i < len(add_problems):
            line += f"（{problem_num}）{add_problems[i]:<16}"
            problem_num += 1
        if i < len(sub_problems):
            line += f"  （{problem_num}）{sub_problems[i]}"
            problem_num += 1
        print(line)
    print("-" * 60)
    print("\n💡 巧算技巧:")
    print("   加法：第二个数接近整百/整十，如 378+198 = 378+200-2 = 576")
    print("   减法：减数接近整百/整十，如 835-202 = 835-200-2 = 633")


if __name__ == "__main__":
    main()