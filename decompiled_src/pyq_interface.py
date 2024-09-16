#Embedded file name: /WORKSPACE/data/entities/client/helpers/pyq_interface.o
import re
import httplib
import urllib
import urllib2
import time
import random
import os
import json
import remoteInterface
import BigWorld
import const
import pyBgTask
from helpers import seqTask
from helpers import httpHelper
import gamelog
from cdata import game_msg_def_data as GMDD
from callbackHelper import Functor
host = '192.168.131.156'
port = '88'
PUBLISH_URL = 'symtuc-pgpp-ty-md-ssl.netease.com'

def getBaseUrl():
    p = BigWorld.player()
    if p.pyq_forcePublishUrl:
        return PUBLISH_URL
    elif BigWorld.isPublishedVersion():
        return PUBLISH_URL
    else:
        return ''.join((host, ':', port))


def commonRequest(callback, url, mothedType = 'GET'):
    baseUrl = getBaseUrl()
    conn = None
    p = BigWorld.player()
    isHttps = BigWorld.isPublishedVersion() or p.pyq_forcePublishUrl
    if isHttps:
        conn = httplib.HTTPSConnection(baseUrl)
    else:
        conn = httplib.HTTPConnection(baseUrl)
    conn.request(mothedType, url)
    r = conn.getresponse()
    if r.status != 200:
        if callback:
            callback(r.status, {})
        return
    content = r.read()
    conn.close()
    data = json.loads(content, object_hook=remoteInterface._jsonEncoderHook)
    if callback:
        callback(r.status, data)


def __getProfile(callback, gbId):
    try:
        p = BigWorld.player()
        url = '/ty/md/user/get_profile?'
        m = {'roleid': p.gbId,
         'skey': p.pyq_skey,
         'targetid': gbId}
        params = urllib.urlencode(m)
        url += params
        commonRequest(callback, url)
    except:
        if callback:
            callback(1, {})
        return


def getProfile(callback, gbId):
    mgr = pyBgTask.getMgr()
    mgr.add_task(__getProfile, (mgr.make_callback(callback), gbId))


def __getNewNum(callback):
    try:
        p = BigWorld.player()
        url = '/ty/md/inform/newNum?'
        m = {'roleid': p.gbId,
         'skey': p.pyq_skey}
        params = urllib.urlencode(m)
        url += params
        commonRequest(callback, url)
    except:
        if callback:
            callback(1, {})
        return


def getNewNum(callback):
    mgr = pyBgTask.getMgr()
    mgr.add_task(__getNewNum, (mgr.make_callback(callback),))


def __getRedDot(callback):
    try:
        p = BigWorld.player()
        url = '/ty/md/inform/getRedDot?'
        m = {'roleid': p.gbId,
         'skey': p.pyq_skey}
        params = urllib.urlencode(m)
        url += params
        commonRequest(callback, url)
    except:
        if callback:
            callback(1, {})
        return


def getRedDot(callback):
    mgr = pyBgTask.getMgr()
    mgr.add_task(__getRedDot, (mgr.make_callback(callback),))


def __getHomeMoments(callback, pageCount):
    try:
        p = BigWorld.player()
        url = '/ty/md/moment/list_home?'
        m = {'roleid': p.gbId,
         'skey': p.pyq_skey,
         'page': pageCount,
         'pageSize': const.PERSONAL_ZONE_MOMENTS_NUM_PER_PAGE}
        params = urllib.urlencode(m)
        url += params
        commonRequest(callback, url)
    except:
        if callback:
            callback(1, {})
        return


def getHomeMoments(callback, pageCount):
    mgr = pyBgTask.getMgr()
    mgr.add_task(__getHomeMoments, (mgr.make_callback(callback), pageCount))


def __getUserMoments(callback, gbId, pageCount):
    try:
        p = BigWorld.player()
        url = '/ty/md/moment/list_user?'
        m = {'roleid': p.gbId,
         'skey': p.pyq_skey,
         'targetid': gbId,
         'page': pageCount,
         'pageSize': const.PERSONAL_ZONE_MOMENTS_NUM_PER_PAGE}
        params = urllib.urlencode(m)
        url += params
        commonRequest(callback, url)
    except:
        if callback:
            callback(1, {})
        return


