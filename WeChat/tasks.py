# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery_once import QueueOnce
from Data.models import Tag, DBSource
from WeChat.models import TagInfo, AgentInfo, TagUsersInfo, EmployeInfo, OrgInfo
from ScheduleTasks.tasksfile.common_code import Sql, Email
from ScheduleTasks.tasksfile.common_code import WeChat
import json
import traceback


@shared_task(base=QueueOnce, once={'graceful': True})
def tag_update(**kwargs):
    receives = kwargs['receives']
    W = WeChat()
    res = W.get_tag_list()
    try:
        for tag_one in res['taglist']:
            defaults = {
                "tagid": tag_one['tagid'],
                "tagname": tag_one['tagname']}
            obj, created = TagInfo.objects.update_or_create(
                tagid=tag_one['tagid'],
                defaults=defaults)
            # print(tag_one)
            print(obj, created)
        return "标签更新成功..."
    except Exception as e:
        E = Email(type="alarm")
        message = ["企业微信-标签更新", "WeChat.tasks.tag_update"]
        message.append(traceback.format_exc().replace("\n", "<br>").replace(" ", "&nbsp;"))
        E.send_mail(receivers=receives, message=message)
        return e

    finally:
        queryset = TagInfo.objects.all()
        local_list = []
        wechat_list = []
        for item in queryset:
            local_list.append(item.tagid)
        for item in res['taglist']:
            wechat_list.append(item['tagid'])
        invalid_list = list(set(local_list) - set(wechat_list))
        print("invalid tagid: %s" % invalid_list)
        if invalid_list:
            for tagid in invalid_list:
                TagInfo.objects.filter(tagid=tagid).delete()


@shared_task(base=QueueOnce, once={'graceful': True})
def agent_update(**kwargs):
    receives = kwargs['receives']
    W = WeChat()
    res = W.get_agent_list()
    try:
        for agent_one in res['agentlist']:
            defaults = {
                "agentid": agent_one['agentid'],
                "name": agent_one['name']}
            obj, created = AgentInfo.objects.update_or_create(
                agentid=agent_one['agentid'],
                defaults=defaults)
            print(obj, created)
        return "应用更新成功..."
    except Exception as e:
        E = Email(type="alarm")
        message = ["企业微信-应用更新", "WeChat.tasks.agent_update"]
        message.append(traceback.format_exc().replace("\n", "<br>").replace(" ", "&nbsp;"))
        E.send_mail(receivers=receives, message=message)
        return e
    finally:
        queryset = AgentInfo.objects.all()
        local_list = []
        wechat_list = []
        for item in queryset:
            local_list.append(item.agentid)
        for item in res['agentlist']:
            wechat_list.append(item['agentid'])
        invalid_list = list(set(local_list) - set(wechat_list))
        print("invalid agentid: %s" % invalid_list)
        if invalid_list:
            for agentid in invalid_list:
                AgentInfo.objects.filter(agentid=agentid).delete()


@shared_task(base=QueueOnce, once={'graceful': True})
def tag_users_update(**kwargs):
    receives = kwargs['receives']
    W = WeChat()
    queryset = TagInfo.objects.all()
    try:
        for item in queryset:
            tagid = str(item.tagid)
            res = W.get_tag_users(tagid)
            userlist = json.dumps(res['userlist'])
            partylist = json.dumps(res['partylist'])
            defaults = {
                "tagid": tagid,
                "tagname": res['tagname'],
                "partylist": partylist,
                "userlist": userlist}
            obj, created = TagUsersInfo.objects.update_or_create(
                tagid=tagid,
                defaults=defaults)
            print(obj, created)
        return "标签成员更新成功..."
    except Exception as e:
        E = Email(type="alarm")
        message = ["企业微信-标签成员更新", "WeChat.tasks.tag_users_update"]
        message.append(traceback.format_exc().replace("\n", "<br>").replace(" ", "&nbsp;"))
        E.send_mail(receivers=receives, message=message)
        return e

@shared_task(base=QueueOnce, once={'graceful': True})
def org_update(**kwargs):
    sql_list = kwargs['sql']
    sqlone_id = kwargs['sql'][0]['id']
    receives = kwargs['receives']
    dbsource_id = Tag.objects.values("dbsource").get(pk=sqlone_id)["dbsource"]
    DB = DBSource.objects.get(pk=dbsource_id)
    DB_HOST = DB.address
    DB_USER = DB.user
    DB_PASS = DB.password
    DB_NAME = DB.database
    DB_SQL = Tag.objects.get(pk=sql_list[0]["id"]).sql

    S = Sql(
        username=DB_USER,
        password=DB_PASS,
        db=DB_NAME,
        host=DB_HOST,
        sql=DB_SQL)
    data = S.get_row()
    data = json.loads(data)
    try:
        for item in data:
            print(item)
            defaults = {
                "org_id": item[0],
                "name": item[1],
                "parent_id": item[2],
                "full_name": item[3],
                "tel": item[4],
                "property": item[5]}
            obj, created = OrgInfo.objects.update_or_create(
                org_id=item[0],
                parent_id=item[2],
                # property=item[5],
                defaults=defaults)
            print(obj, created)
        return "组织更新成功..."
    except Exception as e:
        E = Email(type="alarm")
        message = ["企业微信-组织更新", "WeChat.tasks.org_update"]
        message.append(traceback.format_exc().replace("\n", "<br>").replace(" ", "&nbsp;"))
        E.send_mail(receivers=receives, message=message)
        return e

@shared_task(base=QueueOnce, once={'graceful': True})
def employe_update(**kwargs):
    sql_list = kwargs['sql']
    sqlone_id = kwargs['sql'][0]['id']
    receives = kwargs['receives']
    dbsource_id = Tag.objects.values("dbsource").get(pk=sqlone_id)["dbsource"]
    DB = DBSource.objects.get(pk=dbsource_id)
    DB_HOST = DB.address
    DB_USER = DB.user
    DB_PASS = DB.password
    DB_NAME = DB.database
    DB_SQL = Tag.objects.get(pk=sql_list[0]["id"]).sql

    S = Sql(
        username=DB_USER,
        password=DB_PASS,
        db=DB_NAME,
        host=DB_HOST,
        sql=DB_SQL)
    data = S.get_row()
    data = json.loads(data)
    try:
        for item in data:
            # print(item)
            defaults = {
                "userid": item[0],
                "name": item[1],
                "org_id": item[2],
                "position": item[3],
                "leader": item[4],
                "mobile": item[5],
                "email": item[6],
                "enable": item[7],
                "status": item[8]}
            obj, created = EmployeInfo.objects.update_or_create(
                userid=item[0],
                org_id=item[2],
                defaults=defaults)
            print(obj, created)
        return "组织成员更新成功..."
    except Exception as e:
        E = Email(type="alarm")
        message = ["企业微信-成员更新", "WeChat.tasks.employe_update"]
        message.append(traceback.format_exc().replace("\n", "<br>").replace(" ", "&nbsp;"))
        E.send_mail(receivers=receives, message=message)
        return e
