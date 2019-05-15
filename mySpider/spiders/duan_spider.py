# -*- coding: utf-8 -*-
"""
语言版本：
python：3.7
scrapy：1.6
功能：不使用正则表达式,改用scrapy爬取段子.

"""
import scrapy

class DuanZiSpider(scrapy.Spider):
    name = "duanSpider"
    allowed_domains = ["duanziwang.com"]
    start_urls = ['http://duanziwang.com/category/经典段子/']

    def parse(self, response):
        duanzi_list = response.css('article')  # 提取首页所有笑话，保存至变量duanzi_list
        for viv in duanzi_list:  # 循环获取每一条笑话里面的：标题、内容
            title = viv.css('.post-title a::text').extract_first()  # 提取笑话标题
            contents = viv.css('.post-content p::text').extract()  # 提取笑话内容
            text = ''.join(contents)
            # text = text.encode('UTF-8','ignore')
            # text = text.encode('gb2312','ignore')
            """
            接下来进行写文件操作，储存在一个txt文档里面
            """
            file_name = 'happy.txt'  # 定义文件名,如：happy.txt
            f = open(file_name, "a+", encoding='utf-8')  # “a+”以追加的形式
            f.write('标题：' + str(title))
            f.write('\n')  # ‘\n’ 表示换行
            f.write(str(text))
            f.write('\n-------\n')
            f.close()

        next_page = response.css('.next::attr(href)').extract_first()  # css选择器提取下一页链接
        # print("!!!!!!The page is:" + str(next_page))
        if next_page is not None:  # 判断是否存在下一页

            """
             相对路径如：/page/1
             urljoin能把相对路径替我们转换为绝对路径，也就是加上文件开头设置的域名
             最终next_page为：http://host/page/2/        
            """
            next_page = response.urljoin(next_page)
            """
            scrapy.Request()
            第一个参数：下一页链接，第二个参数为内容回调处理函数，这里是parse函数。
            不断的爬取，直到不存在下一页
            """
            yield scrapy.Request(next_page, callback=self.parse)