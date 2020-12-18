"""
**内部版本号**：*0.1.1.pro-beta*

**目前状态**：*热修正*

**模块说明**：*程序国际化部分，负责文本的翻译，目前不包括QT部分的文本*
"""

import configparser

LOCAL_LANGUAGE = 'zh-ch'  # TODO(长期) 添加自定义本地语言功能


class GetTranslation:  # TODO(长期) 文件和键值不存在错误
    """
    *类参数*

    **module_name -> str** 调用此类的模块名
    **translation_name -> str** 翻译的键值

    *类属性*

    **translation -> str** 翻译文本

    """
    def __init__(self, module_name, translation_name):
        self.localization = f'Localization/{LOCAL_LANGUAGE}.ini'
        self.translation = self._get_translation(module_name, translation_name)

    def _get_translation(self, module_name, translation_name):
        translation_read = open(self.localization, encoding='utf8')
        config_parser = configparser.ConfigParser()
        config_parser.read_file(translation_read)
        return config_parser.get(module_name, translation_name)


if __name__ == '__main__':
    pass
