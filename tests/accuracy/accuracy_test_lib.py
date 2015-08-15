import os
import json


class Result(object):

    def __init__(self):
        """Creates a new result object.
        """
        self.sample_type_dic = {}

    def get_accuracy(self):
        """Counts the accuracy from the test results for all the samples.

        :returns: Accuracy for all the samples of the test.
        """
        total_predictions = 0.0
        true_predictions = 0.0

        for sample_type in self.sample_type_dic:
            predictions = self.sample_type_dic[sample_type]

            total_predictions += predictions['trues'] + predictions['falses']
            true_predictions += predictions['trues']

        return true_predictions / total_predictions

    def get_accuracy_for_type(self, sample_type):
        """Counts the accuracy for given sample type.

        :param sample_type: Type of the sample which accuracy should be
                            calculated for.
        :returns: Accuracy for the given sample type.
        """
        trues = self.sample_type_dic[sample_type]['trues']
        falses = self.sample_type_dic[sample_type]['falses']
        return trues / (trues + falses)

    def register_sample(self, sample_type, b_correct):
        """Registers sample to the result. This should be only used by the test
        it self.

        :param sample_type: Type of the sample that is registered.
        :param b_correct: Indicates whether the algorithm which was tested
                            a gave correct prediction for the sample.
        :type b_correct: bool
        """
        if sample_type not in self.sample_type_dic:
            self.sample_type_dic[sample_type] = {'trues': 0.0, 'falses': 0.0}

        if b_correct:
            self.sample_type_dic[sample_type]['trues'] += 1
        else:
            self.sample_type_dic[sample_type]['falses'] += 1

    def save(self, file_path):
        """Saves this result into a file. Path to the file in which the result will
        be saved is given as a parameter. If path for the file doesn't exist it
        will automatically be created. Also if the given file path is a file,
        the old file will be overwritten.

        :param file_path: Path to the file where result will be saved.
        """
        with open(file_path, 'w') as outfile:
            outfile.write(json.dumps(self.sample_type_dic) + "\n")

    def load(self, file_path):
        """Loads results from the file which file path is given to this result.

        :param file_path: Path to the file where result should be loaded.

        ..warning::
        When result is loaded from a file current result information of result
        object which loads the result from the file is lost.
        """
        with open(file_path, 'r') as infile:
            self.sample_type_dic = json.loads(infile.readline())

    def empty(self):
        """Empties this result.
        """
        self.sample_type_dic = {}


class AccuracyTest(object):

    def __init__(self, algorithm, sample_list, extensions):
        """Creates new accuracy test.
        """
        self.results = Result()
        self.algorithm = algorithm
        self.sample_list = sample_list
        self.extensions = extensions

    def run(self):
        self.results.empty()

        for index, _ in enumerate(self.sample_list):
            self.__test_sample_type(index)

    def get_result(self):
        return self.results

    def __test_sample_type(self, index):
        sample_type = self.sample_list[index][0]

        for sample_dir_path in self.sample_list[index][1]:
            self.__test_directory(sample_dir_path, sample_type)

    def __test_directory(self, directory_path, sample_type):
        for file_name in os.listdir(directory_path):
            self.__test_sample(sample_type,
                               os.path.join(directory_path, file_name))

    def __test_sample(self, sample_type, sample_path):
        if self.__is_file(sample_path):
            self.results.register_sample(sample_type,
                    sample_type == self.algorithm(sample_path))

    def __is_file(self, file_path):
        file_name, file_extension = os.path.splitext(file_path)
        return file_extension in self.extensions
