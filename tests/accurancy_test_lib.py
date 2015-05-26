import os
import json

class Result:
    def __init__(self):
        self.sample_type_dic = {}

    def get_accurancy(self):
        total_predictions = 0.0
        true_predictions = 0.0

        for sample_type in self.sample_type_dic:
            predictions = self.sample_type_dic[sample_type]

            total_predictions = total_predictions + predictions['trues'] + predictions['falses']
            true_predictions = true_predictions + predictions['trues']

        return true_predictions / total_predictions

    def get_accurancy_for_type(self, sample_type):
        trues = self.sample_type_dic[sample_type]['trues']
        falses = self.sample_type_dic[sample_type]['falses']
        return trues / (trues + falses)

    def register_sample(self, sample_type, b_correct):
        if sample_type not in self.sample_type_dic:
            self.sample_type_dic[sample_type] = {'trues': 0.0, 'falses': 0.0}

        trues = self.sample_type_dic[sample_type]['trues']
        falses = self.sample_type_dic[sample_type]['falses']

        if b_correct:
            self.sample_type_dic[sample_type] = {'trues': trues + 1.0, 'falses': falses}
        else:
            self.sample_type_dic[sample_type] = {'trues': trues, 'falses': falses + 1.0}

    def save(self, file_path):
        file = open(file_path, 'w')
        file.write(json.dumps(self.sample_type_dic) + "\n")
        file.close()

    def load(self, file_path):
        file = open(file_path, 'r')
        self.sample_type_dic = json.loads(file.readline())
        file.close()

    def empty(self):
        self.sample_type_dic = {}


class AccurancyTest:
    def __init__(self, algorithm, sample_list, extensions):
        self.results = Result()
        self.algorithm = algorithm
        self.sample_list = sample_list
        self.extensions = extensions

    def run(self):
        self.results.empty()

        for index in range(len(self.sample_list)):
            self.__test_sample_type(index)

    def get_result(self):
        return self.results

    def __test_sample_type(self, index):
        sample_type = self.sample_list[index][0]

        for sample_dir_path in self.sample_list[index][1]:
            self.__test_directory(sample_dir_path, sample_type)

    def __test_directory(self, directory_path, sample_type):
        for file_name in os.listdir(directory_path):
            self.__test_sample(sample_type, os.path.join(directory_path, file_name))

    def __test_sample(self, sample_type, sample_path):
        if self.__is_file(sample_path):
            self.results.register_sample(sample_type, sample_type == self.algorithm(sample_path))

    def __is_file(self, file_path):
        file_name, file_extension = os.path.splitext(file_path)

        if file_extension in self.extensions:
            return True
        else:
            return False
