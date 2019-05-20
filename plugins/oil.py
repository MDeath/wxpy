# LBVHZ3109HMG70448
# LFV2B21K9B3237949
# LSGJR52U855110284
# LWVDA2067GB000986

from bs4 import BeautifulSoup as bs
import requests

def oil(vin):
    try:
        data = {
            'vinCode': vin
        }

        cas = bs(requests.post('http://market.vin114.net/lamuApp/level/LaMu/getVehiclesByVinCode', data=data).text, 'lxml').find('tr', {'class':'select-value'})
        if cas is None:return '未查询到车型信息'
        else:
            data = {
                'levelId': cas.get('levelid'),
                'brandName': cas.get('brand'),
                'newFactory': cas.get('newfactory'),
                'modelsName': cas.get('models'),
                'displacement': cas.get('displacement'),
                'induction': cas.get('induction'),
                'year': cas.get('year'),
                'gearNumber': cas.get('gearnumber'),
                'transmissionDescription': cas.get('transmissiondescription'),
                'engineModel': cas.get('enginemodel')
            }

            response = requests.post('http://market.vin114.net/lamuApp/level/LaMu/getOilProducts', data=data)
            oil_list = bs(response.text, 'lxml').find_all('table', {'class':'table table-bordered'})[1]
            str_list = oil_list.find_all('td')
            msg = ''
            msg += '车型： %s\n' % cas.get('brand')
            msg += '厂商： %s\n' % cas.get('newfactory')
            msg += '车型： %s\n' % cas.get('models')
            msg += '排量： %s\n' % cas.get('displacement')
            msg += '进气类型： %s\n' % cas.get('induction')
            msg += '出厂时间： %s\n' % cas.get('year')
            msg += '挡位数： %s\n' % cas.get('gearnumber')
            msg += '变速器类型： %s\n' % cas.get('transmissiondescription')
            msg += '发动机型号： %s\n' % cas.get('enginemodel')
            for string in str_list:
                text = string.text
                if '  ' in text:
                    text = text.replace('  ', '')
                if '\t' in text:
                    text = text.replace('\t', '')
                if '\r' in text:
                    text = text.replace('\r', '')
                if '\n' in text:
                    text = text.replace('\n', '')
                if '(图)' in text:
                    text = text.replace('(图)', '')
                if 'PLATIN' in text:
                    text = text.replace('PLATIN', 'ROWE')
                if '查看图片' in text or '位置' in text:
                    continue
                if 'td-label' in string.get('class'):
                    msg += text + '\n'
                elif 'td-value' in string.get('class'):
                    msg += '    %s\n' % text
            return msg
    except:return '该车架没有数据'

if __name__ == "__main__":
    while True:
        vin = input('请输入车架号：')
        if len(vin) == 17:break
        else:print('车架号不对')
    print(oil(vin))