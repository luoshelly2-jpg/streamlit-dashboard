import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

def load_data():
    """加载data.xlsx文件"""
    try:
        df = pd.read_excel('data.xlsx', engine='openpyxl')
        return df
    except FileNotFoundError:
        st.error("找不到data.xlsx文件，请确保文件存在于当前目录")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"加载文件时出错: {e}")
        return pd.DataFrame()

def load_uploaded_file(uploaded_file):
    """加载上传的Excel文件"""
    try:
        df = pd.read_excel(uploaded_file, engine='openpyxl')
        
        # 验证文件格式（基本检查）
        required_columns = ['日期', '项目', '任务', '进度', '状态', '详细描述', '风险', '责任人']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            st.warning(f"上传的文件缺少以下列: {', '.join(missing_columns)}")
            st.info("请确保文件包含以下列: 日期, 项目, 任务, 进度, 状态, 详细描述, 风险, 责任人")
            return None
            
        st.success("文件格式验证通过！")
        return df
        
    except Exception as e:
        st.error(f"读取上传文件时出错: {e}")
        return None

def save_uploaded_file(uploaded_file):
    """保存上传的文件为data.xlsx"""
    try:
        # 读取上传的文件内容
        df = pd.read_excel(uploaded_file, engine='openpyxl')
        
        # 保存为data.xlsx
        df.to_excel('data.xlsx', index=False, engine='openpyxl')
        st.success("文件上传并保存成功！")
        return df
        
    except Exception as e:
        st.error(f"保存上传文件时出错: {e}")
        return None

def generate_ai_report(df):
    """生成AI周报（示例功能）"""
    if df.empty:
        return "无法生成报告：数据为空"
    
    # 简单的报告生成逻辑
    total_projects = len(df)
    completed_projects = len(df[df['状态'] == '已完成'])
    in_progress_projects = len(df[df['状态'] == '进行中'])
    
    report = f"# 📊 本周工作周报\n\n"
    report += f"**统计概览:**\n"
    report += f"- 总项目数: {total_projects}\n"
    report += f"- 已完成项目: {completed_projects}\n"
    report += f"- 进行中项目: {in_progress_projects}\n\n"
    
    report += f"**项目详情:**\n"
    for _, row in df.iterrows():
        report += f"- **{row['项目']}**: {row['任务']} (进度: {row['进度']}%, 状态: {row['状态']}, 责任人: {row['责任人']})\n"
    
    report += f"\n**风险评估:**\n"
    for _, row in df.iterrows():
        if pd.notna(row['风险']):
            report += f"- {row['项目']}: {row['风险']}\n"
    
    return report

