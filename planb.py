import csv
import pandas as pd
import math
import os

path_root = r"D:\cyy\projects\member_invation_relation_calcuation"


class Member(object):
    def __init__(self, identifier, parent_id_c=''):
        self.identifier = identifier
        self.parent_id = parent_id_c
        self.info = {}
        self.record = {}
        self.son = {}  # {ID: Member, ID2: Member2}
        self.level = 1
        self.total_level = 1
        self.total_member = 1
        self.direct_member = 0

    def add_son(self, son):
        '''
        Add son member
        :param son: Member(object)
        :return:
        '''
        if type(son) != Member:
            raise TypeError("你要加子成员（Member)啊大哥")

        # if 45 == son.parent_id and son.identifier == 56:
        #     print(self.identifier)

        # print(self.identifier, son.identifier, son.parent_id)
        if self.identifier == 45 and son.identifier == 56:
            print(son.record)

        id_son = son.identifier
        parent_id_c = son.parent_id
        if parent_id_c == self.identifier:
            son.level = self.level + 1
            if id_son in self.son:
                # if 45 == son.parent_id and son.identifier == 56:
                #     print("Merging {} to {}".format(id_son, self.identifier))
                member_add = self.son[id_son].merge_member(son)
                self.total_member += member_add
                if self.son[id_son].total_level + 1 > self.total_level:
                    self.total_level = self.son[id_son].total_level + 1
                # print(member_add)
                self.direct_member = len(self.son)
                return member_add
            else:
                # if 45 == son.parent_id and son.identifier == 56:
                #     print("Add son {} to {}".format(id_son, self.identifier))
                self.son[id_son] = son
                self.total_member += son.total_member
                if son.total_level + 1 > self.total_level:
                    self.total_level = son.total_level + 1
                # print(son.total_member)
                self.direct_member = len(self.son)
                return son.total_member
        else:
            # if 45 == son.parent_id and son.identifier == 56:
            #     print("Searching son {} in {}".format(id_son, self.identifier))
            member_add = 0
            for id_son_self in self.son:
                son_self = self.son[id_son_self]
                member_add += son_self.add_son(son)
                if son_self.total_level + 1 > self.total_level:
                    self.total_level = son_self.total_level + 1

            self.total_member += member_add
            self.direct_member = len(self.son)
            return member_add

    def add_record(self, record_new):
        if record_new['order_id'] is not None:
            self.record[str(self.identifier) + 'order' + str(record_new['order_id'])] = record_new

    def get_record(self):
        # print(self.record)
        if len(self.record) > 0:
            return self.record.popitem()
        else:
            return None

    def update_info(self, info):
        if type(info) != dict:
            raise TypeError("用字典（dict）啊大哥！")

        self.info = info

    def merge_member(self, obj):
        '''

        :param obj: Member(object)
        :return:
        '''
        if type(obj) != Member:
            raise TypeError("你要合另一个成员（Member)啊大哥")

        if (obj.parent_id == '' or math.isnan(obj.parent_id)) and obj.identifier != self.identifier:
            return 0

        # if 45 == obj.parent_id and obj.identifier == 56:
        #     print(self.identifier)

        if obj.identifier == self.identifier:
            record_add = obj.record.copy()
            # print(record_add)
            while len(record_add) > 0:
                # print(record_add)
                # print('adding record for ', self.identifier)
                re_cord_name, record_new = record_add.popitem()  # obj.get_record()
                # print(record_new)
                self.add_record(record_new)

            # print('record added')
            son_add = obj.son.copy()
            member_add = 0
            while len(son_add) > 0:
                # print('adding son')
                id_son, son = son_add.popitem()
                member_add += self.add_son(son)

            self.total_member += member_add
            self.direct_member = len(self.son)
            return member_add
        else:
            member_add = self.add_son(obj)
            self.total_member += member_add
            self.direct_member = len(self.son)
            return member_add

    def get_son(self):
        if len(self.son) > 0:
            return self.son.popitem()
        else:
            return None, None

    # def generate_export_record(self, start_level):
    #     if self.level > start_level + 2:
    #         return None
    #
    #     list_export = self.record
    #     for record_id in list_export:
    #         list_export[record_id]['所在层级'] = self.level
    #         list_export[record_id]['下级总层数'] = self.total_level
    #         list_export[record_id]['下级总人数'] = self.total_member
    #         list_export[record_id]['直推人数'] = self.direct_member
    #
    #     # print(list_export)
    #     if self.level < start_level + 2:
    #         for id_son in self.son:
    #             list_export_son = self.son[id_son].generate_export_record(start_level)
    #             if list_export_son is not None:
    #                 list_export.update(list_export_son)
    #
    #     return list_export
    def generate_export_record(self, start_level):
        list_export = self.record
        for record_id in list_export:
            list_export[record_id]['所在层级'] = self.level
            list_export[record_id]['下级总层数'] = self.total_level
            list_export[record_id]['下级总人数'] = self.total_member
            list_export[record_id]['直推人数'] = len(self.son)

        for id_son in self.son:
            list_export_son = self.son[id_son].generate_export_record(start_level)
            if list_export_son is not None:
                list_export.update(list_export_son)

        # if self.identifier == 56 and self.parent_id == 45:
        #     print(list_export)

        return list_export


