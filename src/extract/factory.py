class ExtracterFactory:
    def get_extracter(self, source_type):
        if source_type == 'csv':
            from .csv_extracter import CSVExtractor
            return CSVExtractor()
        elif source_type == 'api':
            from .api_extracter import APIExtracter
            return APIExtracter()
        else:
            raise ValueError('Unknown Source Type')