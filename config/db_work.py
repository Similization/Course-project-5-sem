from config.db_context_manager import DBContextManager


def get_schema(dbconfig: dict, sql: str):
    with DBContextManager(dbconfig) as cursor:
        if cursor is None:
            raise ValueError("Курсор не создан")

        cursor.execute(sql)
        schema = [column[0] for column in cursor.description]
        result = cursor.fetchall()
    return result, schema


def get_result(dbconfig: dict, sql: str):
    with DBContextManager(dbconfig) as cursor:
        if cursor is None:
            raise ValueError("Курсор не создан")

        cursor.execute(sql)
        result = cursor.fetchall()
    return result


def execute(dbconfig: dict, sql: str):
    with DBContextManager(dbconfig) as cursor:
        if cursor is None:
            raise ValueError("Курсор не создан")

        cursor.execute(sql)
    return


def get_dict(dbconfig: dict, sql: str):
    with DBContextManager(dbconfig) as cursor:
        if cursor is None:
            raise ValueError("Курсор не создан")

        cursor.execute(sql)
        schema = [column[0] for column in cursor.description]
        result = []
        for row in cursor.fetchall():
            result.append(dict(zip(schema, row)))
    return result


def call_procedure(dbconfig: dict, proc_name: str, *args):
    with DBContextManager(dbconfig) as cursor:
        if cursor is None:
            raise ValueError("Курсор не создан")
        param_list = []
        for arg in args:
            param_list.append(arg)
        print("param_list=", param_list)
        res = cursor.callproc(proc_name, param_list)
    return res
