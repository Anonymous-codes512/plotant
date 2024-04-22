import os
import pandas as pd
import json
from django.http import JsonResponse
from project.general_operations import DataProcessor
import shutil
import zipfile

main_storage = "Storage"
user_storage = "Users_Storage"
trash = "Trash"


def create(email):
    main_folder = os.path.join(main_storage, user_storage)
    user = os.path.join(main_folder, email)
    
    os.makedirs(user)


# 4 functions
class ProjectProcessor:

    def create_project(self, email, projectname, file):
        main_folder = os.path.join(main_storage, user_storage)
        user_folder = os.path.join(main_folder, email)

        project_folder = os.path.join(user_folder, projectname)
        os.makedirs(project_folder)

        Previous = os.path.join(project_folder, 'Previous')
        os.makedirs(Previous)

        self.create_file(project_folder, file)
        
        return {'message':'Project Created Successfully.'}


    def create_file(self, project_folder, file):
        file_path = os.path.join(project_folder, file.name)

        with open(file_path, 'wb') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        return {'message':'Project file Uploaded.'}


    def list_projects(self, auth_token):
        user_folder = f'{main_storage}/{auth_token}'

        csv_files = []

        if os.path.exists(user_folder):
            for file in os.listdir(user_folder):
                if file.endswith('.csv'):
                    csv_files.append(file)

        return csv_files
    

    def count_projects(self, email):
        main_folder = os.path.join(main_storage, user_storage)

        user_folder = os.path.join(main_folder, email)
        count = os.listdir(user_folder)
        return len(count)


    def save_file(self, email, projectName, file):
        main_folder = os.path.join(main_storage, user_storage)
        user_folder = os.path.join(main_folder, email)
        project_folder = os.path.join(user_folder, projectName)

        if os.path.exists(project_folder):
            file_path = os.path.join(project_folder, file.name)
            if os.path.exists(project_folder):
                self.save_file_with_suffix(project_folder, file)
            else:
                with open(file_path, 'wb') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)
            
            
            return {'message':'Project file Uploaded.'}
        else:
            raise ValueError("No CSV files found in the project folder.")
    

    def save_file_with_suffix(self, project_folder, file):
        base_name, ext = os.path.splitext(file.name)
        matching_files = [f for f in os.listdir(project_folder) if os.path.splitext(f)[0] == base_name]
        counter = len(matching_files) + 1

        file_path = os.path.join(project_folder, file.name)

        while os.path.exists(file_path):
            new_name = f"{base_name}_{counter}{ext}"
            file_path = os.path.join(project_folder, new_name)
            counter += 1

        with open(file_path, 'wb') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        return file_path


    def delete_project(self, email, projectname):
        main_folder = os.path.join(main_storage, user_storage)
        user_folder = os.path.join(main_folder, email)
        project_folder = os.path.join(user_folder, projectname)
        trash_folder = os.path.join(main_storage, user_storage, trash)
        user_trash_folder = os.path.join(trash_folder, email)
        
        if os.path.exists(user_trash_folder):
            shutil.move(project_folder, user_trash_folder)
            return {'message': 'Project Moved to Trash Successfully.'}
        else:
            os.mkdir(user_trash_folder)
            shutil.move(project_folder, user_trash_folder)
            return {'message': 'Project Moved to Trash Successfully.'}

        
    def restore_project(self, email, projectname):
        main_folder = os.path.join(main_storage, user_storage)
        user_folder = os.path.join(main_folder, email)
        project_folder = os.path.join(user_folder, projectname)
        trash_folder = os.path.join(main_storage, user_storage, trash,email, projectname)

        if os.path.exists(trash_folder):
            shutil.move(trash_folder, project_folder)
            return {'message': 'Project Restored Successfully.'}
        else:
            return {'error': 'Project not found.'}


    def delete_file(self, email, projectname, filename):
        main_folder = os.path.join(main_storage, user_storage)
        user_folder = os.path.join(main_folder, email)
        project_folder = os.path.join(user_folder, projectname)
        file_path = os.path.join(project_folder, filename)

        if os.path.exists(file_path):
            os.remove(file_path)
            return {'message': 'File Deleted Successfully.'}
        else:
            return {'error': 'File not found.'}
        

    def rename_file(self, email, projectname, filename, newfilename):
        main_folder = os.path.join(main_storage, user_storage)
        user_folder = os.path.join(main_folder, email)
        project_folder = os.path.join(user_folder, projectname)
        file_path = os.path.join(project_folder, filename)
        new_file_path = os.path.join(project_folder, newfilename+'.csv')

        if os.path.exists(file_path):
            os.rename(file_path, new_file_path)
            return {'message': 'File Renamed Successfully.'}
        else:
            return {'error': 'File not found.'}


    def downloadFile(self, email, projectname):
        main_folder = os.path.join(main_storage, user_storage)
        user_folder = os.path.join(main_folder, email)
        project_folder = os.path.join(user_folder, projectname)

        archive_filename = f"{projectname}.zip" 
        archive_path = os.path.join(user_folder, archive_filename)

        with zipfile.ZipFile(archive_path, 'w') as zip_archive:
            for filename in os.listdir(project_folder):
                file_path = os.path.join(project_folder, filename)
                if os.path.isfile(file_path):
                    zip_archive.write(file_path, arcname=filename)
        return archive_path


    def delete_downloaded_file(self, file_path):

        if os.path.exists(file_path):
            os.remove(file_path)
            return True



