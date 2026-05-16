import uuid
from typing import List, Dict

# 任务的状态常量
STATUS_ALL = "所有任务"
STATUS_ACTIVE = "仅未完成"
STATUS_COMPLETED = "仅已完成"


def create_task(content: str) -> Dict:
    """
    创建一个新的任务字典。

    Args:
        content: 任务内容，非空字符串。

    Returns:
        一个包含任务数据的字典：{id, content, completed}。

    Raises:
        ValueError: 如果 content 为空或仅包含空白字符。
    """
    if not content or not content.strip():
        raise ValueError("任务内容不能为空或仅包含空白字符。")

    return {
        "id": str(uuid.uuid4()),
        "content": content.strip(),
        "completed": False
    }


def add_task(tasks: List[Dict], content: str) -> List[Dict]:
    """
    向任务列表中添加一个新任务。

    Args:
        tasks: 现有的任务列表。
        content: 新任务的内容。

    Returns:
        更新后的任务列表。
    """
    new_task = create_task(content)
    updated_tasks = list(tasks)
    updated_tasks.append(new_task)
    return updated_tasks


def delete_task(tasks: List[Dict], task_id: str) -> List[Dict]:
    """
    根据任务 ID 从列表中删除一个任务。

    Args:
        tasks: 现有的任务列表。
        task_id: 要删除的任务的 ID。

    Returns:
        更新后的任务列表。
    """
    return [task for task in tasks if task["id"] != task_id]


def toggle_task_status(tasks: List[Dict], task_id: str) -> List[Dict]:
    """
    切换指定任务的状态（已完成 <-> 未完成）。

    Args:
        tasks: 现有的任务列表。
        task_id: 要切换状态的任务的 ID。

    Returns:
        更新后的任务列表。
    """
    updated_tasks = []
    for task in tasks:
        if task["id"] == task_id:
            updated_tasks.append({**task, "completed": not task["completed"]})
        else:
            updated_tasks.append(task)
    return updated_tasks


def filter_tasks(tasks: List[Dict], filter_status: str) -> List[Dict]:
    """
    根据指定的筛选条件过滤任务列表。

    Args:
        tasks: 待过滤的任务列表。
        filter_status: 筛选条件。

    Returns:
        过滤后的任务列表。
    """
    if filter_status == STATUS_ACTIVE:
        return [task for task in tasks if not task["completed"]]
    elif filter_status == STATUS_COMPLETED:
        return [task for task in tasks if task["completed"]]
    else:  # STATUS_ALL
        return list(tasks)  # 返回副本，防止外部修改


def get_task_count_info(tasks: List[Dict]) -> str:
    """
    获取任务统计信息的字符串。

    Args:
        tasks: 当前完整的任务列表。

    Returns:
        格式化的统计信息。
    """
    total = len(tasks)
    active = sum(1 for t in tasks if not t["completed"])
    return f"共 {total} 项，未完成 {active} 项"