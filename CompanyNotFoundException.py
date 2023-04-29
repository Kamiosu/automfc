
class CompanyNotFoundException(Exception): 
    def __init__(self, company):
        self.company = company
        super().__init__(f"Company {company} not found in database")