import pandas as pd


if __name__ == '__main__':

    # 预处理后的数据（以钻井编号划分）地址，参数为 hole_full_name, 例如 U1522A
    data_path = r'.\海洋数据处理与可视化\output\年代与各种数据的关系图\预处理后的数据（以钻井编号划分）\{hole_full_name}.csv'

    # 保存数据，参数为 new_name, 例如 U1522ABCD
    save_path = r'.\海洋数据处理与可视化\output\年代与各种数据的关系图\合并后的预处理数据\{new_name}.csv'

    # 列举所有的钻井
    hole_list = {
        'ross': {
            # 'U1521': ['A'],
            'U1522': ['A'],
            'U1523': ['A', 'B', 'E'],
            'U1524': ['A', 'C'],
            'U1525': ['A'],
        },
        'amundsen': {
            'U1533': ['A', 'B', 'C', 'D'],
        }
    }

    # 合并后的
    will_be_merged = {
        'ross': {
            'U1522A': ['U1522A'],
            'U1523ABE': ['U1523A', 'U1523B', 'U1523E'],
            'U1524A': ['U1524A'],
            'U1524C': ['U1524C'],
            'U1525A': ['U1525A'],
        },
        'amundsen': {
            'U1533A': ['U1533A'],
            'U1533B': ['U1533B'],
            'U1533C': ['U1533C'],
            'U1533D': ['U1533D']
        }
    }

    for sea, merged_holes_list in will_be_merged.items():
        for new_name, holes in merged_holes_list.items():

            new = pd.DataFrame({})

            data = []

            for hole in holes:
                data = pd.read_csv(data_path.format(hole_full_name=hole), index_col=0)

                new = pd.concat([new, data], ignore_index=True)

            # 根据地层年代排序
            new = new.sort_values(by='Time (kyr from J2000)', ascending=False).reset_index(drop=True)

            new.to_csv(save_path.format(new_name=new_name))
