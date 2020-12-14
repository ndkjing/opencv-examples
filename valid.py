from pandas import read_csv
import pandas as pd
from numpy import nan
import numpy as np
from numpy import isnan
from pandas import read_csv
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer  # sklearn0.23.1的功能
import datetime
from collections import Counter


# load the dataset
def load_data(csv_file_path=None):
    if csv_file_path is not None:
        dataset = read_csv(csv_file_path, header=None)
    else:
        dataset = read_csv('pima-indians-diabetes.csv', header=None)
        # 空缺值标记为0
        num_missing = (dataset[[1, 2, 3, 4, 5]] == 0).sum()
        # report the results
        print(num_missing)

        dataset[[1, 2, 3, 4, 5]] = dataset[[1, 2, 3, 4, 5]].replace(0, nan)
        # count the number of nan values in each column
        print(dataset.isnull().sum())

    print(dataset.head(20))
    return dataset


def fill_missing_value_using_mean(dataset):
    """
    将空缺值按空缺位置所在列的均值填补
    :param dataset: 传入pandas数据
    :return:
    """
    dataset[[1, 2, 3, 4, 5]] = dataset[[1, 2, 3, 4, 5]].replace(0, nan)
    # fill missing values with mean column values
    dataset.fillna(dataset.mean(), inplace=True)
    # count the number of NaN values in each column
    print(dataset.isnull().sum())


def fill_missing_value_using_iterative(dataset):
    """
    将空缺值按该行其他未空缺值计算贝叶斯回归来估计空缺值
    :param dataset: 传入pandas数据
    :return:
    """
    # dataset[[1, 2, 3, 4, 5]] = dataset[[1, 2, 3, 4, 5]].replace(0, nan)
    data = dataset.values

    X, y = data[:, 1:], data[:, 0]
    y = np.expand_dims(y,1)
    X = np.asarray(X, dtype=np.float64)
    # print total missing
    print('Missing: %d' % sum(isnan(X).flatten()))
    # define imputer
    imputer = IterativeImputer()
    # fit on the dataset
    imputer.fit(X)
    # transform the dataset
    Xtrans = imputer.transform(X)
    # print total missing
    print('Missing: %d' % sum(isnan(Xtrans).flatten()))
    print(X.shape)
    return_data = np.hstack((y,Xtrans))
    return return_data

# TODO 查找数据缺失行 用数据列均值填补
def generate_missing_row_using_mean(dataset):
    data = dataset.values


# TODO 查找数据缺失行 使用指定数据列按时间顺序缺失
def generate_missing_row_using_sequence_time(dataset):
    dataset = load_data('hour.csv')
    # print(dataset.shape)

    # print(type(dataset.values.tolist()))
    temp_dataset_list = dataset.values.tolist()
    dataset_list = []
    hours_gap = []
    pre_time, cur_time = None, None
    col_len = None
    for row in temp_dataset_list:

        # print(row)
        row_data = row[0].split('\t')
        col_len = len(row_data)
        dataset_list.append(row_data)
        # print('row_data',row_data)
        # 获取时间
        data_row_datetime = row_data[0]
        if pre_time is None and cur_time is None:
            pre_time = data_row_datetime
            cur_time = data_row_datetime
        else:

            pre_time = cur_time
            cur_time = data_row_datetime
            cur_datetime = datetime.datetime.strptime(cur_time, '%Y-%m-%d %H:%M:%S')
            pre_datetime = datetime.datetime.strptime(pre_time, '%Y-%m-%d %H:%M:%S')
            delta = cur_datetime - pre_datetime
            print(delta.days, delta.seconds)
            hours_gap.append(delta.seconds / 3600)
    print(hours_gap)
    c = Counter(hours_gap)
    # 统计最多的元素间隔，以该元素为数据时间间隔
    most_vals_gap = c.most_common(1)[0][0]
    print(most_vals_gap)
    print(len(c))
    if len(c) > 1:
        print('小时数据有缺失')
        print('缺失所在行为')
        loss_data_row_indexs = []
        for i, gap in enumerate(hours_gap):
            if gap != most_vals_gap:
                loss_val_count = (gap // most_vals_gap) - 1
                loss_data_row_indexs.append([i + 1, loss_val_count])

        print(loss_data_row_indexs)
        # 记录插补的次数，用来修正插入位置
        insert_sum = 0
        for loss_data_row_index in loss_data_row_indexs:
            if int(loss_data_row_index[1]) == 1:
                insert_data = [nan] * col_len
                # 在时间维度赋值其他维度均置None
                insert_data[0] = (datetime.datetime.strptime(dataset_list[loss_data_row_index[0]-1+insert_sum][0], '%Y-%m-%d %H:%M:%S') + datetime.timedelta(
                    seconds=most_vals_gap * 3600)).strftime('%Y-%m-%d %H:%M:%S')
                dataset_list.insert(loss_data_row_index[0]+insert_sum, insert_data)
                insert_sum +=1
            else:
                for loss_amount in range(1,int(loss_data_row_index[1])+1):
                    insert_data = [nan] * col_len
                    # 在时间维度赋值其他维度均置None
                    insert_data[0] = (datetime.datetime.strptime(dataset_list[loss_data_row_index[0]-1+insert_sum][0], '%Y-%m-%d %H:%M:%S') + datetime.timedelta(
                        seconds=most_vals_gap * 3600)).strftime('%Y-%m-%d %H:%M:%S')
                    dataset_list.insert(loss_data_row_index[0]+insert_sum, insert_data)
                    insert_sum += 1

    # fill_missing_value_using_iterative(dataset=dataset)
    print('dataset_list', dataset_list)
    dataframe_dataset = pd.DataFrame(dataset_list)
    print(dataframe_dataset)
    return_data = fill_missing_value_using_iterative(dataframe_dataset)
    print(return_data)


if __name__ == '__main__':
    generate_missing_row_using_sequence_time()