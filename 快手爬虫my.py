import requests,re,os
from moviepy.editor import VideoFileClip, concatenate_videoclips


def Video_concatenate(dir_data_path):
    '''concatenate all the mp4 videos in the directory of dir_data_path'''
    # 参数设置
    # 分散视频路径
    suffix = '.mp4'  # 分散的视频后缀
    save_path = f"{dir_data_path}\\all_compilation.mp4"  # 合并后的视频名称
    # 开始合并
    file_names = []
    for root, dirs, files in os.walk(dir_data_path):
        # 按文件名排序
        files.sort()
        # 遍历所有文件
        for file in files:
            # 如果后缀名为 .mp4
            if os.path.splitext(file)[1] == suffix:
                # 拼接成完整路径
                filePath = os.path.join(root, file)
                # 载入视频
                print(f'adding {filePath} to the clip list')
                video = VideoFileClip(filePath)
                # 添加到数组
                file_names.append(video)
    # 拼接视频
    clip = concatenate_videoclips(file_names)
    # 生成目标视频文件
    clip.to_videofile(save_path, fps=24, remove_temp=False)

def Change_to_MP3(dir_data_path):
    for roots,dirs,files in os.walk(dir_data_path):
        for file in files:
            path_1=os.path.join(root,file)
            name=os.path.splitext(file)[0]
            path_2=os.path.join(root,name+'mp3')
            if os.path.splitext(file)[1]=='.mp4':
                try:
                    os.rename(path_1, path_2)
                except Exception as e:
                    print(e)
                    print('rename file fail\r\n')
                else:
                    print('rename file success\r\n')

