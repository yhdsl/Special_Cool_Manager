"""
内部版本号：0.1.0.alpha
目前状态：工作中

模块说明：程序所有异常定义
"""
import SCM_Localization as Local

# SCM_Database - 数据库异常


class DBError(Exception):
    def __str__(self):
        return Local.GetTranslation('SCM_Database', 'DBError').translation


class TableExist(Exception):
    def __str__(self):
        return Local.GetTranslation('SCM_Database', 'TableExist').translation


class TableInexist(Exception):
    def __str__(self):
        return Local.GetTranslation('SCM_Database', 'TableInexist').translation
