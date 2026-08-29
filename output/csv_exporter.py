import pandas as pd

class CsvExporter:
    def export(
        self,
        results,
        output_file
    ):
        df = pd.DataFrame(results)
        df.to_csv(
            output_file,
            index=False
        )