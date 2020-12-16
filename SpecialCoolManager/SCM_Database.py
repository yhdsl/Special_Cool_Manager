"""
内部版本号：0.1.0.pro-alpha
目前状态：工作中

模块说明：负责软件数据库相关操作
"""

import os
import sqlite3
import SCM_Exception


class SQLDBMethod:
    """
    类属性
    database_estorage 数据库储存文件夹地址
    db_name 数据库名称，不带.db后缀

    类方法
    get_con() 返回数据库的connect类
    """

    def __init__(self):
        self.database_estorage = r'Database'
        self.db_name = ''

    def get_con(self):
        if not os.path.exists(self.database_estorage):
            os.mkdir(self.database_estorage)
        if self.db_name == '':
            connect_back = None  # 此分支会引发方法不存在的异常，注意处理
        else:
            connect_back = sqlite3.connect(f'{self.database_estorage}/{self.db_name}.db')
        return connect_back


class SQLTableMethod:  # TODO(长期) 此类可能会触发方法不存在的异常
    """
    类属性
    table_name 指定的表名

    类方法
    con_close() 数据库con的提交和断开连接功能
    table_check() 检查表名是否存在
    table_create(table_format) 创建指定table_format格式的表
    table_create() 删除指定的表

    类异常
    SCM_Exception.TableExist
    SCM_Exception.TableInexist
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

    def _table_backup(self):  # TODO(长期) 完善数据库备份功能
        pass


class SQLColumnMethod:
    """
    pass
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
        if not table_check_bool:
            raise SCM_Exception.ColumnTableError
        else:
            return True

    def _column_name_getin(self):
        """将以列表格式传入的列名转换为SQL语句"""
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
        value_placeholder = f"({('?, ' * len(column_value))[:-2]})"
        column_name = self._column_name_getin()
        if column_name == '*':
            column_name = ''
        self._cur.execute(f"INSERT INTO {self.table_name} {column_name} VALUES {value_placeholder}", column_value)
        return

    def _column_select(self, use_where=False):
        """返回执行搜索的SQL语句"""
        if use_where:
            sql_where = f' WHERE {self.sql_where}'
        else:
            sql_where = ''
        return self._cur.execute(f"SELECT {self._column_name_getin()[1: -1]} FROM {self.table_name} {sql_where}")

    def column_update(self, column_value):
        column_name_in = ''
        for i in self.column_name:
            column_name_in += f"{i}=?, "
        self._cur.execute(f"UPDATE {self.table_name} SET {column_name_in[:-2]} WHERE {self.sql_where}", column_value)
        return

    def column_delete(self):
        self._cur.execute(f"DELETE FROM {self.table_name} WHERE {self.sql_where}")
        return

    def column_value_get(self):
        pass


class SQLWhereMake:  # TODO(临时) 完成where语句编写
    pass


if __name__ == '__main__':
    test_1 = SQLDBMethod()
    test_1.database_estorage = r'D:\Programs\Programs\Working\Special_Cool_Manager\test'
    test_1.db_name = 'database'
    test_con = test_1.get_con()

    test_2 = SQLTableMethod(test_con)
    # test_2.table_name = 'test'
    # test_2.table_create('test_1 TEXT')

    test_3 = SQLColumnMethod(test_con)
    test_3.table_name = 'test'
    test_3.column_insert(('1234', ))

    test_2.con_close()
