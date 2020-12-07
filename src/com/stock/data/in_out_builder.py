from src.com.stock.common.import_lib import *
from src.com.stock.common import import_lib  as com_vari



class InOutBuilder:
    def __init__(self, tr_name , path_to_tr_file):

        print("tr 명  " + tr_name+"    in_out_builder 생성   tr file 경로   " + path_to_tr_file)

        self.tr_name = tr_name
        self.path_to_tr_file = path_to_tr_file

        self.tr_structure = pd.read_excel(path_to_tr_file, sheet_name = self.tr_name)

        self.single_input = self.tr_structure["SINGLE_INPUT"].dropna()
        self.multi_input = self.tr_structure["MULTI_INPUT"].dropna()
        self.single_output = self.tr_structure["SINGLE_OUTPUT"].dropna()
        self.multi_output = self.tr_structure["MULTI_OUTPUT"].dropna()
        self.single_check = self.tr_structure["SINGLE_CHECK"].dropna().astype(bool)
        self.multi_check = self.tr_structure["MULTI_CHECK"].dropna().astype(bool)
        self.pk_output = self.tr_structure["PK_OUTPUT"].dropna()

        self.input_data_list = []
        self.input_dict = {}
        self.input_dict_list = []

        self.pk_dict = {}

    def set_input_list(self, input_data_list ):
        self.input_data_list = input_data_list
        print(self.input_data_list)
        self.input_data_iter = iter(self.input_data_list)

    def get_input_dict_list(self):
        #input_data_list 는 2차원 배열
        print("tr 명   " + self.tr_name + "  의  인풋 dictionary list를 세팅 합니다   "  )
        print("tr 명   " + self.tr_name + "  의  인풋 명  " )
        print(self.single_input)

        for input_data in self.input_data_list:
            input_dict = {}
            for index , value in enumerate(input_data):
                print(self.single_input[index] + "   " + value)
                self.input_dict[index] = value
            self.input_dict_list.append(copy(input_dict))
        return self.input_dict_list

    def get_intput_dict(self):
        #input_data_list 는 2차원 배열
        print("tr 명   " + self.tr_name + "  의  인풋 dictionary list를 세팅 합니다   "  )
        print("tr 명   " + self.tr_name + "  의  인풋 명  " )
        print(self.single_input)

        try:
            self.input_data = []
            self.input_dict = {}
            self.input_data = next(self.input_data_iter)
            for key , value in self.single_input.items():
                print(key)
                print( self.input_data[key])
                self.input_dict[key] = self.input_data[key]
            return self.input_dict
        except StopIteration :
            return None

    def get_pk_dict(self):
        for index , value in enumerate(self.single_input):
            print(self.pk_output)
            if value in self.pk_output.values:
                self.pk_dict[value] = self.input_dict[index]
        return self.pk_dict

    def get_single_output_dict(self):
        single_output_dict = {}
        single_output = self.single_output[self.single_check]
        for key, value in single_output.items():
            single_output_dict[key] = value.strip()
        return single_output_dict

    def get_multi_output_dict(self):
        multi_output_dict = {}
        multi_output = self.multi_output[self.multi_check]
        for key, value in multi_output.items():
            multi_output_dict[key] = value.strip()
        return multi_output_dict






if __name__ ==  "__main__":
    test_vari = InOutBuilder("TR_1206", "C:\dev\OpenStock\src\com\stock\\tr_data\Indi_TR.xlsx")