def getUserMoments(callback, gbId, pageCount):
    mgr = pyBgTask.getMgr()
    mgr.add_task(__getUserMoments, (mgr.make_callback(callback), gbId, pageCount))


def __getCurServerHotMoments(callback, hostId, pageCount):
    try:
        p = BigWorld.player()
        url = '/ty/md/moment/list_cur_server_hot?'
        m = {'roleid': p.gbId,
         'skey': p.pyq_skey,
         'server': hostId,
         'page': pageCount,
         'pageSize': const.PERSONAL_ZONE_MOMENTS_NUM_PER_PAGE}
        params = urllib.urlencode(m)
        url += params
        commonRequest(callback, url)
    except:
        if callback:
            callback(1, {})
        return


def getCurServerHotMoments(callback, hostId, pageCount):
    mgr = pyBgTask.getMgr()
    mgr.add_task(__getCurServerHotMoments, (mgr.make_callback(callback), hostId, pageCount))


def __getAllServerHotMoments(callback, pageCount):
    try:
        p = BigWorld.player()
        url = '/ty/md/moment/list_all_server_hot?'
        m = {'roleid': p.gbId,
         'skey': p.pyq_skey,
         'page': pageCount,
         'pageSize': const.PERSONAL_ZONE_MOMENTS_NUM_PER_PAGE}
        params = urllib.urlencode(m)
        url += params
        commonRequest(callback, url)
    except:
        if callback:
            callback(1, {})
        return


def getAllServerHotMoments(callback, pageCount):
    mgr = pyBgTask.getMgr()
    mgr.add_task(__getAllServerHotMoments, (mgr.make_callback(callback), pageCount))


def __getTopicMoments(callback, topicId, sort, pageCount, serverId = 0):
    try:
        p = BigWorld.player()
        url = '/ty/md/topic/moment/list?'
        m = {'roleid': p.gbId,
         'skey': p.pyq_skey,
         'topicId': topicId,
         'sort': sort,
         'page': pageCount,
         'pageSize': const.PERSONAL_ZONE_MOMENTS_NUM_PER_PAGE}
        if sort == 'cur_server':
            m['serverId'] = serverId
        params = urllib.urlencode(m)
        url += params
        commonRequest(callback, url)
    except:
        if callback:
            callback(1, {})
        return


def getTopicMoments(callback, topicId, sort, pageCount, serverId = 0):
    mgr = pyBgTask.getMgr()
    mgr.add_task(__getTopicMoments, (mgr.make_callback(callback),
     topicId,
     sort,
     pageCount,
     serverId))


def __getMomentById(callback, momentId):
    try:
        p = BigWorld.player()
        url = '/ty/md/moment/get_by_id?'
        m = {'roleid': p.gbId,
         'skey': p.pyq_skey,
         'id': momentId}
        params = urllib.urlencode(m)
        url += params
        commonRequest(callback, url)
    except:
        if callback:
            callback(1, {})
        return


def getMomentById(callback, momentId):
    mgr = pyBgTask.getMgr()
    mgr.add_task(__getMomentById, (mgr.make_callback(callback), momentId))


def __getCommentList(callback, momentId, pageCount):
    try:
        p = BigWorld.player()
        url = '/ty/md/comment/list?'
        m = {'roleid': p.gbId,
         'skey': p.pyq_skey,
         'id': momentId,
         'page': pageCount,
         'pageSize': const.PERSONAL_ZONE_MOMENT_COMMENT_NUM_PER_PAGE}
        params = urllib.urlencode(m)
        url += params
        commonRequest(callback, url)
    except:
        if callback:
            callback(1, {})
        return


def getCommentList(callback, momentId, pageCount):
    mgr = pyBgTask.getMgr()
    mgr.add_task(__getCommentList, (mgr.make_callback(callback), momentId, pageCount))


