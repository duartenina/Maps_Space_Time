import numpy as np

data_folder = 'data/china/'
image_folder = 'images/china/'
provinces_file = data_folder + 'china_regions/gadm36_CHN_1'
colors_provinces = [
    'peachpuff', 'palegreen', 'plum', 'olivedrab', 'salmon'
]
provinces_info = {
    'Anhui':            ('', (0, 31.0), 2),
    'Beijing':          ('', (116.9, 40.4), -1),
    'Chongqing':        ('', (0, 29.0), -1),
    'Fujian':           ('', (117.5, 25.5), 2),
    'Gansu':            ('', ( 96.5, 41.3), 3),
    'Guangdong':        ('', (117.5, 23.2), 3),
    'Guangxi':          ('', (110.0, 24.5), 1),
    'Guizhou':          ('', (105.9, 27.7), 3),
    'Hainan':           ('', (0, 19), 0),
    'Hebei':            ('', (114.4, 41.0), 2),
    'Heilongjiang':     ('', (127.5, 48.0), 1),
    'Henan':            ('', (0, 33.5), 1),
    'Hubei':            ('', (0, 0), 0),
    'Hunan':            ('', (0, 0), 2),
    'Jiangsu':          ('', (122.0, 32.7), 1),
    'Jiangxi':          ('', (116.6, 27.3), 1),
    'Jilin':            ('', (126.0, 42.8), 2),
    'Liaoning':         ('', (122.4, 41.1), 1),
    'Nei Mongol':       ('', (118.0, 44.0), 0),
    'Ningxia Hui':      ('Ningxia\nHui', (0, 36.5), 1),
    'Qinghai':          ('', ( 95.0, 36.0), 2),
    'Shaanxi':          ('', (109.0, 36.0), 2),
    'Shandong':         ('', (120.0, 37.0), 3),
    'Shanghai':         ('', (123.3, 31.0), -1),
    'Shanxi':           ('', (112.2, 36.7), 3),
    'Sichuan':          ('', (102.0, 29.5), 0),
    'Tianjin':          ('', (118.8, 39.0), -1),
    'Xinjiang Uygur':   ('', ( 83.0, 36.5), 0),
    'Xizang':           ('', ( 85.0, 32.0), 1),
    'Yunnan':           ('', (102.0, 24.0), 2),
    'Zhejiang':         ('', (0, 28.0), 3),
}
provinces_skip_outline = [
    'Liaoning', 'Shandong', 'Zhejiang', 'Guangdong'
]
rivers_file = data_folder + 'china_basins/River_basin_num2'
river_color = ['royalblue'] + ['dodgerblue']*7 + ['darkviolet']
river_widths = [2.5] + [2]*7 + [3]
rivers_info = np.array([
    # Oceans
    ['Sea of\nJapan', '日本海',                     (129.7, 39.1), 1],
    ['Bohai\nSea', '渤海',                          (120.7, 38.5), 2],
    ['Korea\nBay', '',                              (124.0, 39.0), 2],
    ['Yellow\nSea', '黃海',                         (124.0, 36.3), 1],
    ['East\nChina\nSea', '東海',                    (125.0, 29.0), 0],
    ['Taiwan\nStrait', '臺灣海峽',                  (120.2, 25.2), 2],
    ['South China\nSea', '南海',                    (116.0, 18.3), 1],
    ['Gulf of\nTonkin', '北部灣',                   (107.5, 19.7), 2],
    # Rivers
    ['Amur\nHeiLong', '黑龙江',                     (132.0, 49.5), 1],
    ['Songhua', '松花江',                           (126.3, 46.7), 2],
    ['Mudan', '牡丹江',                             (131.0, 45.0), 2],
    ['Songhua', '松花江',                           (124.5, 44.7), 2],
    ['Nen', '嫩江',                                 (123.2, 48.0), 2],
    ['Yalu', '鸭绿江',                              (126.7, 40.9), 2],
    ['Liao', '辽河',                                (122.5, 42.9), 2],
    ['Luan', '滦河',                                (116.5, 42.4), 2],
    ['Hai', '海河',                                 (114.9, 39.8), 2],
    ['Hutuo', '滹沱河',                             (114.5, 38.7), 2],
    ['Wey', '衞河',                                 (114.5, 36.3), 2],
    ['Yellow\nHuang', '黄河',                       (105.1, 41.0), 1],
    ['Wei', '渭河',                                 (105.0, 34.3), 2],
    ['Fen', '汾河',                                 (112.1, 35.8), 2],
    ['Huai', '淮河',                                (113.0, 32.5), 2],
    ['Yangtze', '长江',                             ( 89.0, 34.0), 1],
    ['Gan', '赣江',                                 (114.3, 27.5), 2],
    ['Xiang', '湘江',                               (113.5, 26.4), 2],
    ['Yuan', '沅江',                                (111.6, 29.4), 2],
    ['Han', '汉江',                                 (110.5, 32.4), 2],
    ['Wu', '乌江',                                  (107.5, 28.3), 2],
    ['Jialing', '嘉陵江',                           (106.7, 32.0), 2],
    ['Min', '岷江',                                 (103.4, 32.0), 2],
    ['Yalong', '雅砻江',                            (100.3, 32.0), 2],
    ['Qiantang', '钱塘江',                          (120.5, 28.7), 2],
    ['Min', '闽江',                                 (118.5, 27.0), 2],
    ['Pearl\nZhu', '珠江',                          (114.0, 21.0), 1],
    ['Dong', '东江',                                (116.2, 24.0), 2],
    ['Bei', '北江',                                 (112.8, 24.5), 2],
    ['Xi', '西江',                                  (111.2, 22.8), 2],
    ['Yu', '鬱江',                                  (107.1, 23.1), 2],
    ['Liu', '柳江',                                 (108.7, 25.3), 2],
    ['Hongshui', '红水河',                          (105.2, 25.5), 2],
    ['Red\nYuan', '元江',                           (104.0, 22.0), 2],
    ['Black\nLixian', '李仙江',                     (102.6, 21.7), 2],
    ['Mekong\nLancang', '湄公河',                   (101.0, 21.0), 2],
    ['Salween\nNu', '怒江',                         ( 98.0, 23.5), 2],
    ['Indus\nSênggê Zangbo', '獅泉河',              ( 77.5, 33.5), 2],
    ['Brahmaputra\nYarlung Tsangpo', '雅鲁藏布江',  ( 87.0, 30.2), 2],
    ['Tarim', '塔里木盆地',                         ( 83.5, 40.6), 2],
    ['Yarkand', '葉爾羌河',                         ( 76.0, 38.5), 2],
    ['Khotan', '和闐河',                            ( 82.1, 38.5), 2],
    ['Yili', '伊犁河',                              ( 83.0, 43.7), 2],
    ['Irtysh', '额尔齐斯河',                        ( 87.0, 47.0), 2],
    ['Ruo Shui\nHei', '弱水',                       (100.5, 43.3), 2],
    ['Shule', '疏勒河 ',                            ( 97.0, 38.5), 2],
], dtype=object)
cities_file = data_folder + 'China_Cities_Towns/China_Cities_Towns'
cities_info = {
    '': ("", (0, 0), 2, (0, 0)),
    # Municipalities
    'bejing': (None, (0, 0), 0, (0, 0)),
    'tianjin': (None, (0, 0), 1, (0, 0)),
    'shanghai': (None, (0, 0), 1, (0, 0)),
    'chongqing': (None, (0, 0), 1, (0, 0)),
    # Heilongjiang
    'harbin': ('', (1, 0), 1, (0, 0)),
    # Jilin
    'changchung': ('', (-1, 0), 1, (0, 0)),
    'jilin': ('', (1, 0), 2, (0, 0)),
    # Liaoning
    'shenyang': ('Shenyang\nMukden', (-1, 0), 1, (0, 0)),
    'fushun': ('', (1, 0), 2, (0, 0)),
    # Nei Mongol
    'hohhot': ('', (0, 1), 1, (0, 0)),
    'baotou': ('', (-2.5, 1), 2, (0, 0)),
    'dongsheng': ('Ordos', (-1, 0), 2, (110, 40)),
    'pingdingbu': ('Shangdu', (-1, 0), 2, (0, 0)),
    # Hebei
    'shijiazhuang': ('', (3.5, -1), 1, (0, 0)),
    # Shandong
    'jinan': ('', (1, 0), 1, (0, 0)),
    'qingdao': ('', (1, 0), 2, (0, 0)),
    'weihai': ('', (0, 1), 2, (0, 0)),
    # Shanxi
    'taiyuan': ('', (-1, 0), 1, (0, 0)),
    'datong': ('Datong\nPingcheng', (-1, 0), 2, (113.5, 40)),
    # Ningxia
    'yinchuan': ('', (1, 0), 1, (0, 0)),
    # Gansu
    'lanzhou': ('', (0, -1), 1, (0, 0)),
    'zhangye': ('Zhangye\nGanzhou', (1, 0), 2, (0, 0)),
    'dunhuang': ('', (-1, 0), 2, (0, 0)),
    # Shaanxi
    'xian': ("Xi'an", (2.5, -1), 1, (0, 0)),
    'xianyang': ("Chang'an", (-2.5, 1), 2, (0, 0)),
    'hanzhong': ('', (0, -1), 2, (0, 0)),
    'yanan': ("Yan'an", (0, 1), 2, (0, 0)),
    # Henan
    'zhengzhou': ('', (5, -1), 1, (0, 0)),
    'kaifeng': ('', (1, 0), 2, (0, 0)),
    'luoyang': ('', (-3, -.5), 2, (112.5, 35.0)),
    # Anhui
    'hefei': ('', (-1, 0), 1, (0, 0)),
    # Jiangsu
    'nanjing': ('', (-5, 1), 1, (0, 0)),
    'xuzhou': ('Xuzhou\nPengcheng', (1, 0), 2, (0, 0)),
    'yangzhou': ('', (1, 0), 2, (0, 0)),
    # Hubei
    'wuhan': ('', (.5, -1), 1, (0, 0)),
    'xiangyang': ('', (1, 0), 2, (112.0, 32-0)),
    # Sichuan
    'chengdu': ('', (-1, 0), 1, (0, 0)),
    # Guizhou
    'guiyang': ('', (-5, -1), 1, (106, 26)),
    # Hunan
    'changsha': ('', (-1, 0), 1, (0, 0)),
    # Jiangxi
    'nanchang': ('', (0, -1), 1, (0, 0)),
    # Zhejiang
    'hangzhou': ('', (-3.5, -1.5), 1, (0, 0)),
    'ningbo': ('', (2.5, .9), 2, (0, 0)),
    # Fujian
    'fuzhou': ('', (1, 0), 1, (120, 26)),
    'quanzhou': ('', (1, 0), 2, (118.5, 25)),
    'xiamen': ("", (1, 0), 2, (0, 0)),
    # Yunnan
    'kunming': ('', (-1, 0), 1, (0, 0)),
    'dali': ('', (-1, 0), 2, (100, 25.5)),
    # Guangxi
    'nanning': ('', (0, -1), 1, (0, 0)),
    'guilin': ('', (0, 1), 2, (0, 0)),
    # Guangdong
    'guangzhou': ('', (1, 0), 1, (0, 0)),
    'hong kong': ('Hong Kong', (1, 0), 2, (0, 0)),
    'macau': ('', (-1, 0), 2, (0, 0)),
    # Hainan
    'haikou': ('', (0, -1), 1, (110, 20)),
    # Xinjiang
    'urumqi': ('', (1, 0), 1, (0, 0)),
    'hami': ('', (1, 0), 2, (0, 0)),
    'kashi': ('Kashgar', (1, 0), 2, (0, 0)),
    'hotan': ('Khotan', (1, 0), 2, (0, 0)),
    'turpan': ('Turfan', (1, 0), 2, (0, 0)),
    'kuqa': ('', (1, 0), 2, (0, 0)),
    '': ('', (0, 0), 2, (0, 0)),
    # Qinghai
    'xining': ('', (-1, 0), 1, (0, 0)),
    # Xizang
    'lhasa': ('', (0, 1), 1, (0, 0)),
}
city_filter_range = 100_000
cities_colors = {
    0: 'red',
    1: 'gold',
    2: 'white',
    3: 'cyan'
}
cities_sizes = {
    0: (6, 4),
    1: (5, 3),
    2: (3, 2),
    3: (3, 2),
}
text_bg_colors = {
    'province': ('palegreen', 'Hebei'),
    'municipality': ('pink', 'Beijing'),
    'water body': ('cyan', 'Han'),
    'city': ('khaki', "Xi'an")
}