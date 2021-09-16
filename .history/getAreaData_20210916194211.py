import requests
import json
import pandas as pd
import time

province_list = [
    '广东', '四川', '吉林', '宁夏', '福建', '云南', '上海', '北京', '山东', '湖北', '黑龙江', '江苏',
    '河南', '浙江', '河北', '湖南', '安徽', '新疆', '江西', '陕西', '重庆', '天津', '辽宁', '内蒙古',
    '广西', '山西', '甘肃', '海南', '贵州', '青海', '西藏'
]
city_dict = {
    '广东': [
        '广州', '潮州', '东莞', '佛山', '河源', '惠州', '江门', '揭阳', '茂名', '梅州', '清远', '汕头',
        '汕尾', '韶关', '深圳', '阳江', '湛江', '肇庆', '中山', '珠海', '境外输入'
    ],
    '四川': [
        '成都', '阿坝', '巴中', '达州', '德阳', '甘孜', '广安', '广元', '乐山', '凉山', '泸州', '南充',
        '眉山', '绵阳', '内江', '攀枝花', '遂宁', '雅安', '宜宾', '资阳', '自贡', '境外输入'
    ],
    '吉林':
    ['长春', '白城', '公主岭', '吉林', '辽源', '四平', '松原', '通化', '延边', '梅河口市', '境外输入'],
    '宁夏': ['银川', '固原', '石嘴山', '吴忠', '中卫', '宁东管委会', '境外输入'],
    '福建': ['福州', '龙岩', '南平', '宁德', '莆田', '泉州', '三明', '厦门', '漳州', '境外输入'],
    '云南': [
        '昆明', '保山市', '楚雄州', '大理', '德宏州', '迪庆州', '红河', '丽江市', '临沧', '怒江州', '普洱',
        '曲靖', '昭通市', '文山州', '西双版纳州', '玉溪', '境外输入'
    ],
    '上海': [
        '黄浦', '徐汇', '长宁', '静安', '普陀', '虹口', '杨浦', '闵行', '宝山', '嘉定', '浦东', '金山',
        '松江', '青浦', '奉贤', '崇明', '境外输入', '境外来沪', '外地来沪'
    ],
    '北京': [
        '东城', '西城', '朝阳', '丰台', '石景山', '海淀', '顺义', '通州', '大兴', '房山', '门头沟',
        '昌平', '密云', '怀柔', '延庆', '境外输入', '外地来京'
    ],
    '山东': [
        '济南', '滨州', '德州', '菏泽', '济宁', '聊城', '临沂', '青岛', '日照', '泰安', '威海', '潍坊',
        '烟台', '枣庄', '淄博', '境外输入'
    ],
    '湖北': [
        '武汉', '鄂州', '恩施州', '黄冈', '黄石', '荆门', '荆州', '潜江', '神农架', '十堰', '随州',
        '天门', '仙桃', '咸宁', '襄阳', '孝感', '宜昌', '境外输入'
    ],
    '黑龙江': [
        '哈尔滨', '大庆', '大兴安岭', '鹤岗', '黑河', '鸡西', '佳木斯', '牡丹江', '七台河', '齐齐哈尔',
        '双鸭山', '绥化', '伊春', '境外输入'
    ],
    '江苏': [
        '南京', '常州', '淮安', '连云港', '南通', '苏州', '宿迁', '泰州', '无锡', '徐州', '盐城',
        '扬州', '镇江', '境外输入'
    ],
    '河南': [
        '郑州', '安阳', '鹤壁', '焦作', '开封', '洛阳', '漯河', '南阳', '平顶山', '濮阳', '三门峡',
        '商丘', '新乡', '信阳', '许昌', '周口', '驻马店', '境外输入', '济源示范区'
    ],
    '浙江': [
        '杭州', '湖州', '嘉兴', '金华', '丽水', '宁波', '衢州', '绍兴', '台州', '温州', '舟山',
        '境外输入', '省十里丰监狱'
    ],
    '河北': [
        '石家庄', '保定', '沧州', '承德', '邯郸', '衡水', '廊坊', '秦皇岛', '唐山', '邢台', '张家口',
        '境外输入'
    ],
    '湖南': [
        '长沙', '常德', '郴州', '衡阳', '怀化', '娄底', '邵阳', '湘潭', '湘西自治州', '益阳', '永州',
        '岳阳', '张家界', '株洲', '境外输入'
    ],
    '安徽': [
        '合肥', '安庆', '蚌埠', '亳州', '池州', '滁州', '阜阳', '淮北', '黄山', '六安', '马鞍山',
        '宿州', '铜陵', '芜湖', '宣城', '淮南', '境外输入'
    ],
    '新疆': [
        '乌鲁木齐', '兵团第十二师', '兵团第九师', '兵团第四师', '阿克苏', '昌吉州', '喀什', '第八师石河子', '巴州',
        '第七师', '吐鲁番', '六师五家渠', '伊犁州'
    ],
    '江西': [
        '南昌', '抚州', '赣州', '吉安', '景德镇', '九江', '萍乡', '上饶', '新余', '宜春', '鹰潭',
        '境外输入', '赣江新区'
    ],
    '陕西': [
        '西安', '安康', '宝鸡', '汉中', '商洛', '铜川', '渭南', '咸阳', '延安', '榆林', '境外输入',
        '杨凌', '韩城'
    ],
    '重庆': [
        '渝中区', '万州区', '涪陵区', '大渡口区', '江北区', '沙坪坝区', '九龙坡区', '南岸区', '高新区',
        '綦江区', '大足区', '渝北区', '巴南区', '黔江区', '长寿区', '江津区', '合川区', '永川区', '璧山区',
        '铜梁区', '潼南区', '荣昌区', '开州区', '梁平区', '武隆区', '城口县', '丰都县', '垫江县', '忠县',
        '云阳县', '奉节县', '巫山县', '巫溪县', '石柱县', '秀山县', '酉阳县', '彭水县', '境外输入',
        '万盛经开区', '两江新区', '南川区'
    ],
    '天津': [
        '境外输入', '和平区', '河东区', '河西区', '南开区', '河北区', '红桥区', '滨海新区', '东丽区', '西青区',
        '津南区', '北辰区', '武清区', '宝坻区', '外地来津', '静海区', '蓟州区', '宁河区'
    ],
    '辽宁': [
        '沈阳', '境外输入', '鞍山', '本溪', '朝阳市', '大连', '丹东', '抚顺', '阜新', '葫芦岛', '锦州',
        '辽阳', '盘锦', '铁岭', '营口'
    ],
    '内蒙古': [
        '呼和浩特', '包头', '巴彦淖尔', '赤峰', '鄂尔多斯', '呼伦贝尔', '通辽', '乌海', '乌兰察布', '锡林郭勒',
        '兴安盟', '境外输入', '阿拉善盟'
    ],
    '广西': [
        '南宁', '百色', '北海', '防城港', '桂林', '贵港', '河池', '贺州', '来宾', '柳州', '钦州',
        '梧州', '玉林', '境外输入', '崇左'
    ],
    '山西':
    ['太原', '长治', '大同', '晋城', '晋中', '临汾', '吕梁', '朔州', '忻州', '阳泉', '运城', '境外输入'],
    '甘肃': [
        '兰州', '白银', '定西', '甘南州', '金昌', '临夏', '陇南', '平凉', '庆阳', '天水', '张掖',
        '境外输入'
    ],
    '海南': [
        '海口', '境外输入', '保亭', '昌江县', '儋州', '澄迈县', '东方', '定安县', '琼海', '琼中县', '乐东',
        '临高县', '陵水县', '三亚', '万宁', '文昌'
    ],
    '贵州': ['贵阳', '境外输入', '安顺', '毕节', '六盘水', '铜仁', '遵义', '黔西南州', '黔东南州', '黔南州'],
    '青海': ['西宁', '海北州'],
    '西藏': ['拉萨']
}
base_url = 'https://api.inews.qq.com/newsqa/v1/query/pubished/daily/list?'
headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
}
cols = [
    'province', 'city', 'y', 'date', 'confirm', 'dead', 'heal', 'suspect',
    'confirm_add'
]