class KuaishouDownload:
    def __init__(self,user_name,Download_dir_path):
        self.Download_dir_path=Download_dir_path
        self.user_name=user_name
        self.user_id=''
        self.video_num=0
        self.video_current=set()
    #根据用户名称搜索用户id
    def set_user_id(self):
        try:
            url_1 = 'https://www.kuaishou.com/graphql'
            headers_1 = {'Accept-Encoding': 'gzip, deflate, br',
                         'Accept-Language': 'zh-CN,zh;q=0.9',
                         'Connection': 'keep-alive',
                         'Content-Length': '671',
                         'content-type': 'application/json',
                         'Cookie': 'kpf=PC_WEB; kpn=KUAISHOU_VISION; clientid=3; didv=1672468991933; did=web_ef16c83d100f0f30e7d49a49fe5faa91',
                         'Host': 'www.kuaishou.com',
                         'Origin': 'https://www.kuaishou.com',
                         'Referer': 'https://www.kuaishou.com/search/author?searchKey=%E2%9C%A8%E6%8D%8C%E9%9B%B6%E5%BE%8C%E2%9C%A8%E5%B0%8F%E5%93%A5',
                         'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
                         'sec-ch-ua-mobile': '?0',
                         'sec-ch-ua-platform': 'Windows',
                         'Sec-Fetch-Dest': 'empty',
                         'Sec-Fetch-Mode': 'cors',
                         'Sec-Fetch-Site': 'same-origin',
                         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36}'}
            payload_1 = {
                'operationName': "graphqlSearchUser",
                'query': "query graphqlSearchUser($keyword: String, $pcursor: String, $searchSessionId: String) {\n  visionSearchUser(keyword: $keyword, pcursor: $pcursor, searchSessionId: $searchSessionId) {\n    result\n    users {\n      fansCount\n      photoCount\n      isFollowing\n      user_id\n      headurl\n      user_text\n      user_name\n      verified\n      verifiedDetail {\n        description\n        iconType\n        newVerified\n        musicCompany\n        type\n        __typename\n      }\n      __typename\n    }\n    searchSessionId\n    pcursor\n    __typename\n  }\n}\n",
                'variables': {'keyword': self.user_name},
                "pcursor": "1.669100020464E12",
                "page": "profile",
            }
            proxy = {'http': None, 'https': None}
            request_url_id = requests.post(url=url_1, json=payload_1, headers=headers_1, verify=False, proxies=proxy)
            p_0 = re.compile(r'"user_id":".*?"')
            #设置self.user_id!
            self.user_id = p_0.findall(request_url_id.text)[0][11:-1]
            print('user_id is ',self.user_id)
            # return [user_id, user_name]
        except:
            print('please wait, we are fixing the problem')
            self.set_user_id()
    #下载id的视频（可选择是否自动生成合集，以及是否删除剩余文件）
    def get_video_dowloaded(self,fir,sec):
        # 准备链接、伪装
        url_1 = 'https://www.kuaishou.com/graphql'
        headers_2 = {
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Length': '1244',
            'content-type': 'application/json',
            'Cookie': 'did=web_3e279ebec66a74219408aa8a2d8a0c82; didv=1671357370350; _bl_uid=0Xlh5bhetI87ev0Okwy1ukby0vwh; kpf=PC_WEB; kpn=KUAISHOU_VISION; clientid=3; client_key=65890b29; ktrace-context=1|MS43NjQ1ODM2OTgyODY2OTgyLjUyNDgyMTY3LjE2NzI2NjA2MDQ1NTYuNjk5MDI=|MS43NjQ1ODM2OTgyODY2OTgyLjg2NzM2MTk3LjE2NzI2NjA2MDQ1NTYuNjk5MDM=|0|graphql-server|webservice|false|NA; userId=2087467761; kuaishou.server.web_st=ChZrdWFpc2hvdS5zZXJ2ZXIud2ViLnN0EqABJtS4x96CKuscMF8a9UIDjPTa27LVdmWt58UqdZ0j4F2V_QzTiVx8ClowOL-ET3Gn684MJB9FMwVwT8ee0V9zzsyabRxWpsNQZ0q0E7LIDTUL3ucs0C-6uRiCc956yRh3U7OnYhLT1C8fQcG8iDJxWcpMxv8KY8yvKENbEixnbbKGbsWgH98NZxFXhdT08ByiP8NXnlB-A475gcRdIYEfyBoSnIqSq99L0mk4jolsseGdcwiNIiATmgSTJrwWdxO_cL_q08u7AAk-4CcPzRX8o3b_wcTslCgFMAE; kuaishou.server.web_ph=fbf13d1486e97caa49535117ab49c4844647',
            'Host': 'www.kuaishou.com',
            'Origin': 'https://www.kuaishou.com',
            'Referer': f'https://www.kuaishou.com/profile/{self.user_id}',
            'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': 'Windows',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
        }
        payload = {
            'operationName': "visionProfilePhotoList",
            'query': "fragment photoContent on PhotoEntity {\n  id\n  duration\n  caption\n  originCaption\n  likeCount\n  viewCount\n  realLikeCount\n  coverUrl\n  photoUrl\n  photoH265Url\n  manifest\n  manifestH265\n  videoResource\n  coverUrls {\n    url\n    __typename\n  }\n  timestamp\n  expTag\n  animatedCoverUrl\n  distance\n  videoRatio\n  liked\n  stereoType\n  profileUserTopPhoto\n  musicBlocked\n  __typename\n}\n\nfragment feedContent on Feed {\n  type\n  author {\n    id\n    name\n    headerUrl\n    following\n    headerUrls {\n      url\n      __typename\n    }\n    __typename\n  }\n  photo {\n    ...photoContent\n    __typename\n  }\n  canAddComment\n  llsid\n  status\n  currentPcursor\n  tags {\n    type\n    name\n    __typename\n  }\n  __typename\n}\n\nquery visionProfilePhotoList($pcursor: String, $userId: String, $page: String, $webPageArea: String) {\n  visionProfilePhotoList(pcursor: $pcursor, userId: $userId, page: $page, webPageArea: $webPageArea) {\n    result\n    llsid\n    webPageArea\n    feeds {\n      ...feedContent\n      __typename\n    }\n    hostName\n    pcursor\n    __typename\n  }\n}\n",
            'variables': {'userId': f'{self.user_id}', 'pcursor': f"1.6{fir}{sec}287673409E12", 'page': "profile"}
        }
        proxy = {'http': None, 'https': None}
        # 得到用户所有的视频标题，以及下载链接
        try:
            request_url = requests.post(url=url_1, json=payload, headers=headers_2)
            p1 = re.compile(r'"originCaption":.*?","manifest":')
            p2 = re.compile(r'"originCaption":".*?","likeCount":')
            p3 = re.compile(r'"photoH265Url":".*?"')
            request_url_text = request_url.text
            request_url_list = p1.findall(request_url_text)
            for i in range(len(request_url_list)):
                request_name = p2.findall(request_url_list[i])[0][17:-14]
                request_video_url = p3.findall(request_url_list[i])[0][16:-1]
                request_url_list[i] = [request_name, request_video_url]
        except:
            self.get_video_dowloaded( com=False, remove_rest=False)

        # 下载视频到指定path
        if os.path.exists(self.Download_dir_path):
            pass
        else:
            os.mkdir(self.Download_dir_path)
        if os.path.exists(f'{self.Download_dir_path}\\{self.user_name}'):
            pass
        else:
            os.mkdir(f'{self.Download_dir_path}\\{self.user_name}')
        for i in range(len(request_url_list)):
            try:
                request_video = requests.get(request_url_list[i][1], verify=False, proxies=proxy).content
                print('requested videos reached')
            except:
                self.get_video_dowloaded(fir,sec)
            if os.path.exists(f'{self.Download_dir_path}\\{self.user_name}\\{self.user_name}{request_url_list[i][0]}.mp4'):
                pass
            else:
                try:
                    with open(f'{self.Download_dir_path}\\{self.user_name}\\{request_url_list[i][0]} {self.user_name}.mp4',
                          mode='wb') as f:
                        f.write(request_video)
                        f.close()
                except:
                    pass
            file_num=0
            for root,dir,files in os.walk(f'{self.Download_dir_path}\\{self.user_name}'):
                file_num=len(files)
            print(f'{file_num} videoes have been downloaded,please wait')

        # 自动生成合集：
        # 自动生成合集后，删除其余文件
    #把下载的视频，拼接成一个合集
    def concatenate_videoes(self,remove_rest=False):

        # 参数设置
        data_path = f'{self.Download_dir_path}\\{self.user_name}'  # 分散视频路径
        suffix = '.mp4'  # 分散的视频后缀
        save_path = f"{self.Download_dir_path}\\{self.user_name}\\{self.user_name} compilation.mp4"  # 合并后的视频名称

        # 开始合并
        file_names = []
        for root, dirs, files in os.walk(data_path):
            # 按文件名排序
            files.sort()
            # 遍历所有文件
            for file in files:
                # 如果后缀名为 .mp4
                if os.path.splitext(file)[1] == suffix:
                    # 拼接成完整路径
                    filePath = os.path.join(root, file)
                    # 载入视频
                    video = VideoFileClip(filePath)
                    # 添加到数组
                    file_names.append(video)
        # 拼接视频
        clip = concatenate_videoclips(file_names)
        # 生成目标视频文件
        clip.to_videofile(save_path, fps=24, remove_temp=False)

        if remove_rest:
            for i in range(len(request_url_list)):
                os.remove(f"{self.Download_dir_path}\\{self.user_name}\\{self.user_name}{i + 1}.mp4")
    #运行程序：集合的函数
    def run_download(self,make_compilation=False,remove_rest=False):
        self.set_user_id()
        for a in range(1,7):
            for b in range(1,10):
                self.get_video_dowloaded(fir=a,sec=b)
        if make_compilation:
            self.concatenate_videoes(remove_rest=remove_rest)
        #os.remove(f"{self.user_name} compilationTEMP_MPY_wvf_snd.mp3")




if __name__ == "__main__":
    Download_dir_path='D:\桌面文件夹\随意\pdf压缩器（到指定大小）\PhotoReducer'#输入保存的文件夹
    user_name_list=['is橙子']#输入每个要搜索的用户名
    for i in user_name_list:
        ob = KuaishouDownload(i, Download_dir_path)
        ob.run_download(make_compilation=False,remove_rest=False)
    #如果想要自动生成合集，把make_compliation设置成true
    #如果想在生成合集之后，删除文件夹内其它视频
    # Video_concatenate(Download_dir_path)
