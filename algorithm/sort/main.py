import time
from sort.some_sort import (
    bubble_sort,
    selection_sort,
    quick_sort,
    insert_sort,
    heap_sort,
    merge_sort,
    shell_sort,
)


# 装饰器，计算排序时间
def time_count(func):
    def wrapper(list):
        start = time.clock()
        func(list)
        end = time.clock()
        print("排序时间：{0}".format(end - start))

    return wrapper


# 冒泡排序


@time_count
def exec_bubble_sort(list):
    new_l = bubble_sort(list)
    print("冒泡排序：")
    print("new_l：{0}".format(new_l))


# 选择排序
@time_count
def exec_selection_sort(list):
    new_l = selection_sort(list)
    print("选择排序：")
    print("new_l：{0}".format(new_l))


# 快速排序
@time_count
def exec_quick_sort(list):
    new_l = quick_sort(list)
    print("快速排序：")
    print("new_l：{0}".format(new_l))


# 插入排序
@time_count
def exec_insert_sort(list):
    new_l = insert_sort(list)
    print("插入排序：")
    print("new_l：{0}".format(new_l))


# 堆排序
@time_count
def exec_heap_sort(list):
    new_l = heap_sort(list)
    print("堆排序：")
    print("new_l：{0}".format(new_l))


# 归并排序
@time_count
def exec_merge_sort(list):
    new_l = merge_sort(list)
    print("归并排序：")
    print("new_l：{0}".format(new_l))


# 希尔排序
@time_count
def exec_shell_sort(list):
    new_l = shell_sort(list)
    print("希尔排序：")
    print("new_l：{0}".format(new_l))


def main():
    # 当数据量比较大的时候，设置最大递归深度，否则使用递归的算法会报错，比如快速排序
    # 获取最大递归深度：sys.getrecursionlimit()
    # import sys
    # sys.setrecursionlimit(2000)

    import numpy as np

    # 生成不重复测试数据，数据范围是1～20，数据量为10
    # import random
    # l = random.sample(range(1, 21), 10)
    # 生成可重复测试数据，数据范围是0～20，数据量为10
    data = list(np.random.randint(21, size=10))
    print("随机列表data：{0}".format(data))
    print("===============================================")
    # 执行排序
    exec_bubble_sort(data)
    exec_selection_sort(data)
    exec_quick_sort(data)
    exec_insert_sort(data)
    exec_heap_sort(data)
    exec_merge_sort(data)
    exec_shell_sort(data)


if __name__ == "__main__":
    main()
