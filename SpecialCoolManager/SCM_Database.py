"""
内部版本号：0.1.0.alpha
目前状态：发布测试版，进行功能更新和bug修复

模块说明：负责软件数据库相关操作
"""

import os
import sqlite3
import SCM_Exception


class SQLDBMethod:
    """  # TODO(急迫) 统一文档字符串格式
    **类属性** \n
    *database_estorage -> str* 数据库储存文件夹地址，默认为相对文件夹 /Database \n
    *db_name -> str* 数据库文件名称，不带.db后缀 \n
    \n
    **类方法** \n
    *get_con()* 返回指定数据库的connect类 \n
    """

    def __init__(self):
        self.database_estorage = r'Database'
        self.db_name = ''

    def get_con(self):
        if not os.path.exists(self.database_estorage):
            os.mkdir(self.database_estorage)
        if self.db_name == '':
            connect_back = None  # 此条件分支会引发AttributeError异常，请注意捕获
        else:
            connect_back = sqlite3.connect(f'{self.database_estorage}/{self.db_name}.db')
        return connect_back


class SQLTableMethod:  # TODO(长期) 此类可能会触发AttributeError异常
    """
    类的初始化\n
    get_con -> sqlite.connect 传入指定数据库的connect类\n
    \n
    类属性\n
    table_name -> str 指定的表名\n
    \n
    类方法\n
    con_close() 数据库con的提交和断开连接功能，注意最后必须调用\n
    table_check() 检查指定的表名是否存在\n
    table_create(table_format -> str) 创建指定table_format格式的表\n
    table_create() 删除指定的表\n
    \n
    类异常\n
    SCM_Exception.TableExist\n
    SCM_Exception.TableInexist\n
    """

    def __init__(self, get_con):
        self._con = get_con
        self._cur = get_con.cursor()
        self.table_name = ''

    def con_close(self):
        self._con.commit()
        self._con.close()
        return

    def table_check(self):
        self._cur.execute("SELECT tbl_name FROM sqlite_master WHERE type = 'table'")
        table_check = False
        for i in self._cur.fetchall():
            if (self.table_name in i[0]) and (self.table_name != ''):
                table_check = True
        return table_check

    def table_create(self, table_format):
        table_check = self.table_check()
        if not table_check:
            self._cur.execute(f"CREATE TABLE {self.table_name} ({table_format})")
        else:
            raise SCM_Exception.TableExist
        return

    def table_drop(self):
        table_check = self.table_check()
        if not table_check:
            raise SCM_Exception.TableInexist
        else:
            self._cur.execute(f"DROP TABLE {self.table_name}")
        return

    def _table_backup(self):  # TODO(长期) 添加数据库备份功能
        pass


