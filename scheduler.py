from function import *


class Scheduler:
    upload = Upload()
    download = Download()

    def schedule(self, functions: [Function]):
        pass


class BruteForceScheduler(Scheduler):

    def __init__(self, functions: [Function]):
        self.functions = functions

    def schedule(self):
        providers = ["aws", "gcp"]
        result = []
        for function in self.functions:
            for input_provider in providers:
                for output_provider in providers:
                    for function_provider in providers:
                        for service_provider in providers:
                            rtt = function.estimate(input_provider, output_provider, function_provider, service_provider)
                            result.append({
                                "function_type": function.__class__.__name__,
                                "input": input_provider,
                                "output": output_provider,
                                "function": function_provider,
                                "service": service_provider,
                                "roundTripTime": rtt,
                            })
        return result
