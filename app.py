import streamlit as st
from todo_logic import (
    add_task,
    delete_task,
    toggle_task_status,
    filter_tasks,
    get_task_count_info,
    STATUS_ALL,
    STATUS_ACTIVE,
    STATUS_COMPLETED,
)

# --- 应用配置和状态初始化 ---
st.set_page_config(
    page_title="我的待办事项",
    page_icon="✅",
    layout="centered",
)

st.title("📋 我的待办事项")
st.markdown("---")

# 初始化 Session State
if 'tasks' not in st.session_state:
    st.session_state.tasks = []

if 'filter_status' not in st.session_state:
    st.session_state.filter_status = STATUS_ALL


# --- 1. 任务输入模块 ---
st.subheader("添加新任务")
with st.container():
    col1, col2 = st.columns([4, 1])
    with col1:
        new_task_input = st.text_input(
            "任务内容",
            key="new_task",
            placeholder="请输入你需要完成的事情...",
            label_visibility="collapsed",
        )
    with col2:
        add_button = st.button("➕ 添加", use_container_width=True)

    # 处理添加按钮点击事件
    if add_button:
        if new_task_input and new_task_input.strip():
            st.session_state.tasks = add_task(
                st.session_state.tasks, new_task_input
            )
            # 清空输入框：直接通过 key 设置 session state 值为空字符串
            st.session_state["new_task"] = ""
            st.rerun()
        else:
            st.error("任务内容不能为空！请填写有效任务。")

st.markdown("---")

# --- 2. 状态筛选模块 ---
st.subheader("任务管理")
filter_status = st.radio(
    "筛选状态",
    options=[STATUS_ALL, STATUS_ACTIVE, STATUS_COMPLETED],
    index=[STATUS_ALL, STATUS_ACTIVE, STATUS_COMPLETED].index(st.session_state.filter_status),
    horizontal=True,
    key="filter_status"
)
st.caption(get_task_count_info(st.session_state.tasks))

# --- 3. 任务展示与操作模块 ---
display_tasks = filter_tasks(st.session_state.tasks, st.session_state.filter_status)

if not display_tasks:
    if not st.session_state.tasks:
        st.info("🎉 太棒了！目前还没有待办事项。")
    else:
        st.info(f"没有匹配的 {st.session_state.filter_status} 任务。")
else:
    for i, task in enumerate(display_tasks):
        cols = st.columns([0.1, 0.7, 0.2], vertical_alignment="center")

        task_id = task["id"]
        task_content = task["content"]
        is_completed = task["completed"]

        # 第1列：复选框
        with cols[0]:
            checkbox_checked = st.checkbox(
                "已完成",
                value=is_completed,
                key=f"check_{task_id}",
                label_visibility="collapsed"
            )
            if checkbox_checked != is_completed:
                st.session_state.tasks = toggle_task_status(
                    st.session_state.tasks, task_id
                )
                st.rerun()

        # 第2列：任务内容
        with cols[1]:
            if is_completed:
                st.markdown(f"~~{task_content}~~")
            else:
                st.markdown(task_content)

        # 第3列：删除按钮
        with cols[2]:
            delete_button = st.button(
                "❌",
                key=f"delete_{task_id}",
                help="删除此任务",
                use_container_width=True
            )
            if delete_button:
                st.session_state.tasks = delete_task(
                    st.session_state.tasks, task_id
                )
                st.rerun()

        st.divider()

st.markdown("---")
st.caption("数据存储于浏览器会话 (Session State)，刷新页面不会丢失。")