class SQLColumnMethod:
    """
    类的初始化\n
    get_con -> sqlite.connect 传入指定数据库的connect类\n
    \n
    类属性\n
    table_name -> str 指定的表名\n
    column_name -> tup 指定的列名，传入元组\n
    sql_where -> str 不带WHERE的SQL的where语句\n
    \n
    类方法\n
    column_insert(column_value -> tup) 在指定列插入传入的column_value数据\n
    column_update(column_value -> tup) 更新指定列的数据为传入的column_value，WHERE语句强制必须添加\n
    column_delete() 删除WHERE符合条件的表，WHERE语句强制必须添加\n
    column_value_get_one(use_where=False) 返回单个搜索结果，use_where用于控制WHERE语句的启用，没有为空列表\n
    column_value_get_many(size -> int, use_where=False) 返回size个搜索结果，use_where用于控制WHERE语句的启用\n
    column_value_get_all(use_where=False) 返回所有的搜索结果，use_where用于控制WHERE语句的启用\n
    \n
    类异常\n
    SCM_Exception.ColumnInsertMore
    SCM_Exception.ColumnInsertLess
    """

    def __init__(self, get_con):
        self._con = get_con
        self._cur = get_con.cursor()
        self.table_name = ''
        self.column_name = ()
        self.sql_where = ''

    def _table_check(self):
        """确保表名存在，否则抛出异常"""
        table_check = SQLTableMethod(self._con)
        table_check.table_name = self.table_name
        table_check_bool = table_check.table_check()
        if not table_check_bool:  # 表名必须存在
            raise SCM_Exception.ColumnTableError
        else:
            return True

    def _column_name_getin(self):
        """将以列表格式传入的列名转换为合法的SQL语句"""
        if not self.column_name:  # 缺省时默认为所有的列
            column_name_sqlin = '*'
        else:
            column_name_sqlin_1 = ''
            for i in self.column_name:
                column_name_sqlin_1 += i
                column_name_sqlin_1 += ', '
            column_name_sqlin = f'({column_name_sqlin_1[:-2]})'
        return column_name_sqlin

    def column_insert(self, column_value):
        self._table_check()
        column_name_len = len(self.column_name)
        column_value_len = len(column_value)
        if column_name_len != column_value_len:
            if column_name_len < column_value_len:
                raise SCM_Exception.ColumnInsertMore
            elif column_name_len > column_value_len:
                raise SCM_Exception.ColumnInsertLess
        value_placeholder = f"({('?, ' * len(column_value))[:-2]})"
        column_name = self._column_name_getin()
        if column_name == '*':
            column_name = ''
        self._cur.execute(f"INSERT INTO {self.table_name} {column_name} VALUES {value_placeholder}", column_value)
        return

    def _column_select(self, use_where=False):
        """返回正在执行搜索的SQL搜索语句"""
        if use_where and self.sql_where != '':
            sql_where = f' WHERE {self.sql_where}'  # 保留WHERE前的空格
        else:
            sql_where = ''
        return self._cur.execute(f"SELECT {self._column_name_getin()[1: -1]} FROM {self.table_name} {sql_where}")

    def column_update(self, column_value):
        column_name_in = ''
        for i in self.column_name:
            column_name_in += f"{i}=?, "
        column_name_len = len(self.column_name)
        column_value_len = len(column_value)
        if column_name_len != column_value_len:
            if column_name_len < column_value_len:
                raise SCM_Exception.ColumnInsertMore
            elif column_name_len > column_value_len:
                raise SCM_Exception.ColumnInsertLess
        if self.sql_where == '':
            raise SCM_Exception.ColumnUpdateWhereNull
        self._cur.execute(f"UPDATE {self.table_name} SET {column_name_in[:-2]} WHERE {self.sql_where}", column_value)
        return

    def column_delete(self):
        if self.sql_where == '':
            raise SCM_Exception.ColumnDeleteNull
        self._cur.execute(f"DELETE FROM {self.table_name} WHERE {self.sql_where}")
        return

    def column_value_get_one(self, use_where=False):
        value_get = self._column_select(use_where).fetchone()
        if not value_get:
            value_get = []
        return value_get

    def column_value_get_many(self, size, use_where=False):
        value_get = self._column_select(use_where).fetchmany(size)
        return value_get

    def column_value_get_all(self, use_where=False):
        value_get = self._column_select(use_where).fetchall()
        return value_get


class SQLWhereMake:  # TODO(长期) 完成where语句编写
    pass


if __name__ == '__main__':
    test_1 = SQLDBMethod()
    test_1.database_estorage = r'D:\Programs\Programs\Working\Special_Cool_Manager\test'
    test_1.db_name = 'database'
    test_con = test_1.get_con()
    print(type(test_con))

    test_2 = SQLColumnMethod(test_con)
    test_2.table_name = 'test_1'
    # test_2.sql_where = "name_1 = 2"
    test_2.column_name = ('name_2', 'name_1')
    print(test_2.column_value_get_all(use_where=True))

    SQLTableMethod(test_con).con_close()