def calculate_level(args_a, args_b, args_c, args_d, args_e, args_f):
    if args_a.get(args_b) is None:
        return args_c, args_d, args_f

    if len(args_a[args_b]) == 0:
        return args_c, args_d, args_f

    args_d_current = args_d + 1

    if args_d_current > 3:
        return args_c, args_d, args_f

    args_c += len(args_a[args_b])
    # print("层数{}".format(args_d_current))
    # print("当前人数{}".format(args_c))
    # print(args_a[args_b])

    for sub_user_id in args_a[args_b]:
        # print(sub_user_id)
        if args_f.get(args_d_current) is None:
            args_f[args_d_current] = [args_e[sub_user_id]]
        else:
            args_f[args_d_current].append(args_e[sub_user_id])

    if args_d_current == 3:
        return args_c, args_d_current, args_f

    for user_id_search in args_a[args_b]:
        args_c, args_d_update, args_f = calculate_level(args_a, user_id_search, args_c, args_d_current, args_e, args_f)
        if args_d_update > args_d:
            args_d = args_d_update

    return args_c, args_d, args_f


def calculate_level_sim(args_a, args_b, args_c, args_d):
    if args_a.get(args_b) is None:
        return args_c, args_d

    if len(args_a[args_b]) == 0:
        return args_c, args_d

    args_d_current = args_d + 1

    if args_d_current > 3:
        return args_c, args_d

    args_c += len(args_a[args_b])
    # print("层数{}".format(args_d_current))
    # print("当前人数{}".format(args_c))

    if args_d_current == 3:
        return args_c, args_d_current

    for user_id_search in args_a[args_b]:
        args_c, args_d_update = calculate_level(args_a, user_id_search, args_c, args_d_current)
        if args_d_update > args_d:
            args_d = args_d_update

    return args_c, args_d


def generate_csv(list_user_f, file_f, user_id_f, level_f):
    level_f = level_f + 1
    print(level_f)
    if user_id_f not in list_user_f:
        return

    for sub_u_id in list_user_f[user_id_f].keys():
        for line_add in list_user_f[user_id_f][sub_u_id]:
            fp.writerow(line_add)
        if level_f < 3:
            generate_csv(list_user_f, file_f, sub_u_id, level_f)

    return