def __getForwardList(callback, momentId, pageCount):
    try:
        p = BigWorld.player()
        url = '/ty/md/moment/listForward?'
        m = {'roleid': p.gbId,
         'skey': p.pyq_skey,
         'momentId': momentId,
         'page': pageCount,
         'pageSize': const.PERSONAL_ZONE_MOMENT_COMMENT_NUM_PER_PAGE}
        params = urllib.urlencode(m)
        url += params
        commonRequest(callback, url)
    except:
        if callback:
            callback(1, {})
        return


def getForwardList(callback, momentId, pageCount):
    mgr = pyBgTask.getMgr()
    mgr.add_task(__getForwardList, (mgr.make_callback(callback), momentId, pageCount))


def __sendUserMoods(callback, imglist, moodText, topicId):
    try:
        p = BigWorld.player()
        url = '/ty/md/moment/add?'
        m = {'roleid': p.gbId,
         'skey': p.pyq_skey,
         'imglist': imglist,
         'text': moodText,
         'topicId': topicId}
        params = urllib.urlencode(m)
        url += params
        commonRequest(callback, url, mothedType='POST')
    except:
        if callback:
            callback(1, {})
        return


def sendUserMoods(callback, imglist, moodText, topicId):
    mgr = pyBgTask.getMgr()
    mgr.add_task(__sendUserMoods, (mgr.make_callback(callback),
     imglist,
     moodText,
     topicId))


def __getTopic(callback):
    try:
        p = BigWorld.player()
        url = '/ty/md/topic/list?'
        m = {'roleid': p.gbId,
         'skey': p.pyq_skey}
        params = urllib.urlencode(m)
        url += params
        commonRequest(callback, url)
    except:
        if callback:
            callback(1, {})
        return


def getTopic(callback):
    mgr = pyBgTask.getMgr()
    mgr.add_task(__getTopic, (mgr.make_callback(callback),))


def __likeMoments(callback, momentId, action):
    try:
        p = BigWorld.player()
        url = '/ty/md/moment/like?'
        m = {'roleid': p.gbId,
         'skey': p.pyq_skey,
         'id': momentId,
         'action': action}
        params = urllib.urlencode(m)
        url += params
        commonRequest(callback, url, mothedType='POST')
    except:
        if callback:
            callback(1, {})
        return


def likeMoments(callback, momentId, action):
    mgr = pyBgTask.getMgr()
    mgr.add_task(__likeMoments, (mgr.make_callback(callback), momentId, action))


def __delMoments(callback, momentId):
    try:
        p = BigWorld.player()
        url = '/ty/md/moment/del?'
        m = {'roleid': p.gbId,
         'skey': p.pyq_skey,
         'id': momentId}
        params = urllib.urlencode(m)
        url += params
        commonRequest(callback, url, mothedType='POST')
    except:
        if callback:
            callback(1, {})
        return


def delMoments(callback, momentId):
    mgr = pyBgTask.getMgr()
    mgr.add_task(__delMoments, (mgr.make_callback(callback), momentId))


def __forwardMoments(callback, momentId, text):
    try:
        p = BigWorld.player()
        url = '/ty/md/moment/forward?'
        m = {'roleid': p.gbId,
         'skey': p.pyq_skey,
         'id': momentId,
         'text': text}
        params = urllib.urlencode(m)
        url += params
        commonRequest(callback, url, mothedType='POST')
    except:
        if callback:
            callback(1, {})
        return


def forwardMoments(callback, momentId, text):
    mgr = pyBgTask.getMgr()
    mgr.add_task(__forwardMoments, (mgr.make_callback(callback), momentId, text))


def __addComment(callback, momentId, text, replyId, replyCommentId):
    try:
        p = BigWorld.player()
        url = '/ty/md/comment/add?'
        m = {'roleid': p.gbId,
         'skey': p.pyq_skey,
         'id': momentId,
         'text': text}
        if replyId:
            m['replyid'] = replyId
        if replyCommentId:
            m['replyCommentId'] = replyCommentId
        params = urllib.urlencode(m)
        url += params
        commonRequest(callback, url, mothedType='POST')
    except:
        if callback:
            callback(1, {})
        return


