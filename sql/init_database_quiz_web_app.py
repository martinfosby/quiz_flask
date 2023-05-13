from mysql.connector import connect, Error
import time


# warning this will delete database
inp = input('warning this will delete database are you sure? press y to continue: ')
if inp == 'y':
    try:
        with connect(
            host="localhost",
            user='root',
            password='test',
            database='quiz_web_app'
        ) as connection:
            with connection.cursor() as cursor:
                print('deleting database')
                cursor.execute(f"DROP DATABASE {connection.database}")
                time.sleep(1)
                connection.commit()
    except Error as error:
        print(error)
    except Exception as e:
        print(e)



    while True:
        try:
            with connect(
                host="localhost",
                user='root',
                password='test',
                database='quiz_web_app'
            ) as connection:
                print('schema exists')
                print('connection made with database:', connection.database)
                with connection.cursor() as cursor:
                    with open('sql/test_data.sql', 'r') as f:
                        for statement in f.read().split(';'):
                            statement = statement.replace('\n', '')
                            cursor.execute(statement)
                            time.sleep(0.1)
                        connection.commit()
                        print('successfully added test data')
                #     with open('sql/test_data.sql', 'r') as f:
                #         cursor.execute(f.read(), multi=True)
                #         cursor.fetchall()
                #     print('executed test data')
                # connection.commit()  # commit the changes made by the cursor

            break
        except Error as error:
            print(error)
            print('creating schema')
            with connect(
                host="localhost",
                user='root',
                password='test',
            ) as connection:
                with open('sql/quiz_web_app.sql', 'r') as f:
                    with connection.cursor() as cursor:
                        cursor.execute(f.read(), multi=True)
                        time.sleep(1)
                        cursor.fetchall()
        except Exception as e:
            print(e)
