import json
import re
from datetime import datetime

import frontmatter
import markdown
from ehall.conf import settings
from ehall.njmu import Client
from rich import print
from rich.table import Table


class Yjsyss(Client):
    def __init__(self, username=None, password=None, *, login_url=None, app_id=None, base_url=None):
        super().__init__(username, password)
        self.app_id = settings.INSTALLED_APPS[self.__class__.__name__] if app_id is None else app_id
        self.base_url = self.get_base_url() if base_url is None else base_url

    def get_base_url(self):
        self.login()
        response = self.session.get('http://ehall.njmu.edu.cn/appShow?appId=%s' % self.app_id)
        return 'http://yjsyss.njmu.edu.cn%s%%s' % re.search(r'/gmis5/\((\S+)\)/', response.text).group(0)

    def get_records(self):
        response = self.session.get(self.base_url % 'student/pygl/xskyzr_list')
        return json.loads(response.text)['rows']

    def print_records(self):
        rows = self.get_records()

        table = Table(title='xskyzr_list')
        table.add_column('RowNumber')
        table.add_column('id')
        table.add_column('title')
        table.add_column('txrq')

        for row in rows:
            table.add_row(
                row['RowNumber'],
                row['id'],
                row['title'],
                row['txrq'],
            )
        print(table)

    def load_record_content(self, id):
        response = self.session.get(self.base_url % 'student/pygl/xsrz_load?id=%s' % id)
        return json.loads(response.text)['infoxx']['content']

    def delete_record_by_id(self, id):
        response = self.session.post(self.base_url % 'student/pygl/delxsrzByid', data={"ids": "[%s]" % id})
        return json.loads(response.text)['flag']

    def upload_image_from_file(self, filename):
        upfile = open(filename, 'rb')
        response = self.session.post(self.base_url % 'Scripts/ueditor/net/controller.ashx?action=uploadimage', files={"upfile": upfile})
        return response

    def save_record_from_file(self, filename):
        try:
            post = frontmatter.load(filename)
        except FileNotFoundError:
            return None

        assert ['title', 'txrq'] <= list(post.keys())
        assert datetime.strptime(str(post['txrq']), '%Y-%m-%d %H:%M:%S')

        data = {
            "id": "0",
            "title": post['title'],                     # 标题
            "content": markdown.markdown(post.content), # 内容
            "txrq": post['txrq'],                       # 填写日期
            "tjbj": "0",
        }
        response = self.session.post(self.base_url % 'student/pygl/xsrz_save', data={"json": json.dumps(data, default=str)})
        return response

    def get_lectures(self):
        response = self.session.get(self.base_url % 'student/pygl/xsjzbm_bind')
        rows = json.loads(response.text)['rows']

        candidates = []
        for row in rows:
            if datetime.strptime(row['bmkssj'], '%Y-%m-%d %H:%M:%S') > datetime.now():
                candidates.append(row)
        return candidates

    def register_lecture_by_id(self, id):
        import ddddocr
        ocr = ddddocr.DdddOcr()
        response = self.session.get(self.base_url % 'student/pygl/VerificationCode')
        code = ocr.classification(response.content)

        data = {
            "id": id,
            "code": code,
        }
        response = self.session.post(self.base_url % 'student/pygl/xsjzbmDoCode', data=data)
        return response
