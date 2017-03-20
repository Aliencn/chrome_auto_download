# chrome_auto_download
python3

##Windows运行前配置
pip install requests
pip install requests[socks]
pip install requests[security]
pip install beautifulsoup4
pip install selenium

##Linux运行前配置
pip install requests
pip install requests[socks]
pip install requests[security]
pip install beautifulsoup4
pip install selenium
chmod 755 phantomjs
ln phantomjs /bin/

还需要安装phantomjs的所需库，phantomjs官网说明如下
'''
Note: For this static build, the binary is self-contained.
There is no requirement to install Qt, WebKit, or any other libraries. 
It however still relies on Fontconfig (the package fontconfig or libfontconfig, depending on the distribution).
The system must have GLIBCXX_3.4.9 and GLIBC_2.7.
'''


##支持其他系统的phantomjs版本下载
http://phantomjs.org/download.html



##使用说明
'''
from chrome_download import chrome_download
chrome=chrome_download()

#设置代理，可选项
chrome.set_proxy('socks5://127.0.0.1:1080')
chrome.test_proxy()

#下载路径
chrome.chrome_download_dir=r'download'

#chrome版本，目前支持的版本['win','win64','mac']
chrome.chrome_os='win64'

#检查新版本，并下载
chrome.check_download()
'''


##注
windows版chrome建议检查一下数字签名是否正常后再安装
mac和linux我不知道咋检查数字签名