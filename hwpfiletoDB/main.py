#! /usr/bin/python3
#-*- coding:utf-8 -*-
import logging
import sys
import pymysql

def GetLogger(filename):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(fmt='[%(levelname)s] %(asctime)s || %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    file_handler = logging.FileHandler(filename)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger

def ConnectDB():
    logging.debug('ConnectDB')
    try:
        # conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='root', db='test', charset='utf8')
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='kait', password='isms0313#$', db='kait', charset='utf8')
        return conn

    except Exception as e:
        logging.info('ConnectDB_Error')
        logging.debug(e)
        sys.exit()

def GetFilePath(cur, exam_seq, ti_seq, report_type):
    try:
        logging.debug("Get filepath")
        sql = "SELECT CONCAT(file_path, save_file) FROM exam_report_file WHERE exam_seq=" + exam_seq + " AND ti_seq=" + ti_seq + " AND report_type='" + report_type + "';"
        logging.debug('sql: {}'.format(sql))
        cur.execute(sql)
        filepath = cur.fetchone()[0]
        logging.debug('filepath : {}'.format(filepath))
        return filepath
    except Exception as e:
        print("F")
        logging.debug("GetFilePath_Error")
        logging.debug(e)
        sql = "UPDATE exam_report_file SET exp_excute_state='F', exp_excute_log='파일경로획득실패(GetFilePath_Error)', exp_excute_date=NOW() " \
              "WHERE exam_seq=" + exam_seq + " AND ti_seq=" + ti_seq + " AND report_type='" + report_type + "';"
        logging.debug('sql: {}'.format(sql))
        cur.execute(sql)
        sys.exit()

def GetHwpText(filename):
    import olefile
    import zlib
    import struct

    f = olefile.OleFileIO(filename)
    dirs = f.listdir()

    # 문서 포맷 압축 여부 확인
    header = f.openstream("FileHeader")
    header_data = header.read()
    is_compressed = (header_data[36] & 1) == 1

    # Body Sections 불러오기
    nums = []
    for d in dirs:
        if d[0] == "BodyText":
            nums.append(int(d[1][len("Section"):]))
    sections = ["BodyText/Section" + str(x) for x in sorted(nums)]

    # 전체 text 추출
    text = ""
    for section in sections:
        bodytext = f.openstream(section)
        data = bodytext.read()
        if is_compressed:
            unpacked_data = zlib.decompress(data, -15)
        else:
            unpacked_data = data

        # 각 Section 내 text 추출
        section_text = ""
        i = 0
        size = len(unpacked_data)
        while i < size:
            header = struct.unpack_from("<I", unpacked_data, i)[0]
            rec_type = header & 0x3ff
            rec_len = (header >> 20) & 0xfff

            if rec_type in [67]:
                rec_data = unpacked_data[i + 4:i + 4 + rec_len]
                section_text += rec_data.decode('utf-16')
                section_text += "\n"

            i += 4 + rec_len

        text += section_text
        text += "\n"

    # 누름틀 내 텍스트 가져오기
    start = '\x03汫╣\x00\x00\x00\x00\x03'
    end = '\x04汫ॣ\x01\x00\x00\x00\x04'
    arr = []
    while True:
        try:
            start_idx = text.index(start)
            end_idx = text.index(end)
            arr.append(text[start_idx + len(start):end_idx])
            text = text[end_idx + len(end):]
        except ValueError:
            break
    logging.debug("arr: {}".format(arr))
    return arr

def main():
    # logging 세팅
    logger = GetLogger('./log.txt')

    # db 연결
    conn = ConnectDB()
    cur = conn.cursor()

    # filepath 얻기
    exam_seq, ti_seq, report_type = sys.argv[1], sys.argv[2], sys.argv[3]
    filepath = GetFilePath(cur, exam_seq, ti_seq, report_type)

    # 누름틀 내 텍스트 받아오기 --> arr
    arr = GetHwpText(filepath)
    sql = ""

    # report_type 분류
    sql += "UPDATE exam_report_file SET "
    if report_type == '1':      # 결함조치보고서
        logging.debug("report_type == 1, start")
        try:
            while len(arr) < 2:
                arr.append('NULL')
            sql += "exp_error_text='" + arr[0] + "', "
            for i in range(1, len(arr)):
                if i % 2 == 1:
                    sql += "exp_table_tite" + str((i+1)//2) + "='" + arr[i] + "', "
                else:
                    sql += "exp_table_text" + str(i//2) + "='" + arr[i] + "', "
            sql += "exp_excute_state='S', "
            sql += "exp_excute_log='정상', "
            sql += "exp_excute_date=NOW() "
            sql += "WHERE exam_seq=" + exam_seq + " AND ti_seq=" + ti_seq + " AND report_type='" + report_type + "';"
            logging.debug("sql: {}".format(sql))
            cur.execute(sql)
        except Exception as e:
            print("F")
            logging.debug("WritingReport_Error")
            logging.debug(e)
            sql = "UPDATE exam_report_file SET exp_excute_state='F', exp_excute_log='파일서식에러(에러로그확인필요)', exp_excute_date=NOW() " \
                  "WHERE exam_seq=" + exam_seq + " AND ti_seq=" + ti_seq + " AND report_type='" + report_type + "';"
            logging.debug('sql: {}'.format(sql))
            cur.execute(sql)
    elif report_type == '2':    # 보완조치내역서
        logging.debug("report_type == 2, start")
        try:
            sql += "exp_action_text='" + arr[0] + "', "
            sql += "exp_prevention_text='" + arr[1] + "', "
            sql += "exp_excute_state='S', "
            sql += "exp_excute_log='정상', "
            sql += "exp_excute_date=NOW() "
            sql += "WHERE exam_seq=" + exam_seq + " AND ti_seq=" + ti_seq + " AND report_type='" + report_type + "';"
            logging.debug("sql: {}".format(sql))
            cur.execute(sql)
        except Exception as e:
            print("F")
            logging.debug("WritingReport_Error")
            logging.debug(e)
            sql = "UPDATE exam_report_file SET exp_excute_state='F', exp_excute_log='파일서식에러(에러로그확인필요)', exp_excute_date=NOW() " \
                  "WHERE exam_seq=" + exam_seq + " AND ti_seq=" + ti_seq + " AND report_type='" + report_type + "';"
            logging.debug('sql: {}'.format(sql))
            cur.execute(sql)

    logging.debug(sql)

    # db 연결 해제
    conn.commit()
    conn.close()

    # 종료
    print("S")
    sys.exit()


if __name__ == "__main__":
    main()















