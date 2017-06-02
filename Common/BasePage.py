# -*-coding:utf-8-*-
import os
import sys
import time

from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.expected_conditions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait

sys.setdefaultencoding('utf-8')
import xlrd.sheet
import os.path
from configparser import ConfigParser

PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))


class AppAction(object):
    '''封装公共方法'''
    driver = None

    # 重写元素定位方法
    def find_element(self, loc):

        try:
            WebDriverWait(self.driver, 30, 0.2).until(expected_conditions.presence_of_element_located(loc))
            return self.driver.find_element(*loc)
        except(NoSuchElementException, KeyError, ValueError, Exception) as e:
            print(u'BasePage页面查找元素失败:{}'.format(str(e)))
            print(u'页面未找到元素:%s，如果要获取toast，请开启Uiautomator2' % loc)
            raise str(e)

    def find_elements(self, loc):
        try:
            if len(self.driver.find_elements(*loc)):
                return self.driver.find_elements(*loc)
        except(NoSuchElementException, KeyError, ValueError, Exception) as e:
            print(u'页面未找到元素:%s' % (e.args[0]))
            raise e

    def find_elements_i(self, index, loc):
        return self.find_elements(loc)[index]

    # 切换webview页面
    def switch_to_webview(self):
        contexts = self.driver.contexts

        for i in contexts:
            if 'WEBVIEW' in i.upper():
                self.driver.switch_to.context(i)
            else:
                print(u'没有webview出现！')

    # 切换回NATIVE_APP
    def switch_to_app(self):

        self.driver.switch_to.context('NATIVE_APP')

    # 重写send_keys方法
    def send_key(self, loc, values):
        ele = self.find_element(loc)
        # ele.set_text(values)
        try:
            ele.clear()
            ele.set_text(values)
        except:
            try:
                ele.set_value(values)
            except Exception as e:
                print
                u'输入内容异常：{}'.format(str(e))
                raise e

    # 获取屏幕大小
    def getWindowsSize(self, x):
        return int(self.driver.get_window_size()[x])

    # 获取元素的坐标和大小
    def getElementSize(self, loc):
        '''
        :param element:目标元素 
        :return: 元素左上角坐标和大小
        '''
        location = self.find_element(loc).location
        size = self.find_element(loc).size
        return location, size

    # 重写滑动页面方法,上下移动均为半个屏，左右移动80%
    def swipePage(self, direction, duration=500):
        width = self.getWindowsSize('width')
        height = self.getWindowsSize('height')
        if direction.upper() == 'UP':
            self.driver.swipe(width / 2, height * 9 / 10, width / 2, height * 2 / 5, duration)
        elif direction.upper() == 'DOWN':
            self.driver.swipe(width / 2, height * 2 / 5, width / 2, height * 9 / 10, duration)
        elif direction.upper() == 'LEFT':
            self.driver.swipe(width * 9 / 10, height / 2, width / 10, height / 2, duration)
        elif direction.upper() == 'RIGHT':
            self.driver.swipe(width / 10, height / 2, width * 9 / 10, height / 2, duration)
        else:
            print
            u'滑动页面操作指令有误！'

    # 滑动元素
    def swipeElement(self, direction, loc, duration=500):
        '''
        :param direction: 滑动方向
        :param loc: 定位方式
        :return: 无
        '''
        time.sleep(.5)
        location, size = self.getElementSize(loc)
        x = int(location.get('x'))
        y = int(location.get('y'))
        width = size.get('width')
        height = size.get('height')
        start_x = x + int(width) / 10
        start_y = y + int(height) / 10
        end_x = int(x) + int(width) * 9 / 10
        end_y = int(y) + int(height) * 9 / 10
        if direction.upper() == 'LEFT':
            self.driver.swipe(end_x, y + height / 2, start_x, y + height / 2, duration)
        elif direction.upper() == 'RIGHT':
            self.driver.swipe(start_x, y + height / 2, end_x, y + height / 2, duration)
        elif direction.upper() == 'UP':
            self.driver.swipe(x + width / 2, end_y, x + width / 2, start_y, duration)
        elif direction.upper() == 'DOWN':
            self.driver.swipe(x + width / 2, start_y, x + width / 2, end_y, duration)
        elif type(direction) == int or type(direction) == float or str(direction).isdigit():
            direction = str(int(direction))
            x1, x2, x3 = x + width / 6, x + width / 2, x + width * 5 / 6
            y1, y2, y3 = y + height / 6, y + height / 2, y + height * 5 / 6
            dict_x = {1: x1, 2: x2, 3: x3}
            dict_y = {1: y1, 2: y2, 3: y3}
            dict_po = {1: [x1, y1], 2: [x2, y1], 3: [x3, y1], 4: [x1, y2], 5: [x2, y2], 6: [x3, y2], 7: [x1, y3],
                       8: [x2, y3], 9: [x3, y3]}
            str1 = 'TouchAction(self.driver).press(x={0},y={1}).wait(200)'.format(dict_po[int(direction[0])][0],
                                                                                  dict_po[int(direction[0])][1])
            num = 1
            for i in direction[1:]:
                ns = int(direction[num - 1])
                str1 += '.move_to(x={0},y={1}).wait(200)'.format(dict_po[int(i)][0] - dict_po[ns][0],
                                                                 dict_po[int(i)][1] - dict_po[ns][1])
                num += 1
            str1 += '.release().perform()'
            print
            str1
            eval(str1)
        else:
            print
            u'元素滑动方向有误！'

    # 重写点击方法
    def tap(self, positions, duration=250):
        list1 = []
        list2 = []
        s = 0
        positions = positions.strip(']').strip('[').strip()
        positions = positions.split(',')
        for i in positions:
            if i.isdigit() and s < 2:
                list1.append(int(i))
                s += 1
                if s == 2:
                    list2.append(tuple(list1))
                    list1 = []
                    s = 0
        self.driver.tap(list2, duration)

    # 元素拖动
    def dragAndDrop(self, loc1, loc2):
        '''
        :param loc1: 起始元素
        :param loc2: 目标元素
        :return: 无
        '''
        start = self.find_element(loc1)
        end = self.find_element(loc2)
        self.driver.drag_and_drop(start, end)

    # 缩小放大页面
    def p_z_page(self, how):
        '''
        :param x:操作中心点x坐标 
        :param y: 操作中心点y坐标
        :param how:放大还是缩小
        :return: 无
        '''
        width = self.getWindowsSize('width')
        height = self.getWindowsSize('height')
        x = width / 2
        y = height / 2
        if how.upper() == 'SMALLER':
            self.driver.pinch(x, y)
        elif how.upper() == 'LARGER':
            self.driver.zoom(x, y)
        else:
            print
            u'页面大小操作指令有误！'

    # 缩小放大元素
    def p_z_element(self, loc, how):
        '''
        :param loc: 缩小元素定位方式
        :param how: 放大还是缩小
        :return: 无
        '''
        element = self.find_element(loc)
        if how.upper() == 'SMALLER':
            self.driver.pinch(element)
        elif how.upper() == 'LARGER':
            self.driver.zoom(element)
        else:
            print
            u'元素大小操作指令有误！'

    # 摇晃
    def shake(self):
        self.driver.shake()

    # 设置手机网络状态
    def setNetWork(self, connectType):
        '''
        :param connectType:网络类型 
            Value (Alias)      | Data | Wifi | Airplane Mode
            -------------------------------------------------
            0 (None)           | 0    | 0    | 0
            1 (Airplane Mode)  | 0    | 0    | 1
            2 (Wifi only)      | 0    | 1    | 0
            4 (Data only)      | 1    | 0    | 0
            6 (All network on) | 1    | 1    | 0
        :return: 无
        '''

        self.driver.set_network_connection(connectType)
        time.sleep(3)
        type = self.driver.network_connection
        assert int(type) == int(connectType)

    # 定位系统
    def toggleLocation(self):

        self.driver.toggle_location_services()

    def setTable(self, filePath, sheetname):
        '''获取excel中的sheet:
        filePath:文件路径
        sheetname:sheet名
        '''
        sheet = xlrd.open_workbook(filePath)
        table = sheet.sheet_by_name(sheetname)
        return table

    # 读取excel表格，将每行数据yield
    def getSheetData(self, filePath, sheetname):
        '''
        :param filePath: 文件路径
        :param sheetname: sheet名
        :return: yield
        '''
        table = self.setTable(filePath, sheetname)
        for i in range(1, table.nrows):
            yield table.row_values(i)

    # 获取单元格数据
    def getCellData(self, filePath, sheetname, rowNum, colNum):
        '''
        :param sheetname: sheet名
        :param rowNum: 行顺序,从0开始
        :param colNum: 列顺序，从0开始
        :return: 单元格数据
        '''
        table = self.setTable(filePath, sheetname)
        cellData = table.cell_value(rowNum, colNum)
        return cellData

    # 从excel中获取元素的定位方式
    def locate(self, index, filepath="dataEngin\\testData.xls", sheetname="element"):
        '''
        :param index: 元素编号
        :param filePath: excel文件路径
        :param sheet: sheet名
        :return: ('id','com.baidu.yuedu:id/myyuedu_gridview')、('xpath','//android.widget.RelativeLayout[contains(@index,1)]/android.widget.EditText[1]')
        '''
        table = self.setTable(filepath, sheetname)
        for i in range(1, table.nrows):
            if index == table.row_values(i)[0]:
                a, b = table.row_values(i)[1:3]
                if str(b).endswith('.0') or str(b).endswith('.00'):  # 从Excel取整数时会被转换成浮点数，需要转换
                    b = str(b).split('.')[0]
                return [a, b]

    # 生成截图名称
    def savePngName(self, name, toe='normal'):
        '''
        :param nowFunc 当前运行的用例名
        :param name: 截图名称
        :param toe: normal表示正常截图，error表示对框架运行失败截图
        :return: 截图名称
        '''
        day = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        # nowFunc = inspect.stack()[3][-2][0][:-3].strip()  #用例名目录
        # dirs1 = 'result\\' + day + '\\images' + '\\' + nowFunc
        # dirs2 = 'result\\' + day + '\\errorImages' + '\\' + nowFunc
        # dirs3 = 'result\\' + day + '\\shotImg' + '\\' + nowFunc
        dirs1 = dirs2 = dirs3 = 'result\\' + day + '\\' + self.nowFunc
        timeNow = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time()))
        type = '.png'

        # 检查是否存在指定目录，若没有需要创建
        if toe == 'normal':
            if os.path.exists(dirs1):
                pngName = str(dirs1) + '\\' + timeNow + '_' + str(name).decode('utf-8') + type
                self.saveScreenShot(pngName)
            else:
                print
                u'创建截图存储目录！'
                os.makedirs(dirs1)
                print
                u'创建目录成功！'
                pngName = str(dirs1) + '\\' + timeNow + '_' + str(name).decode('utf-8') + type
                self.saveScreenShot(pngName)
        elif toe == 'error':
            if os.path.exists(dirs2):
                pngName = str(dirs2) + '\\' + timeNow + '_' + str(name).decode('utf-8') + type
                self.saveScreenShot_error(pngName)
            else:
                print
                u'创建异常截图存储目录！'
                os.makedirs(dirs2)  # 创建多级目录，如果最后一级目录已存在，抛异常。所有贵哦城目录均被创建，如果不存在
                # os.mkdir(dirs2)  #创建单目录，如果路径为多层目录，只创建最后一级目录，如果最后一级以上的目录不存在则抛异常
                print
                u'创建目录成功！'
                pngName = str(dirs2) + '\\' + timeNow + '_' + str(name).decode('utf-8') + type
                self.saveScreenShot_error(pngName)
        elif toe == 'img':
            if os.path.exists(dirs3):
                pngName = str(dirs3) + '\\' + timeNow + '_' + str(name).decode('utf-8') + type
                self.saveScreenShot_img(pngName)
            else:
                print
                u'创建手动截图存储目录！'
                os.makedirs(dirs3)
                print
                u'创建目录成功！'
                pngName = str(dirs3) + '\\' + timeNow + '_' + str(name).decode('utf-8') + type
                self.saveScreenShot_img(pngName)
        else:
            print
            u'截图存储命名有误！'

    # 系统截图
    def saveScreenShot(self, pngName):
        '''
        :param name: 截图名称
        :return: True or False
        '''
        try:
            saveName = pngName
            self.driver.get_screenshot_as_file(saveName)
            print
            '***' + os.path.dirname(saveName) + '****'
        except Exception as e:
            print
            u'截图失败:{}'.format(str(e))
            raise e

    # 对脚本运行错误进行截图
    def saveScreenShot_error(self, pngName):
        '''
        :param name: 截图名称
        :return: True or False
        '''
        try:
            # self.driver.get_screenshot_as_file(self.savePngName(name,'error'))
            saveName = pngName
            self.driver.get_screenshot_as_file(saveName)
            print
            '***' + os.path.dirname(saveName) + '****'
        except Exception as e:
            print
            u'代码异常截图失败:{}'.format(str(e))
            raise e

    # 手动截图
    def saveScreenShot_img(self, pngName):
        '''
        :param name: 截图名称
        :return: True or False
        '''
        try:
            saveName = pngName
            self.driver.get_screenshot_as_file(saveName)
            print
            '***' + os.path.dirname(saveName) + '****'
        except Exception as e:
            print
            u'手动截图失败:{}'.format(str(e))
            raise e

    # 配置desired_capabilities
    def set_desCaps(self, nowFunc, toast, platformName, platformVersion, deviceName, app, appPackage, appActivity, udid,
                    unicodeKeyboard=True, resetKeyboard=True):
        '''
        :param toast: 是否获取toast
        :param platformName: 要测试的手机系统
        :param platformVersion: 手机操作系统版本
        :param deviceName: 使用手机类型或模拟器类型
        :param app: 待安装的app路径
        :param appPackage: 要运行的Android应用包名
        :param appActivity: 想要从应用包中启动的Android Activity名称
        :param unicodeKeyboard: 使用Unicode输入法，默认False
        :param resetKeyboard: 在设定了UnicodeKeyboard关键字的Unicode测试结束后，重置输入法原有状态，默认False
        :param udid: 设备标识符
        :return: desired_caps
        '''
        self.nowFunc = nowFunc
        desired_caps = {}
        desired_caps['platformName'] = platformName
        desired_caps['platformVersion'] = platformVersion
        desired_caps['deviceName'] = deviceName
        desired_caps['unicodeKeyboard'] = unicodeKeyboard
        desired_caps['resetKeyboard'] = resetKeyboard
        desired_caps['app'] = PATH(app)
        desired_caps['udid'] = udid
        desired_caps['appPackage'] = appPackage
        desired_caps['appActivity'] = appActivity
        desired_caps['newCommandTimeout'] = 180
        # desired_caps['appWaitActivity'] = appPackage
        if toast == 'Y':
            print
            u'是否获取toast：', toast
            desired_caps['automationName'] = 'Uiautomator2'
        else:
            print
            u'是否获取toast：', toast
        desired_caps['sessionOverride'] = True
        desired_caps['noSign'] = True  # 不进行重签名
        return desired_caps

    def getDesCap(self, tarApp):
        '''获取desired_caps配置'''
        self.tarApp = tarApp
        platformName = self.getIniData('DesiredCaps', 'platformName')
        platformVersion = self.getIniData('DesiredCaps', 'platformVersion')
        deviceName = self.getIniData('DesiredCaps', 'deviceName')
        app = self.getIniData(self.tarApp, 'app')
        appPackage = self.getIniData(self.tarApp, 'appPackage')
        appActivity = self.getIniData(self.tarApp, 'appActivity')
        unicodeKeyboard = self.getIniData('DesiredCaps', 'unicodeKeyboard')
        resetKeyboard = self.getIniData('DesiredCaps', 'resetKeyboard')
        udid = self.getIniData('DesiredCaps', 'udid')
        if unicodeKeyboard.upper() == 'TRUE':
            unicodeKeyboard = True
        else:
            unicodeKeyboard = False
        if resetKeyboard.upper() == 'TRUE':
            resetKeyboard = True
        else:
            resetKeyboard = False
        desired_caps = [platformName, platformVersion, deviceName, app, appPackage, appActivity, udid, unicodeKeyboard,
                        resetKeyboard]
        return desired_caps

    # app安装
    def install_app(self):
        # packages = self.getIniData('DesiredCaps', 'appPackage')
        packages = self.getDesCap(self.tarApp)[4]
        app = self.getDesCap(self.tarApp)[3]
        if self.driver.is_app_installed(packages):
            print
            u'app已安装，进行重新安装！'
        elif not self.driver.is_app_installed(packages):
            print
            u'app未安装，将进行安装！'
            i = 1
            while i < 4:
                print
                u'尝试第 %s 次安装！' % i
                # self.driver.install_app(app)
                if os.system('adb install {}'.format(self.getDesCap(self.tarApp)[3])) == 0:
                    WebDriverWait(self.driver, 10).until(lambda driver: driver.is_app_installed(packages))
                if self.driver.is_app_installed(self.getDesCap(self.tarApp)[4]):
                    print
                    u'安装成功！'
                    break
                else:
                    i += 1
                    continue
            else:
                print
                u'安装失败！'

    # 卸载app
    def uninstall_app(self):
        if self.driver.is_app_installed(self.getDesCap(self.tarApp)[4]):
            self.driver.remove_app(self.getDesCap(self.tarApp)[4])
            i = 1
            while i < 4:
                if not self.driver.is_app_installed(self.getDesCap(self.tarApp)[4]):
                    print
                    u'卸载完成！'
                    break
                else:
                    print
                    u'第 %s 次卸载失败！将重新卸载！' % i
                    i += 1
                    continue
            else:
                print
                u'卸载失败！'

    def getIniData(self, section, option, file='config\\data.ini'):
        '''
        读取ini配置数据
        :param file: 文件路径
        :param section: ini配置文件节点
        :param option: ini配置文件节点下的属性
        :return: 数据
        '''
        cf = ConfigParser()
        cf.read(file)
        options = cf.get(section, option)
        return options

    def rootTime(self, times):
        '''
        格式化时间日期
        :param time: 设置的日期值
        :return: 年，月，日，时，分，秒
        '''
        times = times.strip()  # 2017-05-02 23:30:54
        list1 = times.split(' ')
        y, m, d = list1[0].split('-')
        H, M, S = list1[1].split(':')
        # print int(y), int(m), int(d), int(H), int(M), int(S)
        return int(y), int(m), int(d), int(H), int(M), int(S)

    def flicks(self, x1, y1, x2, y2, n):
        '''
        滑动
        :param x1: 起始点坐标x
        :param y1: 起始点坐标y
        :param x2: 终点坐标x
        :param y2: 终点坐标y
        :return: 无
        '''
        i = 0
        while i < n:
            self.driver.swipe(x1, y1, x2, y2, duration=200)
            i += 1
