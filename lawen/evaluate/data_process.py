import json


def GTrajectoryProcess(task_name, gt_trajectory_path):
    """输入.

    Args:
        task_name (str): 任务描述
        gt_trajectory_path (str): 轨迹Ground_truth路径

    Returns:
        str: 处理后的轨迹
    """
    with open(gt_trajectory_path, "r", encoding="utf-8") as f:
        content = json.load(f)
    for con in content:
        if con['confirmed_task'] == task_name:
            ground_truth = con
    raw_gt_trajectory = ground_truth['action_reprs']
    gt_trajectory = []
    type = ''
    type_list = []
    name = ''
    name_list = []
    action_list = []
    extra_list = []

    for act in raw_gt_trajectory:
        for sym in act:
            type = type + sym
            if sym == ']':
                break
        type_list.append(type)
        act = act.replace(type + "  ", '')
        type = ''
        for sym in act:
            if sym == '-':
                break
            name = name + sym
        name = name[:-1]
        name_list.append(name)
        act = act.replace(name + " -> ", '')
        name = ''
        if "CLICK" in act or "hover" in act:
            action_list.append("CLICK")
            extra_list.append('')
        elif "TYPE" in act:
            action_list.append("TYPE")
            extra = act.replace("TYPE: ", '')
            extra_list.append(extra)


        elif "SELECT" in act:
            action_list.append("SELECT")
            extra = act.replace("SELECT: ", '')
            extra_list.append(extra)

    for i in range(len(action_list)):
        if extra_list[i] == '':
            gt_trajectory.append(dict.fromkeys(['action'], {'name': action_list[i],
                                                            'input_action_args': {'target_element': name_list[i]}}))
        elif action_list[i] == "TYPE":
            gt_trajectory.append(dict.fromkeys(['action'], {'name': action_list[i],
                                                            'input_action_args': {'target_element': name_list[i],
                                                                                  "text": extra_list[i]}}))
        elif action_list[i] == "SELECT":
            gt_trajectory.append(dict.fromkeys(['action'], {'name': action_list[i],
                                                            'input_action_args': {'target_element': name_list[i],
                                                                                  "option": extra_list[i]}}))
    return gt_trajectory


def TrajectoryProcess(trajectory):
    """输入.

    Args:
        trajectory (list(dict)): 智能体生成的轨迹

    Returns:
        str: 处理后的轨迹
    """
    result = []

    for tra in trajectory:
        result.append(dict.fromkeys(['action'], tra['action']))
    return result