def create_status_pie_chart(df):
    """创建状态分布饼状图"""
    if df.empty:
        return None
    
    status_counts = df['状态'].value_counts()
    fig = px.pie(
        values=status_counts.values,
        names=status_counts.index,
        title="项目状态分布",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(showlegend=False)
    return fig

def save_data(df):
    """保存数据到Excel文件"""
    try:
        df.to_excel('data.xlsx', index=False, engine='openpyxl')
        st.success("数据保存成功！")
        return True
    except Exception as e:
        st.error(f"保存数据时出错: {e}")
        return False

def main():
    # 页面配置
    st.set_page_config(
        page_title="工作周报看板",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # 标题
    st.title("📊 工作周报看板")
    
    # 文件上传功能
    st.sidebar.header("📤 数据上传")
    uploaded_file = st.sidebar.file_uploader(
        "上传Excel文件",
        type=["xlsx"],
        help="上传包含办公数据的Excel文件，支持.xlsx格式"
    )
    
    if uploaded_file is not None:
        if st.sidebar.button("💾 保存上传的文件"):
            with st.spinner("正在处理上传的文件..."):
                df = save_uploaded_file(uploaded_file)
                if df is not None:
                    st.sidebar.success("文件已保存为data.xlsx")
                    st.rerun()
        
        # 预览上传的文件
        st.sidebar.subheader("📋 上传文件预览")
        preview_df = load_uploaded_file(uploaded_file)
        if preview_df is not None:
            st.sidebar.dataframe(preview_df.head(3), use_container_width=True)
            st.sidebar.write(f"文件包含 {len(preview_df)} 行数据")
    
    # 加载数据
    df = load_data()
    
    if df.empty:
        st.warning("没有数据可显示")
        return
    
    # 创建标签页布局
    tab1, tab2, tab3 = st.tabs(["📋 数据编辑", "📊 数据可视化", "🤖 AI 周报生成"])
    
    with tab1:
        st.header("📋 数据编辑表格")
        
        # 使用st.data_editor创建可编辑表格
        edited_df = st.data_editor(
            df,
            use_container_width=True,
            height=400,
            num_rows="dynamic",
            column_config={
                "日期": st.column_config.DateColumn(
                    "日期",
                    format="YYYY-MM-DD",
                    required=True
                ),
                "进度": st.column_config.ProgressColumn(
                    "进度",
                    help="项目完成进度",
                    format="%d%%",
                    min_value=0,
                    max_value=100
                ),
                "状态": st.column_config.SelectboxColumn(
                    "状态",
                    help="项目当前状态",
                    options=["未开始", "进行中", "已完成", "暂停", "待审核"]
                )
            }
        )
        
        # 保存按钮
        if st.button("💾 保存更改", use_container_width=True):
            if save_data(edited_df):
                df = load_data()  # 重新加载数据
        
        # 显示一些统计信息
        st.subheader("📈 统计信息")
        col1_1, col1_2, col1_3, col1_4 = st.columns(4)
        
        with col1_1:
            st.metric("总项目数", len(df))
        
        with col1_2:
            completed = len(df[df['状态'] == '已完成'])
            st.metric("已完成", completed)
        
        with col1_3:
            in_progress = len(df[df['状态'] == '进行中'])
            st.metric("进行中", in_progress)
            
        with col1_4:
            unique_persons = df['责任人'].nunique()
            st.metric("责任人数量", unique_persons)
    
    with tab2:
        st.header("📊 数据可视化")
        
        # 状态分布饼图
        st.subheader("项目状态分布")
        pie_chart = create_status_pie_chart(df)
        if pie_chart:
            st.plotly_chart(pie_chart, use_container_width=True)
        
        # 责任人分布
        st.subheader("责任人项目分布")
        person_counts = df['责任人'].value_counts()
        fig_person = px.bar(
            x=person_counts.index,
            y=person_counts.values,
            title="各责任人负责项目数量",
            labels={'x': '责任人', 'y': '项目数量'}
        )
        st.plotly_chart(fig_person, use_container_width=True)
        
        # 进度分布
        st.subheader("项目进度分布")
        fig_progress = px.histogram(
            df,
            x='进度',
            title="项目进度分布",
            nbins=10
        )
        st.plotly_chart(fig_progress, use_container_width=True)
    
    with tab3:
        st.header("🤖 AI 周报生成")
        
        if st.button("🚀 生成 AI 周报", use_container_width=True):
            with st.spinner("正在生成周报..."):
                report = generate_ai_report(df)
                
            st.success("周报生成成功！")
            st.markdown("---")
            st.markdown(report)
            
            # 提供下载功能
            report_filename = f"weekly_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            st.download_button(
                label="📥 下载周报",
                data=report,
                file_name=report_filename,
                mime="text/markdown",
                use_container_width=True
            )
        else:
            st.info("点击按钮生成基于当前数据的AI周报")
        
        # 显示数据基本信息
        st.markdown("---")
        st.subheader("ℹ️ 数据信息")
        st.write(f"数据行数: {len(df)}")
        st.write(f"数据列数: {len(df.columns)}")
        st.write(f"最后更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 显示责任人列表
        st.subheader("👥 责任人列表")
        responsible_persons = df['责任人'].unique()
        for person in responsible_persons:
            person_projects = df[df['责任人'] == person]
            st.write(f"**{person}**: {len(person_projects)} 个项目")

if __name__ == "__main__":
    main()