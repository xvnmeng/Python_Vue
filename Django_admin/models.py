from django.db import models

# Create your models here.

# 用户表
class User(models.Model):
    id = models.AutoField(primary_key=True, serialize=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    # 用户状态
    status = models.CharField(max_length=5, default='1')
    # class Meta:
    #     unique_together = ("id", "username")



# 测试接口数据表
class Article(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    content = models.TextField()
    #deleted alive
    status = models.CharField(max_length=10)


class User2(models.Model):
    id = models.AutoField(primary_key=True, serialize=True)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    # 创建时间
    create_tiem = models.DateTimeField(auto_now_add=True)
    # 更新时间
    update_time = models.DateTimeField(auto_now=True)
    # 文本格式
    # body = models.TextField()                # 正文
    # 用户状态
    # status = models.IntegerField(max_length=5)




'''
1、models.AutoField　　自增列=int(11)
　 如果没有的话，默认会生成一个名称为id的列，如果要显示的定义一个自增列，必须把该列设置为主键(primary_key=True)
2、models.CharField　　字符串类型字段 必须加max_length参数
3、models.BooleanField　布尔类型字段=tinyint(1)  不能为空，Blank=True
4、models.ComaSeparatedIntegerField　　用逗号分割的数字类型=varchar 继承CharField，所以必须加max_lenght参数
5、models.DateField　　日期字段类型date
　 参数auto_now=True表示每次更新都会更新这个时间；参数auto_now_add表示只是第一次创建时添加，之后的更新不再改变
6、models.DateTimeField　　日期字段类型datetime  同DateField的参数
7、models.Decimal　　十进制小数类型=decimal
　 必须指定整数位max_digits和小数位decimal_places
8、models.EmailField　　字符串类型(正则表达式邮箱)=varchar  对字符串进行正则表达式验证
9、models.FloatField　　浮点类型=double
10、models.IntegerField　　整形
11、models.BigIntegerField　长整形
　　integer_field_ranges = {
　　　　'SmallIntegerField': (-32768, 32767),
　　　　'IntegerField': (-2147483648, 2147483647),
　　　　'BigIntegerField': (-9223372036854775808, 9223372036854775807),
　　　　'PositiveSmallIntegerField': (0, 32767),
　　　　'PositiveIntegerField': (0, 2147483647),
　　}
12、models.IPAddressField　　字符串类型(ip4正则表达式)
13、models.GenericIPAddressField　　字符串类型（ip4和ip6是可选的）
　　参数protocol可以是：both、ipv4、ipv6  验证时，会根据设置进行报错
14、models.NullBooleanField　　允许为空的布尔类型
15、models.PositiveIntegerFiel　　正Integer
16、models.PositiveSmallIntegerField　　正smallInteger
17、models.SlugField　　减号、下划线、字母、数字
18、models.SmallIntegerField　　数字
　　数据库中的字段有：tinyint、smallint、int、bigint
19、models.TextField　　字符串=longtext
20、models.TimeField　　时间 HH:MM[:ss[.uuuuuu]]
21、models.URLField　　字符串类型，地址正则表达式
22、models.BinaryField　二进制
23、models.ImageField   图片
24、models.FilePathField 文件
'''