def local_timestamp():
    return time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())


def writeRawData():
    csvDataFrame = pd.DataFrame(columns=cols)
    for province in province_list:
        # print(province)
        for city in city_dict[province]:
            # print(city)
            request_url = base_url + 'province=' + province + '&city=' + city
            print(request_url)
            req = requests.get(request_url, headers=headers)
            jsonData = req.text
            data = json.loads(jsonData)
            timeSeriesData = data['data']
            if timeSeriesData is None:
                size = csvDataFrame.index.size
                y = time.strftime("%Y", time.localtime())
                date = time.strftime("%m.%d", time.localtime())
                csvDataFrame.loc[size] = [
                    province, city, y,
                    str(date), '0', '', '', '', ''
                ]
                print(csvDataFrame.loc[size])
                continue
            # null 说明api有问题（命名错误）或者该地未发生疫情
            for i in timeSeriesData:
                size = csvDataFrame.index.size
                try:
                    y = i['y']
                except KeyError:
                    y = i['year']
                csvDataFrame.loc[size] = [
                    province, city, y,
                    str(i['date']), i['confirm'], i['dead'], i['heal'],
                    i['suspect'], i['confirm_add']
                ]

    hkmctw = ['香港', '澳门', '台湾']
    for province in hkmctw:
        request_url = base_url + 'province=' + province
        print(request_url)
        req = requests.get(request_url, headers=headers)
        jsonData = req.text
        data = json.loads(jsonData)
        timeSeriesData = data['data']
        if timeSeriesData is None:
            size = csvDataFrame.index.size
            y = time.strftime("%Y", time.localtime())
            date = time.strftime("%m.%d", time.localtime())
            csvDataFrame.loc[size] = [
                province, province, y,
                str(date), '0', '', '', '', ''
            ]
            print(csvDataFrame.loc[size])
            continue
        # null 说明api有问题（命名错误）或者该地未发生疫情
        for i in timeSeriesData:
            size = csvDataFrame.index.size
            try:
                y = i['y']
            except KeyError:
                y = i['year']
            csvDataFrame.loc[size] = [
                province, province, y,
                str(i['date']), i['confirm'], i['dead'], i['heal'], '',
                i['confirm_add']
            ]

    # csvDataFrame.to_excel('rawData' + local_timestamp() + '.xlsx',
    #                       encoding='utf-8-sig')
    # print('rawData' + local_timestamp() + '.xlsx has been written!')
    csvDataFrame.to_excel('rawData'+'.xlsx',
                          encoding='utf-8-sig')
    print('rawData' + '.xlsx has been written!')


if __name__ == '__main__':
    writeRawData()