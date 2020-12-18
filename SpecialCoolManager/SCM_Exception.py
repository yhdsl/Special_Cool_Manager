"""
**内部版本号**：*0.1.10.alpha*

**目前状态**：*随项目开发进度进行*

**模块说明**：*定义程序所有异常*
"""
import SCM_Localization as Local

# SCM_Database - 定义数据库异常


class DBError(Exception):
    def __str__(self):
        return Local.GetTranslation('SCM_Database', 'DBError').translation


class TableExist(Exception):
    def __str__(self):
        return Local.GetTranslation('SCM_Database', 'TableExist').translation


class TableInexist(Exception):
    def __str__(self):
        return Local.GetTranslation('SCM_Database', 'TableInexist').translation


class ColumnTableError(Exception):
    def __str__(self):
        return Local.GetTranslation('SCM_Database', 'ColumnTableError').translation


class ColumnInsertMore(Exception):
    def __str__(self):
        return Local.GetTranslation('SCM_Database', 'ColumnInsertMore').translation


class ColumnInsertLess(Exception):
    def __str__(self):
        return Local.GetTranslation('SCM_Database', 'ColumnInsertLess').translation


class ColumnUpdateMore(Exception):
    def __str__(self):
        return Local.GetTranslation('SCM_Database', 'ColumnUpdateMore').translation


class ColumnUpdateLess(Exception):
    def __str__(self):
        return Local.GetTranslation('SCM_Database', 'ColumnUpdateLess').translation


class ColumnUpdateWhereNull(Exception):
    def __str__(self):
        return Local.GetTranslation('SCM_Database', 'ColumnUpdateWhereNull').translation


class ColumnDeleteNull(Exception):
    def __str__(self):
        return Local.GetTranslation('SCM_Database', 'ColumnDeleteNull').translation