def addComment(callback, momentId, text, replyId, replyCommentId):
    mgr = pyBgTask.getMgr()
    mgr.add_task(__addComment, (mgr.make_callback(callback),
     momentId,
     text,
     replyId,
     replyCommentId))


def __delComment(callback, commentId):
    try:
        p = BigWorld.player()
        url = '/ty/md/comment/del?'
        m = {'roleid': p.gbId,
         'skey': p.pyq_skey,
         'id': commentId}
        params = urllib.urlencode(m)
        url += params
        commonRequest(callback, url, mothedType='POST')
    except:
        if callback:
            callback(1, {})
        return


def delComment(callback, commentId):
    mgr = pyBgTask.getMgr()
    mgr.add_task(__delComment, (mgr.make_callback(callback), commentId))


def __addFollow(callback, targetid):
    try:
        p = BigWorld.player()
        url = '/ty/md/follow/add?'
        m = {'roleid': p.gbId,
         'skey': p.pyq_skey,
         'targetid': targetid}
        params = urllib.urlencode(m)
        url += params
        commonRequest(callback, url, mothedType='POST')
    except:
        if callback:
            callback(1, {})
        return


def addFollow(callback, targetid):
    mgr = pyBgTask.getMgr()
    mgr.add_task(__addFollow, (mgr.make_callback(callback), targetid))


def __cancelFollow(callback, targetid):
    try:
        p = BigWorld.player()
        url = '/ty/md/follow/cancel?'
        m = {'roleid': p.gbId,
         'skey': p.pyq_skey,
         'targetid': targetid}
        params = urllib.urlencode(m)
        url += params
        commonRequest(callback, url, mothedType='POST')
    except:
        if callback:
            callback(1, {})
        return


def cancelFollow(callback, targetid):
    mgr = pyBgTask.getMgr()
    mgr.add_task(__cancelFollow, (mgr.make_callback(callback), targetid))


def getNewsList(callback, currentPage, pageSize):
    mgr = pyBgTask.getMgr()
    mgr.add_task(__getNewsList, (mgr.make_callback(callback), currentPage, pageSize))


def __getNewsList(callback, curentPage = 1, pageSize = 10):
    try:
        p = BigWorld.player()
        url = '/ty/md/inform/list?'
        m = {'roleid': p.gbId,
         'skey': p.pyq_skey,
         'pageSize': pageSize,
         'page': curentPage}
        params = urllib.urlencode(m)
        url += params
        commonRequest(callback, url)
    except:
        if callback:
            callback(1, {})
        return


def getFollowList(callback, currentPage, pageSize):
    mgr = pyBgTask.getMgr()
    mgr.add_task(__getFollowList, (mgr.make_callback(callback), currentPage, pageSize))


def __getFollowList(callback, curentPage = 1, pageSize = 10):
    try:
        p = BigWorld.player()
        url = '/ty/md/follow/list_follow_list?'
        m = {'roleid': p.gbId,
         'skey': p.pyq_skey,
         'pageSize': pageSize,
         'page': curentPage}
        params = urllib.urlencode(m)
        url += params
        commonRequest(callback, url)
    except:
        if callback:
            callback(1, {})
        return


def getVistorList(callback, currentPage, pageSize):
    mgr = pyBgTask.getMgr()
    mgr.add_task(__getVistorList, (mgr.make_callback(callback), currentPage, pageSize))


def __getVistorList(callback, curentPage = 1, pageSize = 10):
    try:
        p = BigWorld.player()
        url = '/ty/md/user/recent_visitors?'
        m = {'roleid': p.gbId,
         'skey': p.pyq_skey,
         'pageSize': pageSize,
         'page': curentPage}
        params = urllib.urlencode(m)
        url += params
        commonRequest(callback, url)
    except:
        if callback:
            callback(1, {})
        return
