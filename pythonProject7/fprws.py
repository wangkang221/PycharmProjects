import pytest
import logging
# module一个模块只会执行一次，最开头和最结尾调用
def setup_module():
    print('每个模块执行一次 开始')
def teardown_module():
    print('每个模块执行一次 结束')

# function 每个用例执行一次，不会对类中的用例生效
def setup_function():
    print("每个类外用例前执行")
def teardown_function():
    print("每个类外用例后执行")

if __name__ == '__main__':
    pytest.main()