# 4 functions
class FileProcessor:

    def save_file(self, filepath, data):
        data.to_csv(filepath, index=False)

    def update(self, data, col, row_no, value):
        data.loc[row_no, col] = value
        
    def delete_file(self, guest, filename):
        file_path = f'Storage\\Visitor_Storage\\{filename}'
        if os.path.exists(file_path):
            os.remove(file_path)
            message = f"File {filename}.csv has been deleted."
            json_msg = json.dumps(message)
            return json.loads(json_msg)
        else:
            message = f"File {filename} does not exist."
            json_msg = json.dumps(message)
            return json.loads(json_msg)

    def edit_val(self, col, row_no, value, guest):
        data = pd.read_csv(f'Storage\\Visitor_Storage\\{guest}')
        updated_data = self.update(data, col, row_no, value)
        updated_data.csv(f'Storage\\Visitor_Storage\\{guest}')



class DataProcessor:
    def __init__(self):
        self.file_path = None

    def get_column_names(self, data):
        column_names = []
        for column in data.columns:
            column_names.append(column)
        return json.dumps(column_names)

    def get_column_data(self, col, data):
        column_data = []
        for column in data[col]:
            column_data.append(column)
        return json.dumps(column_data)
    
    def get_column_data_unique(self, col, data):
        unique_values = data[col].unique().tolist()
        return json.dumps(unique_values)

    def get_column_unique_data(self, data):
        column_data_unique = {}
        for col in data.columns:
            unique_values = data[col].unique().tolist()
            column_data_unique[col] = unique_values
        return json.dumps(column_data_unique)

    def get_only_int_float_column_names(self, column_data):
        only_int_float_column_names = []
        for col, values in column_data.items():
            if all(isinstance(v, (int, float)) for v in values):
                only_int_float_column_names.append(col)
        return json.dumps(only_int_float_column_names)
    
    def get_sum_of_int_and_float_columns(self, data):
        int_float_columns = [col for col in data.columns if data[col].dtype in ('int64', 'float64')]
        sum_dict = {col: data[col].sum() for col in int_float_columns}
        json_sum_of_int_and_float_columns = json.dumps(sum_dict)
        return json_sum_of_int_and_float_columns

    def legends(self, x, y, z, data):
        flg = False
        unique_x_values = data[x].unique().tolist()
        y_values_with_respect_to_unique_x_values = []
        y_values_with_respect_to_unique_z_values = {}

        for product in unique_x_values:
            product_data = data[data[x] == product]
            if product_data[y].dtype != 'object':   
                product_quantity_sum = product_data[y].sum()
                y_values_with_respect_to_unique_x_values.append(round(float(product_quantity_sum),  1))
                
                z_grouped_data = product_data.groupby(z)[y].count().to_dict()
                y_values_with_respect_to_unique_z_values[product] = z_grouped_data
            else:
                flg = True
                y_counts = product_data[y].value_counts().to_dict()
                y_values_with_respect_to_unique_x_values.append(y_counts)

                z_grouped_data = product_data.groupby(z)[y].count().to_dict()
                y_values_with_respect_to_unique_z_values[product] = z_grouped_data

        if flg == True:
            final_list = []

            for entry in y_values_with_respect_to_unique_x_values:
                sum =  0
                for key, value in entry.items():
                    sum = sum + value
                final_list.append(sum)
            y_values_with_respect_to_unique_x_values = final_list

        return {'x': unique_x_values, 'y': y_values_with_respect_to_unique_x_values, 'z': y_values_with_respect_to_unique_z_values}

    def x_y_data(self, x, y, data):
        flg = False
        unique_x_values = data[x].unique().tolist()
        y_values_with_respect_to_unique_x_values = []

        for product in unique_x_values:
            product_data = data[data[x] == product]
            if product_data[y].dtype != 'object': 
                product_quantity_sum = product_data[y].sum()
                y_values_with_respect_to_unique_x_values.append(round(float(product_quantity_sum), 1))
            else:
                flg = True
                y_counts = product_data[y].value_counts().to_dict()
                y_values_with_respect_to_unique_x_values.append(y_counts)
        if flg == True:
            final_list = []

            for entry in y_values_with_respect_to_unique_x_values:
                sum = 0
                for key, value in entry.items():
                    sum = sum + value
                final_list.append(sum)
            y_values_with_respect_to_unique_x_values = final_list

        return {'x': unique_x_values, 'y': y_values_with_respect_to_unique_x_values}
  
    def open_file(self, email, project_name, file_name):
        # try:
            main_folder = os.path.join(main_storage, user_storage)
            user_folder = os.path.join(main_folder, email)
            project_folder = os.path.join(user_folder, project_name)
            file = os.path.join(project_folder, file_name)

            data = pd.read_csv(file)
            # has_nan = data.isnull().values.any()
            # locations = {'rows': [], 'cols': []}
            # corrupt_file = []

            # if has_nan:
            #     print("There are empty cells in the dataset.")
            #     nan_locations = pd.DataFrame(data.isnull(), columns=data.columns).stack()
            #     for idx in nan_locations[nan_locations].index:
            #         row_number, col_name = idx
            #         locations['rows'].append(row_number+1)
            #         locations['cols'].append(col_name.split(' ')[1])
            #     corrupt_file.append(True)
            #     print(f'some cells are empty try fill them or remove them locations are: {locations}')
            #     return {'flg':True, 'locations':f'some cells are empty try fill them or remove them locations are: {locations}'}
            # else:
            #     print("There are no empty cells in the dataset.")
            
                # with open(csv_file_path, 'wb') as destination:
                #     for chunk in file.chunks():
                #         destination.write(chunk)
            
            # data = pd.read_csv(csv_file_path)

            json_data = data.to_json(orient='records')
            parsed_json_data = json.loads(json_data)

            head = data.head(5)
            json_head = head.to_json(orient='records')
            parsed_json_head = json.loads(json_head)

            column_names = data.columns.tolist()
            column_data = {}
            for col in column_names:
                column_data[col] = data[col].tolist()

            column_dataJ = json.dumps(column_data)
           

            result_data = {
                'flg':False,
                'json_data': head,
                'head': data,
                'column_names': json.loads(self.get_column_names(data)),
                'column_data': json.loads(column_dataJ),
                'column_data_unique': json.loads(self.get_column_unique_data(data)),
                # 'sum': json.loads(self.get_sum_of_int_and_float_columns(data)),
                'type': json.loads(self.get_only_int_float_column_names(column_data)),
            }
            return result_data

    def get_labels(self, email, x, y, project_name, file_name):
        main_folder = os.path.join(main_storage, user_storage)
        user_folder = os.path.join(main_folder, email)
        project_folder = os.path.join(user_folder, project_name)
        file = os.path.join(project_folder, file_name)

        data = pd.read_csv(file)

        # int_columns = data.select_dtypes(include='int').columns
        # data[int_columns] = data[int_columns].astype(float)
        print(data)
        result = self.x_y_data(x, y, data)
        
        return json.dumps(result)
    
    def get_labels_legends(self,email, x, y, z, project_name, file_name):
        main_folder = os.path.join(main_storage, user_storage)
        user_folder = os.path.join(main_folder, email)
        project_folder = os.path.join(user_folder, project_name)
        file = os.path.join(project_folder, file_name)


        data = pd.read_csv(file)
        # data[int_columns] = data[int_columns].astype(float)
        result = self.legends(x, y, z, data)
        print(result)
        
        return json.dumps(result)
    

