import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_office_data():
    # 设置随机种子以确保结果可重现
    np.random.seed(42)
    
    # 生成5条数据
    num_records = 5
    
    # 日期字段：生成最近5个工作日的日期
    dates = [datetime.now().date() - timedelta(days=i) for i in range(num_records)]
    
    # 项目字段
    projects = ['网站改版', '移动应用开发', '数据分析平台', '客户管理系统', '内部培训系统']
    
    # 任务字段
    tasks = [
        '首页设计评审',
        '用户登录功能开发',
        '数据清洗脚本编写',
        '客户信息导入',
        '培训材料准备'
    ]
    
    # 进度字段：0-100之间的随机整数
    progress = np.random.randint(30, 100, num_records)
    
    # 状态字段
    statuses = ['进行中', '已完成', '待审核', '暂停', '进行中']
    
    # 详细描述字段
    descriptions = [
        '完成首页UI设计和交互原型，等待团队评审',
        '开发用户登录认证功能，包括密码加密和会话管理',
        '编写数据清洗脚本，处理缺失值和异常数据',
        '导入客户基本信息到新系统，验证数据完整性',
        '准备培训PPT和实操案例，安排培训时间'
    ]
    
    # 风险字段
    risks = [
        '设计风格可能不符合品牌规范',
        '安全漏洞风险需要额外测试',
        '数据质量可能影响分析结果',
        '数据迁移可能出现丢失',
        '参与度可能不高需要宣传'
    ]
    
    # 责任人字段
    responsible_persons = ['张三', '李四', '王五', '赵六', '钱七']
    
    # 创建DataFrame
    data = {
        '日期': dates,
        '项目': projects,
        '任务': tasks,
        '进度': progress,
        '状态': statuses,
        '详细描述': descriptions,
        '风险': risks,
        '责任人': responsible_persons
    }
    
    df = pd.DataFrame(data)
    
    # 保存到Excel文件
    df.to_excel('data.xlsx', index=False, engine='openpyxl')
    
    print(f"成功生成 {num_records} 条办公数据到 data.xlsx")
    print("\n生成的数据预览:")
    print(df)
    
    return df

if __name__ == "__main__":
    generate_office_data()