from .models import Contractor, License, Permit

def get_contractor(id):
    contractor = Contractor.query.get_or_404(id)
    return contractor


def get_license(id):
    license = License.query.get_or_404(id)
    return license


def get_permit(id):
    permit = Permit.query.get_or_404(id)
    return permit
