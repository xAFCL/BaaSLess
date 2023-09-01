import pandas as pd


class Service:
    def estimate(self, work_size: int, function_provider: str, service_provider: str):
        """Estimate the service time of a cloud service."""
        pass


class Upload(Service):
    def estimate(self, file_size: int, function_provider: str, storage_provider: str, number_of_files: int = 1):
        """Estimate the download time of a cloud storage service."""
        parameters = pd.read_csv("parameters/storage.csv")
        row = parameters[
            (parameters["function"] == function_provider) & (parameters["service"] == storage_provider) & (
                    parameters["direction"] == "upload")]
        latency = row["latency"].values[0]
        bandwidth = row["bandwidth"].values[0]
        return number_of_files * latency + file_size / bandwidth


class Download(Service):
    def estimate(self, file_size: int, function_provider: str, storage_provider: str, number_of_files: int = 1):
        """Estimate the upload time of a cloud storage service."""
        parameters = pd.read_csv("parameters/storage.csv")
        row = parameters[(parameters["function"] == function_provider) & (parameters["service"] == storage_provider) & (
                parameters["direction"] == "download")]
        latency = row["latency"].values[0]
        bandwidth = row["bandwidth"].values[0]
        return number_of_files * latency + file_size / bandwidth


class SpeechToText(Service):
    def estimate(self, audio_length: int, function_provider: str, recognition_provider: str):
        """Estimate the service time of a speech recognition service."""
        parameters = pd.read_csv("parameters/speech-to-text.csv")
        row = parameters[
            (parameters["function"] == function_provider) & (parameters["service"] == recognition_provider)]
        latency = row["latency"].values[0]
        speed = row["speed"].values[0]
        return latency + audio_length / speed


class TextToSpeech(Service):
    def estimate(self, number_of_characters: int, function_provider: str, synthesis_provider: str):
        """Estimate the service time of a speech synthesis service."""
        parameters = pd.read_csv("parameters/text-to-speech.csv")
        row = parameters[
            (parameters["function"] == function_provider) & (parameters["service"] == synthesis_provider)]
        latency = row["latency"].values[0]
        speed = row["speed"].values[0]
        return latency + number_of_characters / speed
