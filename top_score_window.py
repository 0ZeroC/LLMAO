import os
import json

#遍历给定路径下fl_path的所有文件，并统计在预定义条件下的分数排名
def find_topscores(fl_path):
    top_1 = 0
    top_3 = 0
    top_5 = 0
    # 使用os.walk函数遍历fl_path目录及其所有子目录。
    # os.walk返回每个目录的路径、目录名列表和文件名列表。
    # 这里只使用目录路径（subdir）和文件名列表（files）
    for subdir, _, files in os.walk(fl_path):
        for file in files:
            file_path = os.path.join(subdir, file)#使用os.path.join拼接子目录路径和文件名
            if "sus.json" in file_path:
                #打开与sus.json文件对应的metadata.json文件。动态修改文件路径
                #这里通过替换文件路径中的"sus"为"metadata"来找到元数据文件路径，然后加载JSON数据。
                with open(file_path.replace("sus", "metadata")) as json_file:
                    meta_json = json.load(json_file)
                #打开sus.json文件，并加载JSON数据。
                with open(file_path) as json_file:
                    sus_json = json.load(json_file)
                real_bugs = meta_json["bug_line_number"]
                #这两行代码首先颠倒sus_json中的键和值，然后再次颠倒回来，
                #目的可能是为了去除重复的值，确保每个键（行号）对应唯一的值（分数）。
                temp = {val: key for key, val in sus_json.items()}
                sus_json = {val: key for key, val in temp.items()}

                #遍历排序后的sus_json字典，并用enumerate生成每个项的索引i，用来计算排名rank。
                for i, (key, value) in enumerate(sus_json.items()):
                    rank = i + 1
                    if int(key) in real_bugs:
                        if rank == 1:
                            top_1 += 1
                        if rank <= 3:
                            top_3 += 1
                        if rank <= 5:
                            top_5 += 1
                        break
    print(f"top 5: {top_5}")
    print(f"top 3: {top_3}")
    print(f"top 1: {top_1}")

if __name__ == "__main__":
    
    print(f"Top score for llmao_window")
    current_path = os.getcwd()#获取当前工作目录
    score_dir = "score_llmao_window"#文件夹名
    fl_path = f"{current_path}/{score_dir}"  #文件夹路径
    find_topscores(fl_path)#调用函数
    
    print(f"Top score for Transfer")
    score_dir = "score_transferfl"
    fl_path = f"{current_path}/{score_dir}"
    find_topscores(fl_path)
