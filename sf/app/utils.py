from .models import Contractor, License

def get_contractor(id):
    contractor = Contractor.query.get_or_404(id)
    return contractor


def get_license(id):
    license = License.query.get_or_404(id)
    return license
