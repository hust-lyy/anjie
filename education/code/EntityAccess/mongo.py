import pymongo
import json
import configparser
import os
import bson
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='Dao.log',
                    filemode='a')


class Dao(object):

    def __init__(self, collection):
        try:
            self.__conf = configparser.ConfigParser()

            # path = os.path.join(os.path.split(os.getcwd())[0], 'config.conf')            
            path = os.path.join(os.getcwd(), 'config.conf')  # 启动APP.py使用这个
            logging.debug(path)
            self.__conf.read(path)
            self.__client = pymongo.MongoClient(self.__conf.get('mongo', 'host'),
                                                int(self.__conf.get('mongo', 'port')))
        except Exception as e:
            logging.error(e)
        self.__db = self.__client[self.__conf.get('mongo', 'database')]
        self.__collection = self.__db[collection]
    # insert()方法  插入数据
    # 参数 data:添加的数据(list类型)  [{},{}]
    # 返回添加后数据在mongo的ObjectID
    #

    def insert(self, data):
        try:
            if len(data) > 1:
                return self.__collection.insert_many(data).inserted_ids
            else:
                return str(self.__collection.insert_one(data[0]).inserted_id)
        except Exception as e:
            logging.error(e)
    #
    # delect()删除数据
    # 参数require 删除数据的条件(dict类型){}
    # 参数isAll是否将符合条件的全部删除(bool类型)Ture is ALL , False is Only one
    # 返回删除的数量

    #
    def delect(self, require, isAll=False):

        try:
            if isAll:
                return self.__collection.delete_many(require).deleted_count
            else:
                return self.__collection.delete_one(require).deleted_count
        except Exception as e:
            logging.error(e)
    # update()更新数据
    # 参数require为要更新的检索条件 不得为空(dict类型){}
    # 参数data要更新的数据 不得为空(dict类型){}
    # 参数isAll是否将符合条件的全部更新(bool类型)默认为False   True 为全部更新 ,False为只更新第一个被检索到的
    # 返回更新的数量
    #

    def update(self, require, data, isAll=False):
        try:
            if isAll:
                return self.__collection.update_many(require, {'$set': data}).matched_count
            else:
                return self.__collection.update_one(require, {'$set': data}).matched_count
        except Exception as e:
            logging.error(e)
    # replace()替换文档
    # 参数require为要替换的文档的检索条件  不得为空(dict类型){}
    # 参数data要更新的文档 不得为空(dict类型){}
    # 返回替换文档的数量
    # 注意条件如果不唯一则符合条件的所有文档均被替换

    def replace(self, require, data):
        try:
            return self.__collection.replace_one(require, data).matched_count
        except Exception as e:
            logging.error(e)
    # select()查询数据
    # 参数require为查询条件 不得为空 (dict类型){}
    # 参数showkey为显示的字段名 默认为全显示(dict类型){}
    # 参数count为显示的条数 默认为全显示 整数型
    # 返回cursor(供子函数count()以及data()使用)
    #

    # def select(self, require, showkey=None, count=0):
    #     try:
    #         result=[]
    #         if count > 0:
    #             self.__cursor = self.__collection.find(require, projection=showkey, limit=count)
    #             return self
    #             # for dic in self.__cursor:
    #             #     result.append(dic)
    #             # return result
    #         else:
    #             self.__cursor = self.__collection.find(require, projection=showkey)
    #             return self
    #             # for dic in self.__cursor:
    #             #     result.append(dic)
    #             # return result
    #     except Exception as e:
    #         logging.error(e)
    def select(self, require, showkey=None, start=0, count=0):
        try:
            result = []
            if count > 0 and start > 0:
                self.__cursor = self.__collection.find(
                    require, projection=showkey).skip(start).limit(count)
                return self
                # for dic in self.__cursor:
                #     result.append(dic)
                # return result
            else:
                self.__cursor = self.__collection.find(require, projection=showkey)
                return self
                # for dic in self.__cursor:
                #     result.append(dic)
                # return result
        except Exception as e:
            logging.error(e)

    @property  # 将函数转换为属性
    def count(self):
        return self.__cursor.count()

    def data(self):
        result = []
        for dic in self.__cursor:
            result.append(dic)
        return result

    def close(self):
        return self.__client.close()

    # def count(self,cursor):
    #     return self.__cursor.count()
    # def data(self):
    #     return self.select
    # class select(Dao):
    #     def __init__(self)
#     try:
#         conf=configparser.ConfigParser()
#         path=os.path.join(os.path.split(os.getcwd())[0],'config.conf')
#         conf.read(path)
#         client = pymongo.MongoClient(conf.get('mongo','host'), int(conf.get('mongo','port')))
#         db = client[conf.get('mongo','database')]
#         collection = db.Banners
#         print(collection.find())
#         aaa=list(collection.find())
#         print(aaa[0]['name'])
#     except Exception as e:
#         print(e,'error')
#ccc = Dao('aaa')
# print(video=Dao('Videos'))
# print(ccc.insert([{'name':'111','age':23},{'name':'222','age':25}]))
# #[ObjectId('5998104bc3666e423dcde52b'), ObjectId('5998104bc3666e423dcde52c')]
# print(ccc.delect({'name':'111'},True))
# print(ccc.update({'name':'222'},{'age':28,'bbb':[{'ccc':'dfffdd'}]}))
# print(ccc.select({'name':'222'},{'name':True,'_id':False}).count)
# print(ccc.select({},{'name':True}).data())
# print(ccc.count())
# for banners in collection.find():
#     # banner_json=json.dumps(dict(banners))
#
#     print(dict(banners))
# data={'_id':bson.ObjectId('5992d748bd1aa70c7553f814'),'_id':bson.ObjectId('59953bf2c3666e37d317ca04')}
# print(ccc.delect(data,True))
