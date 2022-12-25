import os
import re
import pandas as pd
from .myTime import Time
from enum import Enum


class Details(Enum):
    center = 'center'
    right = 'right'
    left = 'left'
    none = 'none'
    down = 'down'
    up = 'up'
    off = 'off'
    on = 'on'
    head = 'head'
    leg = 'leg'
    wing = 'wing'
    tail = 'tail'


class ClsMotion(object):

    def to_time(self, seconds):
        time = Time()
        minutes, time.second = divmod(seconds, 60)
        time.hour, time.minute = divmod(minutes, 60)
        return f'{time}'

    def process_frames(self, frames_path):
        # self.frames_path = frames_path
        frames = os.listdir(frames_path)
        dict_frame_time = {}
        for fileName in frames:
            frame_number = re.findall(r'\d+', fileName)
            frame_time = float(frame_number[0])
            dict_frame_time[frame_time] = self.get_pose(
                os.path.splitext(fileName)[0].replace(frame_number[0], ''))
        return self.get_motion_per_time(dict_frame_time)

    def process_vedio(self, vedio_path):
        frames = os.listdir(vedio_path)
        dict_frame_time = {}
        for fileName in frames:
            frame_number = re.findall(r'\d+', fileName)
            frame_time = float(frame_number[0])
            dict_frame_time[frame_time] = os.path.splitext(
                fileName)[0].replace(frame_number[0], '')
        self.get_motion_per_time(dict_frame_time)

    def get_motion_per_time(self, dict_frame_time):
        head = Details.head.value
        leg = Details.leg.value
        wing = Details.wing.value
        tail = Details.tail.value
        center = Details.center.value
        right = Details.right.value
        left = Details.left.value
        down = Details.down.value
        up = Details.up.value
        off = Details.off.value
        on = Details.on.value
        none = Details.none.value

        row = dict({"Time": 0, "No Motion": '', "No Motion Time Span": '',
                    'head status': '',      "head movement": '', "head movement time span": '',
                    'leg status': '',       "leg movement": '', "leg movement time span": '',
                    'wing status': '',      "wing movement": '', "wing movement time span": '',
                    'tail status': '',       "tail movement": '', "tail movement time span": ''})
        tbl_movement = []
        dict_pose_change = {head: False, leg: False, wing: False, tail: False}
        dict_pose_start_time = {head: 0.0, leg: 0.0, wing: 0.0, tail: 0.0}
        dict_pose_end_time = {head: 0.0, leg: 0.0, wing: 0.0, tail: 0.0}
        list_of_sorted_keys = list(sorted(dict_frame_time))
        for index, cur_time in enumerate(sorted(dict_frame_time)):
            if len(dict_frame_time) - index == 1:
                break
            else:
                # birds_curr, birds_next are the dicts representing the pose of the bird
                birds_pose_curr = dict_frame_time[cur_time]
                next_time = list_of_sorted_keys[index + 1]
                birds_pose_next = dict_frame_time[next_time]

                # if there is a diff create a new obj that contain a time
                diff = self.get_difference(birds_pose_curr, birds_pose_next)

                if diff is not None:
                    # new_row = None

                    for birdPart in diff.keys():
                        if not dict_pose_change[birdPart]:
                            # first move so record the start time
                            dict_pose_start_time[birdPart] = next_time
                            dict_pose_change[birdPart] = True
                        else:
                            # Dict = dict({1: 'Geeks', 2: 'For', 3: 'Geeks'})
                            # https://www.geeksforgeeks.org/python-dictionary/
                            # if this the second move for the same part then record the end time
                            # and caculate the time interval of the move
                            dict_pose_end_time[birdPart] = next_time
                        
                            temp = Time()
                            delta = temp.subtract_time(Time(second=int(dict_pose_end_time[birdPart])), Time(
                                second=int(dict_pose_start_time[birdPart])))
                            new_row = row.copy()
                            t = next_time/30
                            new_row['Time'] = f'{int(t//60)}:{t%60:.2f}'
                            new_row[f"{str(birdPart)} status"] = f"{diff[birdPart]}"
                            new_row[f"{str(birdPart)} movement"] = f"{birds_pose_curr[birdPart]}-{diff[birdPart]}"
                            new_row[f"{str(birdPart)} movement time span"] = int(
                                dict_pose_end_time[birdPart])-int(dict_pose_start_time[birdPart])
                        

                            if (len(tbl_movement) != 0 and tbl_movement[len(tbl_movement)-1]['Time'] == new_row['Time']):
                                if tbl_movement[len(tbl_movement)-1]['head movement'] == '' and new_row['head movement'] != '':
                                    tbl_movement[len( tbl_movement)-1]['head movement'] = new_row['head movement']
                                    tbl_movement[len( tbl_movement)-1]['head movement time span'] = new_row['head movement time span']
                                    tbl_movement[len( tbl_movement)-1]['head status'] = new_row['head status']
                                
                                if tbl_movement[len(tbl_movement)-1]['leg movement'] == '' and new_row['leg movement'] != '':
                                    tbl_movement[len(tbl_movement)-1]['leg movement'] = new_row['leg movement']
                                    tbl_movement[len(tbl_movement)-1]['leg movement time span'] = new_row['leg movement time span']
                                    tbl_movement[len( tbl_movement)-1]['leg status'] = new_row['leg status']

                                if tbl_movement[len(tbl_movement)-1]['wing movement'] == '' and new_row['wing movement'] != '':
                                    tbl_movement[len(tbl_movement)-1]['wing movement'] = new_row['wing movement']
                                    tbl_movement[len(tbl_movement)-1]['wing movement time span'] = new_row['wing movement time span']
                                    tbl_movement[len(tbl_movement)-1]['wing status'] = new_row['wing status']

                                if tbl_movement[len(tbl_movement)-1]['tail movement'] == '' and new_row['tail movement'] != '':
                                    tbl_movement[len(tbl_movement)-1]['tail movement'] = new_row['tail movement']
                                    tbl_movement[len(tbl_movement)-1]['tail movement time span'] = new_row['tail movement time span']
                                    tbl_movement[len( tbl_movement)-1]['tail status'] = new_row['tail status']
                                       
                               

                            else:
                                tbl_movement.append(new_row)

                            dict_pose_start_time[birdPart] = next_time

                 

        return self.data_frame(dict_frame_time, tbl_movement)

    def get_difference(self, first_dict, second_dict):
        try:
            first_dict = set(first_dict.items())
            second_dict = set(second_dict.items())
            return dict(second_dict - first_dict)
        except:
            return None

    def get_pose(self, file_name):

        head = Details.head.value
        leg = Details.leg.value
        wing = Details.wing.value
        tail = Details.tail.value
        center = Details.center.value
        right = Details.right.value
        left = Details.left.value
        down = Details.down.value
        up = Details.up.value
        off = Details.off.value
        on = Details.on.value
        none = Details.none.value
        # if we take just one name
        try:
            file_name_trimmed = file_name.replace(
                '.', ':').replace('_', ',').lower()
            file_name_trimmed = ('{%s}' % file_name_trimmed)
            file_name_trimmed = eval(file_name_trimmed)
            return file_name_trimmed
        except:
            pass
            # print(file_name_trimmed)

    def data_frame(self, file_name, change):
        head = Details.head.value
        leg = Details.leg.value
        wing = Details.wing.value
        tail = Details.tail.value
        center = Details.center.value
        right = Details.right.value
        left = Details.left.value
        down = Details.down.value
        up = Details.up.value
        off = Details.off.value
        on = Details.on.value
        none = Details.none.value
        # if we take a list i.e. [{head:right, leg:up, tail:left, wing:on}]
        # convert the input string into the above format
        # list_of_sorted_keys = list(sorted(file_name))
        # print(change)
        # convert dict to dataframe
        df = pd.DataFrame.from_dict(change, orient='columns')
        # print(len(list_of_sorted_keys))
        # time = pd.Series(list_of_sorted_keys)
        export_details = pd.DataFrame(change).set_index("Time")
        export_ready_dataframe = export_details.groupby(
            by="Time", dropna=False).max()
        # print(export_ready_dataframe)
        # export_ready_dataframe["change"] = pd.Series(change)
        export_details.columns = ["No Motion", "No Motion\n Time Span (sec)",
                                  'head status', "head movement", "head movement\n time span",
                                  'leg status',  "leg movement", "leg movement\n  time span",
                                  'wing status',   "wing movement", "wing movement\n  time span",
                                  'tail status',    "tail movement", "tail movement\n  time span"]
        # export_details.to_excel(
        #     excel_writer=self.sheetPath, sheet_name="Details")
        return export_details
        # export_ready_dataframe.to_excel(excel_writer=self.sheetPath, sheet_name="totals")


if __name__ == '__main__':
    # sheet path, frames path
    ob = ClsMotion(r"C:\Users\rhaze\Downloads\xd\test.xlsx")
    ob.process_frames(
        r"C:\Users\rhaze\Desktop\Projects\ProjectETL\frames")
    # time_string = time.strftime("%H:%M:%S", named_tuple)

    # print(time_string)
