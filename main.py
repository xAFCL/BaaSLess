import pandas as pd
from scheduler import *
from function import *

if __name__ == '__main__':
    # speech translator workflow
    functions = [
        Collect(),
        SpeechRecognition(input_size=3800, output_size=2.236, work_size=118000),
        Translate(input_size=2.236, output_size=1.785, work_size=2236),
        SpeechSynthesis(input_size=1.785, output_size=2800, work_size=1785),
        Merge(input_size=14000, output_size=14000, number_of_files=5)
    ]
    scheduler = BruteForceScheduler(functions)
    result = scheduler.schedule()
    pd.DataFrame(result).to_excel("result/speech-translator.xlsx")

    functions = [
        Split(input_size=654, output_size=650, number_of_pages=25),
        Extract(input_size=26, output_size=1.443),
        Translate(input_size=1.443, output_size=1.362, work_size=1443),
        SpeechSynthesis(input_size=1.362, output_size=2500, work_size=1362),
        Merge(input_size=62500, output_size=62300, number_of_files=25)
    ]
    scheduler = BruteForceScheduler(functions)
    result = scheduler.schedule()
    pd.DataFrame(result).to_excel("result/read-for-me.xlsx")