data_processor = DataProcessor()
class FileProcessor:
    def save_file(self, filepath, data):
        data.to_csv(filepath, index=False)

    def update(self, data, col, row_no, value):
        data.loc[row_no, col] = value
        return data
        
    # def delete_file(self, guest, filename):
    #     file_path = f'Storage\\Visitor_Storage\\{filename}'
    #     if os.path.exists(file_path):
    #         os.remove(file_path)
    #         message = f"File {filename}.csv has been deleted."
    #         json_msg = json.dumps(message)
    #         return json.loads(json_msg)
    #     else:
    #         message = f"File {filename} does not exist."
    #         json_msg = json.dumps(message)
    #         return json.loads(json_msg)
    def edit_val(self, col, row_no, value, guest, x, y):
        main_folder = os.path.join(main_storage, 'Visitor_Storage')
        print(main_folder, '\n\n')

        if os.path.exists(main_folder):
            for file in os.listdir(main_folder):
                if file == guest:
                    filepath = os.path.join(main_folder, file)
                    print(filepath, '\n\n')
                    filename_without_extension, _ = os.path.splitext(file)
                    data = pd.read_csv(filepath)

                    updated_data = self.update(data, col, row_no, value)

                    new_file_path = os.path.join(main_folder, f'{filename_without_extension}_updated.csv')
                    print(new_file_path, '\n\n')

                    updated_data.to_csv(new_file_path, index=False)

                    if os.path.exists(filepath):
                        os.remove(filepath)

                    os.rename(new_file_path, filepath)

                    labels = data_processor.get_labels(x, y, guest)

                    return labels


    



    







