#main.py
import pyb
import upcd8544
from machine import SPI,Pin
from pyb import Pin
import os

def main():
    SPI    = pyb.SPI(1) #DIN=>X8-MOSI/CLK=>X6-SCK
    #DIN =>SPI(1).MOSI 'X8' data flow (Master out, Slave in)
    #CLK =>SPI(1).SCK  'X6' SPI clock
    
    RST    = pyb.Pin('X1')
    CE     = pyb.Pin('X2')
    DC     = pyb.Pin('X3')
    LIGHT  = pyb.Pin('X4')
    lcd_5110 = upcd8544.PCD8544(SPI, RST, CE, DC, LIGHT)
    x21 = Pin('X21', Pin.OUT_PP) #定义X21为输出信号
    x22 = Pin('X22', Pin.OUT_PP) #定义X22为输出信号
    x10 = Pin('X10', Pin.IN) #设置X10为启动测试接口，与GND短接后启动测试
    while True:
        if x10.value() == 0:
            ######循环检测模式，提高检测精度
            print(x10.value())
            number = 0
            test_num = 250 #检测次数
            b_1 = []
            b_2 = []#检测结果列表
            #检测循环
            while number < test_num:
                number += 1
                pyb.delay(1)
                names_1 = locals()
                names_1['adc%s' % number] = pyb.ADC(pyb.Pin('X11')).read() #循环检测X11端口数据
                # 将每次循环检测结果添加到列表中
                b_1.append(names_1['adc%s' % number])
                names_2 = locals()
                names_2['adc%s' % number] = pyb.ADC(pyb.Pin('Y11')).read() #循环检测Y11端口数据
                b_2.append(names_2['adc%s' % number])
            #将列表中数据相加
            sum_1 = 0
            for i in range(len(b_1)):
                sum_1 += b_1[i]
            data_1 = sum_1 / test_num
            sum_2 = 0
            for j in range(len(b_2)):
                sum_2 += b_2[j]
            data_2 = sum_2 / test_num
            #print(data)
            valtage_1 = ("%.3f" % (data_1*3.3/4096*2)) #ADC读数转换为电压值,电压值取小数点后3位
            lcd_5110.lcd_write_string('V=' + valtage_1 + 'V', 0,0)
            valtage_2 = ("%.3f" % (data_2*3.3/4096*1.626))
            lcd_5110.lcd_write_string('I=' + valtage_2 + 'A', 0,1)

            #判断电压电流值上下限
            if valtage_1 < '4.8' or valtage_1 > '5.2' or valtage_2 < '1.75' or valtage_2 > '1.85':
                lcd_5110.lcd_write_string('Fail', 0,2)
                x21.high()
                x22.low()
            else:
                lcd_5110.lcd_write_string('Pass', 0,2)
                x22.high()
                x21.low()
                '''
                # 向SD卡追加写入数据
                with open('/sd/data1.txt', 'a') as f:
                    f.write(valtage_1 + 'V' + valtage_2 + 'A' '\r\n')
                '''
        else:
            continue
if __name__ == '__main__':
    main()