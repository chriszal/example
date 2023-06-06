from api.model.clinicians import Clinicians

class CliniciansService:

    def create_user(self, first_name, last_name, email, password, roles):
        user = Clinicians(first_name=first_name, last_name=last_name,
                    email=email, roles=roles)
        user.set_password(password)
        user.save()
        return user

    def list_users(self):
        return Clinicians.objects.all()
