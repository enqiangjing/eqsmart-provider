from eqsmart.components.scan_services import ScanServices
from eqsmart.components.read_module import ReadModule
from eqsmart.main.provider import Provider
from eqlink.main.register import LinkRegister
from threading import Thread
import sys

sys.path.append('../..')

'''配置文件加载器'''
read_conf_module = ReadModule('configuration')


class Register:
    """ 服务注册器 """

    def __init__(self, path):
        """
        注册中心连接工具初始化
        :param path: 配置文件路径
        """
        ''' 注册中心的配置信息 '''
        load_link_conf = read_conf_module.read('conf_center')
        self.link_conf = load_link_conf.LinkServerConf(path).read_server()

    def register(self):
        """
        Provider到注册中心的注册器
        :return: Provider 服务注册器
        """
        return LinkRegister(self.link_conf)


class Application:
    """ 应用启动器 """

    def __init__(self, path):
        """
        app初始化
        :param path: 配置文件路径
        """
        self.conf_path = path
        ''' Provider服务列表扫描 '''
        scan_services = ScanServices('../services')
        load_provider_conf = read_conf_module.read('conf_provider')
        self.services = scan_services.get_services()
        self.services_class = scan_services.get_services_class()
        self.provider_conf = load_provider_conf.ProviderServerConf(path).read_server()

    def __provider__(self):
        """ 提供服务的Provider启动并注册 """
        print(self.provider_conf)
        Provider(self.provider_conf, self.services, self.services_class).server_init(
            Register(self.conf_path).register().register_int)


def main():
    """ 启动服务 """
    Thread(target=Application('configuration/profiles/app.yaml').__provider__).start()


if __name__ == '__main__':
    main()
