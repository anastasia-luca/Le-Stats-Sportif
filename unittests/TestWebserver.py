import unittest
from app.data_ingestor import DataIngestor

class TestStringMethods(unittest.TestCase):
    '''
        Testing class for server's functions
    '''
    def setUp(self):
        self.data_ingestor = DataIngestor("./unittests/test.csv", None)

    def test_states_mean(self):
        question = 'Percent of adults aged 18 years and older who have obesity'
        result = self.data_ingestor.states_mean(question)
        expected_result = {"New Mexico": 27.7, "Ohio": 29.4, "Arkansas": 38.6, "Nebraska": 44.3}
        self.assertEqual(result, expected_result)

    def test_state_mean(self):
        question = 'Percent of adults aged 18 years and older who have an overweight classification'
        state = 'Ohio'
        result = result = self.data_ingestor.state_mean(question, state)
        expected_result = {"Ohio": 35.233333333333334}
        self.assertEqual(result, expected_result)

    def test_best5(self):
        question = 'Percent of adults who engage in muscle-strengthening activities on 2 or more days a week'
        result = result = self.data_ingestor.best5(question)
        expected_result = {"Washington": 40.3, "Vermont": 37.9, "New Hampshire": 35.3, "Massachusetts": 31.4, "Connecticut": 29.3}
        self.assertEqual(result, expected_result)

    def test_worst5(self):
        question = 'Percent of adults who engage in muscle-strengthening activities on 2 or more days a week'
        result = result = self.data_ingestor.worst5(question)
        expected_result = {"Rhode Island": 18.049999999999997, "Connecticut": 29.3, "Massachusetts": 31.4, "New Hampshire": 35.3, "Vermont": 37.9}
        self.assertEqual(result, expected_result)

    def test_global_mean(self):
        question = 'Percent of adults who engage in no leisure-time physical activity'
        result = self.data_ingestor.global_mean(question)
        expected_result = {"global_mean": 28.342857142857145}
        self.assertEqual(result, expected_result)

    def test_diff_from_mean(self):
        question = 'Percent of adults aged 18 years and older who have obesity'
        result = self.data_ingestor.diff_from_mean(question)
        expected_result = {'Arkansas': -2.8800000000000097, 'Nebraska': -8.580000000000005, 'New Mexico': 8.019999999999992, 'Ohio': 6.319999999999993}
        self.assertEqual(result, expected_result)

    def test_state_diff_from_mean(self):
        question = 'Percent of adults aged 18 years and older who have an overweight classification'
        state = 'Ohio'
        result = result = self.data_ingestor.state_diff_from_mean(question, state)
        expected_result = {"Ohio": -1.2333333333333343}
        self.assertEqual(result, expected_result)

    def test_mean_by_category(self):
        question = 'Percent of adults who engage in no leisure-time physical activity'
        result = self.data_ingestor.mean_by_category(question)
        expected_result = {"('Arizona', 'Race/Ethnicity', 'Non-Hispanic Black')": 25.6, "('Kansas', 'Age (years)', '45 - 54')": 28.7,
                            "('Maryland', 'Income', '$15,000 - $24,999')": 38.4, "('Nebraska', 'Age (years)', '18 - 24')": 18.6,
                            "('Nebraska', 'Income', '$15,000 - $24,999')": 31.5, "('Ohio', 'Race/Ethnicity', '2 or more races')": 31.6, "('Wisconsin', 'Age (years)', '55 - 64')": 24.0}
        self.assertEqual(result, expected_result)

    def test_state_mean_by_category(self):
        question = 'Percent of adults who engage in no leisure-time physical activity'
        state = 'Nebraska'
        result = self.data_ingestor.state_mean_by_category(question, state)
        expected_result = {"Nebraska" : {"('Age (years)', '18 - 24')": 18.6, "('Income', '$15,000 - $24,999')": 31.5}}
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
