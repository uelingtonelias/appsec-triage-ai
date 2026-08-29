class DataflowAnalyzer:
    def analyze(self, finding):
        return {
            "source": finding.source,
            "sink": finding.sink,
            "flow": finding.dataflow
        }