from service import *


class Function:
    overhead_time = {
        "aws": 825.4,
        "gcp": 233.1
    }
    upload = Upload()
    download = Download()
    s2t = SpeechToText()
    t2s = TextToSpeech()

    def estimate(self, input_provider: str, output_provider: str, function_provider: str, service_provider: str):
        """Estimate the round trip time of a serverless function."""
        pass


class SpeechRecognition(Function):
    computation_time = {
        "aws": 0,
        "gcp": 0
    }

    def __init__(self, input_size: float, output_size: float, work_size: float):
        self.input_size = input_size
        self.output_size = output_size
        self.work_size = work_size

    def estimate(self, input_provider: str, output_provider: str, function_provider: str, recognition_provider: str):
        """Estimate the round trip time of a speech recognition function."""
        s2t = self.s2t.estimate(self.work_size, function_provider, recognition_provider)
        ut = self.upload.estimate(self.output_size, function_provider, output_provider)
        ct = self.computation_time[function_provider]
        o = self.overhead_time[function_provider]
        mv = None
        if recognition_provider == input_provider:
            # S2T + UT + CT + O
            mv = 0
        elif recognition_provider == "gcp" and input_provider == "aws":
            # DT + S2T + UT + CT + O
            mv = self.download.estimate(self.input_size, function_provider, input_provider)
        elif recognition_provider == "aws" and input_provider == "gcp":
            # DT + UT + S2T + UT + CT + O
            mv = self.download.estimate(self.input_size, function_provider, input_provider) + \
                 self.upload.estimate(self.input_size, function_provider, recognition_provider)
        return mv + s2t + ut + ct + o


class SpeechSynthesis(Function):
    computation_time = {
        "aws": 56.1,
        "gcp": 69.9
    }

    def __init__(self, input_size: float, output_size: float, work_size: float):
        self.input_size = input_size
        self.output_size = output_size
        self.work_size = work_size

    def estimate(self, input_provider: str, output_provider: str, function_provider: str, synthesis_provider: str):
        """Estimate the round trip time of a speech synthesis function."""
        dt = self.download.estimate(self.input_size, function_provider, input_provider)
        t2s = self.t2s.estimate(self.work_size, function_provider, synthesis_provider)
        ut = self.upload.estimate(self.output_size, function_provider, output_provider)
        ct = self.computation_time[function_provider]
        o = self.overhead_time[function_provider]
        return dt + t2s + ut + ct + o


class Translate(Function):
    computation_time = {
        "aws": 0,
        "gcp": 0
    }

    def __init__(self, input_size: float, output_size: float, work_size: float):
        self.input_size = input_size
        self.output_size = output_size
        self.work_size = work_size

    def estimate(self, input_provider: str, output_provider: str, function_provider: str, translate_provider: str):
        """Estimate the round trip time of a translation function."""
        dt = self.download.estimate(self.input_size, function_provider, input_provider)
        tra = 0
        # speech translator workflow
        if self.work_size == 2236:
            if function_provider == "aws" and translate_provider == "aws":
                tra = 175
            elif function_provider == "aws" and translate_provider == "gcp":
                tra = 275
            elif function_provider == "gcp" and translate_provider == "aws":
                tra = 169
            elif function_provider == "gcp" and translate_provider == "gcp":
                tra = 404
        # read for me workflow
        elif self.work_size == 1443:
            if function_provider == "aws" and translate_provider == "aws":
                tra = 187.3
            elif function_provider == "aws" and translate_provider == "gcp":
                tra = 277.3
            elif function_provider == "gcp" and translate_provider == "aws":
                tra = 207.5
            elif function_provider == "gcp" and translate_provider == "gcp":
                tra = 322.7
        ut = self.upload.estimate(self.output_size, function_provider, output_provider)
        ct = self.computation_time[function_provider]
        o = self.overhead_time[function_provider]
        return dt + tra + ut + ct + o


class Collect(Function):
    computation_time = {
        "aws": 0,
        "gcp": 0
    }

    def estimate(self, input_provider: str, output_provider: str, function_provider: str, service_provider: str):
        """Estimate the round trip time of a collect function."""
        col = 0
        if function_provider == "aws" and input_provider == "aws":
            col = 267.2
        elif function_provider == "aws" and input_provider == "gcp":
            col = 162.6
        elif function_provider == "gcp" and input_provider == "aws":
            col = 287.9
        elif function_provider == "gcp" and input_provider == "gcp":
            col = 99.2
        ct = self.computation_time[function_provider]
        o = self.overhead_time[function_provider]
        return col + ct + o


class Merge(Function):
    computation_time = {
        "aws": 20,
        "gcp": 20
    }

    def __init__(self, input_size: float, output_size: float, number_of_files: int):
        self.input_size = input_size
        self.output_size = output_size
        self.number_of_files = number_of_files

    def estimate(self, input_provider: str, output_provider: str, function_provider: str, service_provider: str):
        """Estimate the round trip time of a collect function."""
        dt = self.download.estimate(self.input_size, function_provider, input_provider, self.number_of_files)
        ct = self.computation_time[function_provider]
        ut = self.upload.estimate(self.output_size, function_provider, output_provider)
        o = self.overhead_time[function_provider]
        return dt + ct + ut + o


class Split(Function):
    computation_time = {
        "aws": 287.6,
        "gcp": 208
    }

    def __init__(self, input_size: float, output_size: float, number_of_pages: int):
        self.input_size = input_size
        self.output_size = output_size
        self.number_of_pages = number_of_pages

    def estimate(self, input_provider: str, output_provider: str, function_provider: str, service_provider: str):
        """Estimate the round trip time of a split function."""
        dt = self.download.estimate(self.input_size, function_provider, input_provider)
        ct = self.computation_time[function_provider]
        ut = self.upload.estimate(self.output_size, function_provider, output_provider, self.number_of_pages)
        o = self.overhead_time[function_provider]
        return dt + ct + ut + o


class Extract(Function):
    computation_time = {
        "aws": 0,
        "gcp": 0
    }

    def __init__(self, input_size: float, output_size: float):
        self.input_size = input_size
        self.output_size = output_size

    def estimate(self, input_provider: str, output_provider: str, function_provider: str, extract_provider: str):
        """Estimate the round trip time of an extract function."""
        dt = self.download.estimate(self.input_size, function_provider, input_provider)
        ext = 0
        if function_provider == "aws" and extract_provider == "aws":
            ext = 2122.5
        elif function_provider == "aws" and extract_provider == "gcp":
            ext = 1246.6
        elif function_provider == "gcp" and extract_provider == "aws":
            ext = 2567.6
        elif function_provider == "gcp" and extract_provider == "gcp":
            ext = 1008.3
        ut = self.upload.estimate(self.output_size, function_provider, output_provider)
        ct = self.computation_time[function_provider]
        o = self.overhead_time[function_provider]
        return dt + ext + ut + ct + o