def planb():
    print('Loading CSV')
    path = '.\返利最新查询_new.csv'
    df = pd.read_csv(path, encoding="utf-8")
    count = df.__len__()
    # print("共{}行数据\r".format(count))
    rows = df.iterrows()

    # list_level = { }
    # list_user = { }
    # list_record = { } # list of relationships of subuser to parent user
    list_order = { }
    list_integral = { } # {ID: Member}

    # print('导入csv')
    for i, line in rows:
        order_id = line['order_id']
        line['用户ID'] = int(line['用户ID'])
        if line['上级ID'] != '' and not math.isnan(line['上级ID']):
            line['上级ID'] = int(line['上级ID'])
        else:
            line['上级ID'] = ''
            if line['用户ID'] == 56:
                print(line)

        if order_id in list_order:
            list_order[order_id].append(line)
        else:
            list_order[order_id] = [line]

    # print(list_order)
    print('CSV loaded')
    print('Generate member')

    for order_id in list_order:
        integral = {}
        # print(list_order[order_id])
        for line in list_order[order_id]:
            if line['上级ID'] == '' or math.isnan(line['上级ID']):
                top_id = line['用户ID']
                member_top = Member(top_id)
                member_top.add_record(line)
                integral['top'] = member_top
            else:
                user_id = line['用户ID']
                parent_id = line['上级ID']
                member_new = Member(user_id, parent_id)
                member_new.add_record(line)
                integral[user_id] = member_new

        # if 182460 in integral:
        #     print(integral[182460])
        #     print(integral[182460].parent_id)
        #     print(integral)

        integral_copy = {'top': integral.pop('top')}

        while len(integral) > 0:
            for user_id in integral:
                parent_id = integral[user_id].parent_id
                if parent_id not in integral:
                    # if 182460 == user_id:
                    #     print(integral[182460].record)
                    #     print(integral[182460].parent_id)
                    #     print(integral)
                    member_add = integral.pop(user_id)

                    # if 182460 == user_id:
                    #     print(member_add.record)
                    #     print(member_add.parent_id)

                    # print(integral)
                    # print(user_id)
                    for parent_id in integral_copy:
                        integral_copy[parent_id].add_son(member_add)
                        # if parent_id == 45 and member_add.identifier == 56:
                        #     print('right')

                    # print(user_id)
                    integral_copy[user_id] = member_add
                    # if 182460 == user_id:
                        # print(integral_copy[182460])
                    break

        integral = integral_copy
        # if 182460 in integral:
        #     print(len(integral))
        for parent_id in integral:

            member_top = integral[parent_id]
            # if 45 == member_top.parent_id and member_top.identifier == 56:
            #     print(member_top.record)
            top_id = member_top.identifier
            if top_id in list_integral:
                list_integral[top_id].merge_member(member_top)
            else:
                list_integral[top_id] = member_top

            # if 45 == member_top.parent_id and member_top.identifier == 56:
            #     print(member_top.record)

            # print('userid:', top_id, 'user level', member_top.level)

        # print('order ', order_id, ' finished')


    # print(list_integral)
    print('merging finished')

    for user_id in list_integral:
        integral = list_integral[user_id]
        # if user_id == 45:
        #     print(integral.son[56].record)
        #     print(integral.son)
        # if user_id == 29:
        #     print(integral.son[45].son[65].son[140144].record)
        #     print(integral.son)

        # print(integral.level)
        # print(integral)
        # print(integral.total_member, integral.total_level)
        # if user_id == 182460:
        #     print(integral.record)
        #     print(integral.parent_id)
        #     print(integral)
        print('Calculating level and member of user id {}......'.format(user_id))
        if integral.total_member >= 30 and integral.total_level >= 3:
            list_line_export = integral.generate_export_record(integral.level)
            # print(len(list_line_export))

            if list_line_export is not None and len(list_line_export) >= 30:
                print('Generate csv for {}'.format(user_id))
                path_new = path_root + r"\拆分结果\\" + r"\顶层ID_{}.csv".format(user_id)
                file = open(path_new, "w", newline='', encoding="utf-8")
                file.write('ID,用户ID,上级ID,order_id,姓名,级别,电话,获得返利,消费金额,订单号,返利比率,当前层级,下级总层数,下级总人数,直推人数\r\n')
                fp = csv.writer(file)
                for line_n in list_line_export:
                    line = list_line_export[line_n]
                    if int(line['用户ID']) == user_id:
                        line['上级ID'] = ''
                        # print(user_id)
                    if int(line['用户ID']) == 56 and user_id == 45:
                        print(line)
                    # line['下级总层数'] = integral.total_level
                    # line['下级总人数'] = integral.total_member
                    # line['直推人数'] = len(integral.son)
                    fp.writerow(line)
                #     count_level_inputted = 1
                #     count_sub_users_inputted = 0
                #     # print(list_sub_user)
                #     for level in range(count_level):
                #         if count_level_inputted <= 3 or count_sub_users_inputted < 30:
                #             for line in list_sub_user[level + 1]:
                #                 fp.writerow(line)
                #                 count_sub_users_inputted += 1
                #             count_level_inputted += 1
                #         else:
                #             break
                #
                file.close()

                # for dir_csv in os.listdir(os.path.join(path_root, "new2")):
                #     for path_csv in os.listdir(os.path.join(os.path.join(path_root, "new2"), dir_csv)):
                #         if os.path.isfile(path_csv) or os.path.isdir()

    # for i, line in rows:
    #     parent_id = line['上级ID']
    #     if math.isnan(parent_id):
    #         parent_id = ''
    #         line['上级ID'] = parent_id
    #     else:
    #         parent_id = int(parent_id)
    #         line['上级ID'] = parent_id
    #     user_id = line['用户ID']
    #     #print("导入上级ID{}".format(parent_id))
    #
    #     if user_id not in list_user:
    #         list_user[user_id] = line
    #
    #     if parent_id not in list_record:
    #         list_record[parent_id] = {user_id: []}
    #
    #     if user_id in list_record[parent_id]:
    #         list_record[parent_id][user_id].append(line)
    #     else:
    #         list_record[parent_id][user_id] = [line]  # example: {29:{45:[{记录1,,记录2}, 56:[]}, other:}
    #
    #     if parent_id != '':
    #         if parent_id not in list_level:
    #             list_level[parent_id] = {user_id}
    #             #print(parent_id)
    #         else:
    #             list_level[parent_id].add(user_id)
    #
    # print(list_level[92])
    # # print(list_user[45])
    # # print(list_level[45])
    # # print(29 in list_level[56] or 45 in list_level[56])
    # #
    # for user_id in list_level.keys():
    #     # print("计算用户ID{}层级".format(user_id))
    #     count_sub_users = len(list_level[user_id])
    #     # print("直推人数{}".format(count_sub_users))
    #     count_level = 1
    #     if list_user.get(user_id) is None:
    #         list_sub_user = {1: [{"", "", "" , "", ""}]}
    #     else:
    #         list_sub_user = {1: [list_user[user_id]]}
    #     count_sub_users, count_level, list_sub_user = calculate_level(list_level, user_id, count_sub_users, count_level, list_user, list_sub_user)
    #     # count_sub_users, count_level = calculate_level(list_level, user_id, count_sub_users, count_level)
    #     if count_sub_users >= 30 and count_level >= 3:
    #         path_new = os.path.join(path_root, "new2")
    #         if list_sub_user[1][0]["上级ID"] != '':
    #             path_new = path_new + r"\\" + str(list_sub_user[1][0]["上级ID"])
    #             if not os.path.isdir(path_new):
    #                 os.mkdir(path_new)
    #         path_new = path_new + r"\\" + r"\id_{}.csv".format(user_id)
    #         file = open(path_new, "w", newline='', encoding="utf-8")
    #         file.write('ID,用户ID,上级ID,order_id,姓名,级别,电话,获得返利,消费金额,订单号,返利比率\r\n')
    #         fp = csv.writer(file)
    #         level = 0
    #
    #         generate_csv(list_record, fp, user_id, level)
    #
    #
    #     #     if list_sub_user[1][0]["上级ID"] != '':
    #     #         path_new = path_new + r"\\" + str(list_sub_user[1][0]["上级ID"])
    #     #         if not os.path.isdir(path_new):
    #     #             os.mkdir(path_new)
    #     #     list_sub_user[1][0]["上级ID"] = ''
    #     #     path_new = path_new + r"\\" + r"\id_{}.csv".format(user_id)
    #     #     file = open(path_new, "w", newline='', encoding="utf-8")
    #     #     file.write('ID,用户ID,上级ID,order_id,姓名,级别,电话,获得返利,消费金额,订单号,返利比率\r\n')
    #     #     fp = csv.writer(file)
    #     #     count_level_inputted = 1
    #     #     count_sub_users_inputted = 0
    #     #     # print(list_sub_user)
    #     #     for level in range(count_level):
    #     #         if count_level_inputted <= 3 or count_sub_users_inputted < 30:
    #     #             for line in list_sub_user[level + 1]:
    #     #                 fp.writerow(line)
    #     #                 count_sub_users_inputted += 1
    #     #             count_level_inputted += 1
    #     #         else:
    #     #             break
    #     #
    #         file.close()
    #
    #     # for dir_csv in os.listdir(os.path.join(path_root, "new2")):
    #     #     for path_csv in os.listdir(os.path.join(os.path.join(path_root, "new2"), dir_csv)):
    #     #         if os.path.isfile(path_csv) or os.path.isdir()

if __name__ == '__main__':
    planb()
