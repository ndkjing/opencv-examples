from faker import Faker
import random
import numpy  as np

f = Faker(locale='zh_CN')
#  姓名
def chinese_name():
    # print(f.name())
    return f.name()


# 性别
def gender():
    gender_list = ['男', '女']
    return random.choice(gender_list)


# 年龄
def age():
    age_list = range(1, 100)
    return random.choice(age_list)


# 电话
def phone_number():
    return f.phone_number()


# 身份证号
def id_card():
    return f.ssn()

# 日期
def data_time():
    return f.date_time()

# email
def email():
    return f.email()

# 随机整数
def random_int():
    return f.random_int()

# 家庭住址
def home_address():
    return f.address()

# 正态分布
def generate_normal(mean=0,variance=1,nums=1000):
    """

    :param mean:正态分布均值
    :param variance: 方差
    :param nums: 数量
    :return: 返回numpy矩阵
    """
    x = np.random.normal(mean, variance, nums)
    return x

# 二项分布数据
def generate_binomial_distribution(success_p=0.5,nums=1000):
    """
    :param success_p: 实验100次成功概率
    :param nums: 生成数据数量
    :return: 一维numpy矩阵
    """
    x = np.random.binomial(100,success_p, size=nums)
    print(x.shape)
    return x

# 生成指定相关性系数的双变量数据
def generate_related_distribution(related=0.5,nums=1000):
    """

    :param related:相关性系数
    :param nums: 生成数据数量
    :return: 返回二维numpy矩阵
    """
    # 均值为0, 标准差为1的多元正态分布
    X = np.random.multivariate_normal([0, 0], [[1, related], [related, 1]], nums)
    print(X.shape)
    return X


class PersonInfo:
    """
    生成个人信息数据
    """
    def __init__(self):
        print(chinese_name())
        print(gender())

    def generate_data(self, length=1):
        return_list = []
        for i in range(length):
            l = []
            l.append(chinese_name())
            l.append(gender())
            l.append(age())
            l.append(id_card())
            l.append(email())
            l.append(home_address())
            return_list.append(l)
        return return_list


class WideTable:
    """
    指定宽表数据格式生成数据
    """
    # 日期   站点名称   站点id   河道名称 河道id  经纬度   氨氮  总磷 溶解氧   高锰酸钾  高锰酸盐   水温  降雨   天气
    def __init__(self):
        pass

    def generate_data(self,length=1):
        return_list = []
        for i in range(length):
            l = []
            l.append(data_time())
            l.append(chinese_name())
            l.append(random_int())
            l.append(random_int())
            l.append(random_int())
            l.append(random_int())
            l.append(random_int())
            return_list.append(l)
        return return_list

class DistributionData:
    """
    指定数据分布规律分布
    """
    def __init__(self):
        pass

    def generate_data(self,length=1):
        pass


class GenerateDataTemplate:
    """
    自定义表结构数据
    """
    def __init__(self):
        pass

    def generate_data(self,length=1):
        pass



if __name__ == '__main__':
    # a = PersonInfo()
    # print(f.profile())
    # print(home_address())
    # generate_related_distribution()
    print(f.date_time())